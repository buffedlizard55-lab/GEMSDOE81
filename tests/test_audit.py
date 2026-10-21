import json
import sys
from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'vendor')]
from audit import audit, check_template, domain_proof, read_verified, sha256
from gems57.evaluate_holdout import evaluate, pooled_summary
from gems57.submission_writer import write_submission
from gems57.uniqueness import dot_overlap


def test_dense_prior_blocks_any_nonempty_subset():
    allowed = np.ones((15,15), bool)
    prior = np.full((15,15), 0.00001)
    proof = domain_proof(allowed, prior)
    assert proof['universal_overlap_blocker']
    assert proof['forward_overlap_for_every_nonempty_candidate'] == 1
    rng = np.random.default_rng(81)
    for _ in range(15):
        candidate = rng.random((15,15)) < .1
        assert dot_overlap(candidate,prior) == 1


def test_exact_circular_radius_not_square():
    witness = np.zeros((11,11)); witness[5,5] = 1
    allowed = np.zeros_like(witness,bool); allowed[5,8] = True
    assert domain_proof(allowed,witness)['universal_overlap_blocker']
    allowed[8,8] = True
    assert domain_proof(allowed,witness)['covered_allowed_pixels'] == 1
    assert not domain_proof(allowed,witness)['universal_overlap_blocker']


def test_empty_domain_is_not_a_universal_proof():
    assert not domain_proof(np.zeros((3,3),bool),np.ones((3,3)))['universal_overlap_blocker']


def test_nonfinite_and_nonpositive_are_not_support():
    witness = np.array([[np.nan,np.inf,-1,0]],float)
    assert domain_proof(np.ones((1,4),bool),witness)['covered_allowed_pixels'] == 0


@pytest.mark.parametrize('allowed,witness',[(np.ones((3,3)),np.ones((3,3))),
                                          (np.ones((3,3),bool),np.ones((4,3))),
                                          (np.ones(3,bool),np.ones(3))])
def test_bad_domains_rejected(allowed,witness):
    with pytest.raises(ValueError): domain_proof(allowed,witness)


def test_shared_files_match_upstream_hashes():
    check_template()


def test_pin_tampering_detected(tmp_path):
    (tmp_path/'registry').mkdir()
    (tmp_path/'vendor/gems57').mkdir(parents=True)
    (tmp_path/'vendor/gems57/metric.py').write_text('tampered')
    (tmp_path/'registry/template_pin.json').write_text(json.dumps({'files':{'metric.py':'0'*64}}))
    with pytest.raises(ValueError, match='modified'): check_template(tmp_path)


def test_read_rejects_hash_mismatch(tmp_path):
    path=tmp_path/'bad.tif'; path.write_bytes(b'wrong')
    with pytest.raises(ValueError,match='SHA256'): read_verified(path,'0'*64)


def test_read_rejects_multiple_bands(tmp_path):
    path=tmp_path/'bands.tif'
    with rasterio.open(path,'w',driver='GTiff',height=2,width=2,count=2,dtype='float32',
                       crs='EPSG:32611',transform=from_origin(243350,4508550,100,100)) as ds:
        ds.write(np.zeros((2,2,2),np.float32))
    with pytest.raises(ValueError,match='one band'): read_verified(path,sha256(path))


def test_real_proof_matches_recorded_result():
    if not (ROOT/'.cache/registry/dense_witness.tif').exists():
        pytest.skip('run restore_inputs.py for full-resolution integration check')
    result=audit()
    assert result == json.loads((ROOT/'evidence/preflight.json').read_text()) or (
        # JSON serializes tuple grid dimensions as lists.
        json.loads(json.dumps(result)) == json.loads((ROOT/'evidence/preflight.json').read_text()))
    assert result['proof']['uncovered_allowed_pixels'] == 0
    assert not result['authorized_to_submit']


@pytest.mark.parametrize('value',[float('nan'),float('inf'),-0.01,1.01,-9999])
def test_shared_writer_rejects_range_errors_before_writing(tmp_path,value):
    prediction=np.zeros((4,4),np.float32); prediction[1,1]=value
    with pytest.raises(ValueError, match='normalized'):
        write_submission(tmp_path/'forbidden.tif',prediction,tmp_path/'nonexistent.tif',
                         np.ones((4,4),bool),name='unit-test-not-submission',note='Unit test only')
    assert not list(tmp_path.iterdir())


