"""Regression checks for the merged parallel-session safety conflict."""
import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'src'), str(ROOT/'vendor')]
from audit_existing import NAME, SHA256, inspect
from audit import sha256
from gems81 import submission_writer as compatibility_writer
from gems57 import submission_writer as shared_writer
from gems57 import metric as shared_metric


def test_no_private_writer_or_metric_fork():
    from gems81 import metric
    assert compatibility_writer.write_submission is shared_writer.write_submission
    assert metric.dti_binary is shared_metric.dti_binary
    assert metric.kernel is shared_metric.kernel


@pytest.mark.parametrize('value', [np.nan, np.inf, -9999, -.01, 1.01])
def test_compatibility_writer_no_longer_coerces_bad_floats_to_dots(tmp_path, value):
    prediction = np.zeros((3,3), np.float32)
    prediction[1,1] = value
    with pytest.raises(ValueError, match='finite and in'):
        compatibility_writer.write_submission(tmp_path/'rejected.tif', prediction,
            tmp_path/'missing-template.tif', np.ones((3,3), bool),
            name='unit-test', note='Synthetic software test, not a geological experiment')
    assert not list(tmp_path.iterdir())


def test_private_holdout_is_retired():
    from gems81.holdout import make_draws
    with pytest.raises(RuntimeError, match='retired'):
        make_draws(None, None)


@pytest.mark.parametrize('entrypoint', ['build_submission', 'finalize_submission'])
def test_generation_runners_stop_even_without_universal_proof(monkeypatch, entrypoint, capsys):
    import blocked_generation
    monkeypatch.setattr(blocked_generation, 'audit', lambda: {'decision':'NO_UNIVERSAL_PROOF_NOT_CLEARANCE'})
    runner = importlib.import_module(entrypoint)
    assert runner.main() == 2
    assert json.loads(capsys.readouterr().out)['authorized_to_submit'] is False


def test_generation_runner_fails_closed_on_missing_data(monkeypatch, capsys):
    import blocked_generation
    def fail():
        raise FileNotFoundError('missing witness')
    monkeypatch.setattr(blocked_generation, 'audit', fail)
    assert blocked_generation.main() == 3
    result = json.loads(capsys.readouterr().out)
    assert result['decision'] == 'STOP_INPUT_ERROR'
    assert result['authorized_to_submit'] is False


def site_fixture(tmp_path, monkeypatch):
    # Superseded fixture: the site builder now publishes the promoted CONT
    # candidate from evidence/run_card.json, still failing closed.
    import build_site
    for folder in ('evidence','docs/downloads','registry'):
        (tmp_path/folder).mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT/'evidence/run_card.json', tmp_path/'evidence/run_card.json')
    card = json.loads((ROOT/'evidence/run_card.json').read_text())
    shutil.copy(ROOT/'docs/downloads'/card['submission_name'],
                tmp_path/'docs/downloads'/card['submission_name'])
    monkeypatch.setattr(build_site, 'ROOT', tmp_path)
    monkeypatch.setattr(build_site, 'DOCS', tmp_path/'docs')
    return build_site, card


def test_site_rejects_stale_authorization(tmp_path, monkeypatch):
    builder, card = site_fixture(tmp_path, monkeypatch)
    path = tmp_path/'evidence/run_card.json'
    card['verdict'] = 'negative'
    path.write_text(json.dumps(card))
    with pytest.raises(ValueError, match='promote'):
        builder.main()
    assert not (tmp_path/'docs/index.html').exists()


def test_site_rejects_changed_tif_bytes(tmp_path, monkeypatch):
    builder, card = site_fixture(tmp_path, monkeypatch)
    with (tmp_path/'docs/downloads'/card['submission_name']).open('ab') as stream:
        stream.write(b'changed')
    with pytest.raises(ValueError, match='SHA256 mismatch'):
        builder.main()
    assert not (tmp_path/'docs/index.html').exists()


def test_site_build_is_idempotent(tmp_path, monkeypatch):
    builder, card = site_fixture(tmp_path, monkeypatch)
    builder.main()
    before = {p.relative_to(tmp_path): sha256(p) for p in (tmp_path/'docs').rglob('*') if p.is_file()}
    builder.main()
    after = {p.relative_to(tmp_path): sha256(p) for p in (tmp_path/'docs').rglob('*') if p.is_file()}
    assert before == after


def test_existing_tif_checked_with_shared_tools():
    if not (ROOT/'.cache/registry/dense_witness.tif').exists():
        pytest.skip('restore_inputs.py needed for full-resolution check')
    card = inspect()
    recorded = json.loads((ROOT/'evidence/run-card.json').read_text())
    assert card == recorded
    assert card['raster_sha256'] == SHA256
    assert card['validator_output']['status'] == 'LOCAL_FORMAT_PASS'
    assert card['registry']['final_dot_overlap_within_3px'] == 1
    assert card['authorized_to_download_and_submit'] is False
    assert card['experiments_run'] == card['weekly_slots_used'] == 0


def test_validator_cli_missing_file_returns_failure():
    result = subprocess.run([sys.executable, str(ROOT/'scripts/validate_submission.py'),
                             str(ROOT/'does-not-exist.tif')], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    record = json.loads(result.stdout)
    assert record['authorized_to_submit'] is False
    assert record['status'] == 'VALIDATION_ERROR'


def test_legacy_results_are_not_accepted_holdout_or_ci():
    legacy = json.loads((ROOT/'evidence/legacy-asb.json').read_text())
    assert legacy['ci95'] is None
    assert legacy['authorized_to_submit'] is False
    assert legacy['status'] == 'SUPERSEDED_UNACCEPTED_VALIDATION'
    for path in (ROOT/'evidence/run.json',
                 ROOT/'docs/downloads'/NAME.replace('.tif','.receipt.json')):
        record = json.loads(path.read_text())
        assert record['authorized_to_submit'] is False
        assert record['status'] == 'SUPERSEDED'
        assert 'holdout_DTI' not in record
        target = (path.parent/record['authoritative_card']).resolve()
        assert target.exists()
        assert json.loads(target.read_text())['verdict'] == 'negative'
    # The canonical card is the session-2 CONT promotion, a separate file.
    card = json.loads((ROOT/'evidence/run_card.json').read_text())
    assert card['verdict'] == 'promote' and 'holdout_DTI' in card


def test_validator_cli_nonzero_for_failed_report(monkeypatch, capsys):
    import validate_submission as cli
    monkeypatch.setattr(sys, 'argv', ['validate_submission.py', 'synthetic.tif'])
    monkeypatch.setattr(cli, 'audit', lambda: {'decision': 'STOP_UNIVERSAL_DUPLICATE',
        'input_sha256': {'sample': 'test-fixture', 'catalogue': 'test-fixture'}})
    monkeypatch.setattr(cli, 'read_verified', lambda *args: (np.zeros((2,2)), None))
    monkeypatch.setattr(cli, 'validate', lambda *args, **kwargs: {'all_checks_passed': False})
    monkeypatch.setattr(cli, 'format_report', lambda *args, **kwargs: {'ok': False})
    assert cli.main() == 1
    result = json.loads(capsys.readouterr().out)
    assert result['status'] == 'LOCAL_FORMAT_FAIL'
    assert result['authorized_to_submit'] is False
