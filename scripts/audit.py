#!/usr/bin/env python3
"""Reproducible, candidate-independent literal-support stop proof. Never a clearance.

Exit 2: literal finite-positive support is universally covered by one witness.
       The pinned template has a competing like-for-like surface interpretation;
       this code reports the semantic caveat and stays fail-closed.
Exit 3: untrusted or missing inputs. Exit 0: no universal proof, NOT approval.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor'))
from gems57.uniqueness import _dots, _near, OVERLAP_LIMIT  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def domain_proof(allowed, witness):
    allowed = np.asarray(allowed)
    witness = np.asarray(witness)
    if allowed.dtype != bool or allowed.ndim != 2 or witness.shape != allowed.shape:
        raise ValueError('2D boolean allowed mask and matching witness required')
    support = _dots(witness)
    near = _near(support, radius_px=3.0)
    count = int(allowed.sum())
    covered = int((allowed & near).sum())
    return dict(allowed_pixels=count, witness_positive_pixels=int(support.sum()),
                exact_positive_allowed_pixels=int((allowed & support).sum()),
                covered_allowed_pixels=covered, uncovered_allowed_pixels=count-covered,
                universal_overlap_blocker=count > 0 and covered == count,
                forward_overlap_for_every_nonempty_candidate=1.0 if count > 0 and covered == count else None,
                stop_threshold_strictly_greater_than=OVERLAP_LIMIT)


def check_template(root=ROOT):
    pin = json.loads((root / 'registry/template_pin.json').read_text())
    for name, expected in pin['files'].items():
        if sha256(root / 'vendor/gems57' / name) != expected:
            raise ValueError(f'upstream template modified: {name}')
    return pin


def read_verified(path, expected):
    if sha256(path) != expected:
        raise ValueError(f'input SHA256 mismatch: {path.name}')
    with rasterio.open(path) as ds:
        if ds.count != 1 or ds.crs is None:
            raise ValueError(f'one band with CRS required: {path.name}')
        return ds.read(1), (ds.crs.to_string(), ds.shape, tuple(ds.transform))


def audit(root=ROOT):
    pin = check_template(root)
    man = {x['id']: x for x in json.loads((root/'registry/data_manifest.json').read_text())['files']}
    source = json.loads((root/'registry/witness_sources.json').read_text())['dense_witness']
    inputs = {
        'sample': (root/'data/bridge/sample_submission.tif', man['sample_submission']['sha256']),
        'catalogue': (root/'data/bridge/existing_faults.tif', man['existing_faults']['sha256']),
        'witness': (root/'.cache/registry/dense_witness.tif', source['sha256']),
    }
    arrays, grids = {}, {}
    for name, (path, expected) in inputs.items():
        arrays[name], grids[name] = read_verified(path, expected)
    if any(g != grids['sample'] for g in grids.values()):
        raise ValueError('CRS/shape/transform mismatch')
    foot = np.isfinite(arrays['sample'])
    if not foot.any() or not np.isfinite(arrays['catalogue'][foot]).all():
        raise ValueError('empty footprint or nonfinite catalogue inside footprint')
    cat = foot & _dots(arrays['catalogue'])
    proof = domain_proof(foot & ~cat, np.where(foot, arrays['witness'], 0))
    full_proof = domain_proof(foot, np.where(foot, arrays['witness'], 0))
    blocked = proof['universal_overlap_blocker']
    return {
        'schema': 'gems81-preflight-v1', 'evidence_class': 'REGISTRY-MEASUREMENT, not a performance score',
        'decision': 'STOP_LITERAL_SUPPORT_OVERLAP' if blocked else 'NO_LITERAL_UNIVERSAL_PROOF_NOT_CLEARANCE',
        'scope': 'One verified witness suffices for a stop under the literal positive-support reading; this is not a resolved like-for-like dot-field finding or a complete registry scan.',
        'input_sha256': {k: v[1] for k,v in inputs.items()}, 'witness_source': source,
        'template_commit': pin['commit'], 'template_hashes_verified': True,
        'grid': {'crs': grids['sample'][0], 'shape': grids['sample'][1], 'transform': grids['sample'][2]},
        'footprint_pixels': int(foot.sum()), 'catalogue_pixels': int(cat.sum()),
        'proof': proof, 'including_catalogue_proof': full_proof,
        'support_definition': 'finite registry prediction value > 0; literal positive-pixel support, regardless of dense-surface representation',
        'argument': 'Under this support definition, for A contained in the 3px halo W of a prior, every nonempty C subset A has |C intersect W|/|C|=1 > 0.70. This is a candidate-independent stop under the literal reading.',
        'shared_template_semantic_caveat': 'Pinned uniqueness.py also provides two_phase_summary: it classifies dense supports as continuous surfaces and says their overlap firing is not duplication evidence. The user protocol does not explicitly resolve whether such positive support counts as registry raster dots; do not silently choose the exemption or claim this is interpretation-independent impossibility.',
        'rank_correlation': None,
        'rank_correlation_reason': 'No new pre-emission surface was built. The inherited candidate has a separate final-raster audit in evidence/legacy-candidate-audit.json; the universal overlap proof is sufficient to stop before placement under the literal positive-support reading.',
        'candidate_generated_by_this_audit': False,
        'inherited_candidate_audit': 'evidence/legacy-candidate-audit.json',
        'experiments_run_this_turn': 0, 'weekly_slots_used': 0,
        'authorized_to_submit': False, 'verdict': 'negative'
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=ROOT/'evidence/preflight.json')
    args = ap.parse_args()
    try:
        result = audit()
        code = 2 if result['proof']['universal_overlap_blocker'] else 0
    except (OSError, ValueError, KeyError, TypeError, rasterio.errors.RasterioError) as exc:
        result = {'decision': 'STOP_INPUT_ERROR', 'error': str(exc), 'authorized_to_submit': False, 'verdict': 'negative'}
        code = 3
    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_suffix('.partial')
    tmp.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    tmp.replace(args.out)
    print(json.dumps(result, indent=2, allow_nan=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