def test_shared_evaluator_max_cover_and_spatial_pooling():
    # Synthetic software test, NOT a geological holdout experiment or run-card score.
    truth=np.zeros((12,12),bool); truth[2,2]=True; truth[9,9]=True
    valid=np.ones_like(truth); visible=np.zeros_like(truth)
    fold={'region':valid,'truth':truth,'visible':visible,'masked_known':visible}
    p=truth.astype(float)
    result, terms=evaluate(p,fold,valid,block_side=6)
    assert result['n_truth'] == 2
    assert result['tp'] == pytest.approx(2)
    assert result['fp'] == 0
    assert result['fn'] == 0
    pooled_summary({'test':terms},draws=25,candidate='test')
    visible[2,2]=True
    masked,_=evaluate(p,fold,valid,block_side=6)
    assert masked['n_truth'] == 1


def test_no_false_submission_or_performance_claim():
    # Session-2 supersession: one promoted CONT candidate, honestly labelled.
    # The session-1 negative card stays negative and is not overwritten.
    neg=json.loads((ROOT/'evidence/run-card.json').read_text())
    assert neg['verdict']=='negative' and neg['authorized_to_download_and_submit'] is False
    card=json.loads((ROOT/'evidence/run_card.json').read_text())
    assert card['verdict']=='promote'
    sh=card['holdout_DTI']['candidate_CONT_shared']
    assert sh['all']['CONT']['dti'] > sh['all']['F_CONT']['dti'] > card['holdout_DTI']['same_instrument_controls_shared']['d28_fixed']['all']['dti']
    assert 0 < len(card['submission_note']) <= 140
    assert card['validator_shared']['validate']['all_checks_passed']
    assert card['validator_shared']['template_format_report']['ok']
    tif=ROOT/'docs/downloads'/card['submission_name']
    assert tif.exists() and sha256(tif)==card['raster_sha256']
    for v in card['correlation_overlap_vs_registry'].values():
        assert abs(v['surface_rank_corr_sampled'])<=0.90 and v['dot_overlap_within_3px']<=0.70
    home=(ROOT/'docs/index.html').read_text()
    assert 'OK TO DOWNLOAD' in home and 'OK TO SUBMIT: YES' in home
    assert card['submission_name'] in home and 'Do not submit' in home
    summary=(ROOT/'docs/executive-summary.html').read_text()
    assert 'OK TO DOWNLOAD: YES' in summary and card['submission_name'] in summary
    # Parallel-session PCD raster (arena/db89212c): present for audit, must stay
    # honestly labelled negative with a validator-clean receipt and NOT-OK page.
    pcd=ROOT/'docs/downloads/gems81-pcd-poisson44090-buf2-20261021T233503Z-67d63907-zeros.tif'
    assert pcd.exists() and sha256(pcd)=='46c4119a9f112159af874f22df7dfcd8d6508b3d3ef671202ba35b03f62ff39e'
    rc=json.loads(pcd.with_suffix('.receipt.json').read_text())
    assert rc['verdict']=='negative' and rc['validator']['checks']['all_passed'] is True
    assert 'NOT OK TO SUBMIT' in (ROOT/'docs/pcd-candidate.html').read_text()
    add=json.loads((ROOT/'evidence/registry_addendum_81b.json').read_text())
    cv=add['gems81-cont-poisson44090-buf2-20261021T233115Z-42223e10-zeros.tif']
    assert abs(cv['surface_rank_corr_sampled'])<=0.90 and cv['pcd_dots_within_3px']<=0.70


def test_all_local_website_links_and_html_fragments_resolve():
    from html.parser import HTMLParser
    from urllib.parse import unquote, urlsplit

    class Links(HTMLParser):
        def __init__(self):
            super().__init__()
            self.urls=[]
            self.anchors=set()

        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            if values.get('id'):
                self.anchors.add(values['id'])
            if tag == 'a' and values.get('name'):
                self.anchors.add(values['name'])
            for key,value in attrs:
                if key in ('href','src') and value:
                    self.urls.append(value)

    pages={page.resolve():page for page in (ROOT/'docs').rglob('*.html')}
    parsed_pages={}
    for path,page in pages.items():
        parser=Links()
        parser.feed(page.read_text())
        parsed_pages[path]=parser

    for page_path,parser in parsed_pages.items():
        for url in parser.urls:
            parts=urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            target=(page_path.parent/unquote(parts.path)).resolve() if parts.path else page_path
            assert target.exists(), (page_path,url)
            if parts.fragment and target.suffix.lower() in {'.html','.htm'}:
                target_parser=parsed_pages.get(target)
                if target_parser is None:
                    target_parser=Links()
                    target_parser.feed(target.read_text())
                    parsed_pages[target]=target_parser
                assert unquote(parts.fragment) in target_parser.anchors, (page_path,url)

    # Keep the fragment-only path under test; it used to be skipped as an empty path.
    assert any(url.startswith('#') for parser in parsed_pages.values() for url in parser.urls)


def test_current_markdown_local_links_resolve():
    import re
    from urllib.parse import unquote, urlsplit

    pages=[ROOT/'docs/hypotheses.md', ROOT/'docs/evidence-and-blockers.md',
           ROOT/'docs/research/review.md', ROOT/'docs/research/session-review.md', ROOT/'docs/research/external-source-screen.md']
    for page in pages:
        text=page.read_text()
        for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            parts=urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            target=(page.parent/unquote(parts.path)).resolve() if parts.path else page
            assert target.exists(), (page,href)


def fixture_audit_root(tmp_path, *, mismatch=False, nan_catalogue=False):
    import hashlib
    (tmp_path/'registry').mkdir()
    (tmp_path/'data/bridge').mkdir(parents=True)
    (tmp_path/'.cache/registry').mkdir(parents=True)
    # Use actual pinned upstream files; no change to the shared evaluator.
    import shutil
    shutil.copytree(ROOT/'vendor/gems57',tmp_path/'vendor/gems57')
    shutil.copy(ROOT/'registry/template_pin.json',tmp_path/'registry/template_pin.json')
    hashes={}
    for name,dest in [('sample','data/bridge/sample_submission.tif'),
                      ('catalogue','data/bridge/existing_faults.tif'),
                      ('witness','.cache/registry/dense_witness.tif')]:
        arr=np.ones((4,4),np.float32) if name != 'catalogue' else np.zeros((4,4),np.float32)
        if name=='catalogue' and nan_catalogue: arr[1,1]=np.nan
        transform=from_origin(243450 if mismatch and name=='witness' else 243350,4508550,100,100)
        path=tmp_path/dest
        with rasterio.open(path,'w',driver='GTiff',height=4,width=4,count=1,dtype='float32',
                           crs='EPSG:32611',transform=transform) as ds: ds.write(arr,1)
        hashes[name]=sha256(path)
    (tmp_path/'registry/data_manifest.json').write_text(json.dumps({'files':[
        {'id':'sample_submission','sha256':hashes['sample']},
        {'id':'existing_faults','sha256':hashes['catalogue']}]}))
    (tmp_path/'registry/witness_sources.json').write_text(json.dumps({'dense_witness':{'sha256':hashes['witness']}}))
    return tmp_path


def test_audit_rejects_grid_shift(tmp_path):
    fixture_audit_root(tmp_path,mismatch=True)
    with pytest.raises(ValueError,match='CRS/shape/transform'): audit(tmp_path)


def test_audit_rejects_nan_in_catalogue(tmp_path):
    fixture_audit_root(tmp_path,nan_catalogue=True)
    with pytest.raises(ValueError,match='nonfinite catalogue'): audit(tmp_path)


def test_audit_rejects_changed_input_bytes(tmp_path):
    fixture_audit_root(tmp_path)
    with (tmp_path/'.cache/registry/dense_witness.tif').open('ab') as f: f.write(b'changed')
    with pytest.raises(ValueError,match='SHA256'): audit(tmp_path)


def test_main_replaces_stale_approval_with_input_error(tmp_path,monkeypatch):
    import audit as mod
    out=tmp_path/'receipt.json'; out.write_text('{"authorized_to_submit":true}')
    def fail(): raise ValueError('invalid input')
    monkeypatch.setattr(mod,'audit',fail)
    monkeypatch.setattr(sys,'argv',['audit.py','--out',str(out)])
    assert mod.main() == 3
    result=json.loads(out.read_text())
    assert result['authorized_to_submit'] is False
    assert result['decision']=='STOP_INPUT_ERROR'
