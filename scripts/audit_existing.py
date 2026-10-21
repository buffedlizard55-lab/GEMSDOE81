#!/usr/bin/env python3
"""Recheck the inherited negative TIFF, not a new surface/emission experiment."""
import json
from pathlib import Path

import numpy as np

from audit import ROOT, audit, read_verified
from gems57.gates import format_report
from gems57.uniqueness import dot_overlap
from gems57.validate import validate

NAME = 'gems81-asb-poisson44090-buf2-20261021T221522Z-1a12c8f1-zeros.tif'
SHA256 = 'e548bc657c9141f17af11b2c9063894eb0abcb4665504f22e1d3dde3ce504402'


def inspect(root=ROOT):
    proof = audit(root)  # authenticates inputs and shared tools before using them
    manifest = {e['id']: e for e in json.loads((root/'registry/data_manifest.json').read_text())['files']}
    sample_path = root/'data/bridge/sample_submission.tif'
    sample, grid = read_verified(sample_path, manifest['sample_submission']['sha256'])
    catalogue, _ = read_verified(root/'data/bridge/existing_faults.tif', manifest['existing_faults']['sha256'])
    witness, _ = read_verified(root/'.cache/registry/dense_witness.tif', proof['input_sha256']['witness'])
    path = root/'docs/downloads'/NAME
    pred, pred_grid = read_verified(path, SHA256)
    if grid != pred_grid:
        raise ValueError('inherited candidate grid differs from template')
    foot = np.isfinite(sample)
    local = validate(path, footprint=foot, catalogue=(catalogue > 0) & foot)
    template = format_report(path, sample_path, footprint=foot)
    overlap = dot_overlap(pred, witness)
    return {
        'schema': 'gems81-reviewed-negative-v2',
        'hypothesis': 'Inherited ASB: antithetic scarp-pair ranks combined with basement/conductivity gradient ranks.',
        'mechanism': 'Prior-session rank-surface Poisson thinning; this review only rechecks existing raster bytes and gates.',
        'named_non_fault_mimic': 'Paired terrace risers or paleo-shorelines over sedimentary pinch-outs.',
        'lane': 'No identifiable assigned method paragraph; no new geological lane opened.',
        'holdout': {
            'evidence_class': 'HOLDOUT-DTI', 'value': None, 'ci95': None,
            'withheld_positives': None, 'evaluator_version': 'gems57-pooled-hide-v2',
            'status': 'NOT RUN: binding uniqueness stop; legacy private-evaluator results are not accepted validation.',
            'legacy_record': 'evidence/legacy-asb.json',
        },
        'leakage_canary': {'auc': None, 'status': 'NOT RUN: legacy AUC used full catalogue, not fold-withheld positives.'},
        'registry': {
            'evidence_class': 'REGISTRY-MEASUREMENT, not a performance score',
            'final_dot_overlap_within_3px': overlap,
            'rank_correlation': None,
            'rank_correlation_reason': 'Not needed for rejection: overlap alone exceeds the binding limit.',
            'witness_sha256': proof['input_sha256']['witness'],
            'surface_check': 'Original continuous surface not preserved; universal proof rejects all nonempty in-footprint support.',
            'scope': 'One sufficient rejection witness; no full inventory clearance claimed.',
            'decision': 'duplicate' if overlap > 0.70 else 'unresolved',
        },
        'raster_sha256': SHA256,
        'validator_output': {
            'status': 'LOCAL_FORMAT_PASS' if local['all_checks_passed'] and template['ok'] else 'LOCAL_FORMAT_FAIL',
            'no_nan_inside_footprint': local['checks']['in_footprint_all_finite'],
            'values_in_0_1': local['checks']['in_footprint_range_0_1'] and template['ok'],
            'crs_shape_transform_match': grid == pred_grid,
            'shared_validator': local, 'shared_template_report': template,
            'warning': 'Local validation is not organizer acceptance or slot authorization.',
        },
        'submission_name': NAME,
        'note': 'NEGATIVE ASB archive: local format pass, duplicate registry overlap; not approved for competition submission.',
        'verdict': 'negative', 'decision': 'STOP_DUPLICATE',
        'authorized_to_download_and_submit': False,
        'research_download_only': True,
        'new_tif_generated_this_session': False,
        'experiments_run': 0, 'weekly_slots_used': 0,
        'incomplete_requirements': [
            'No new unique competition-ready TIFF; binding duplicate stop remains active.',
            'No valid buffered shared-evaluator holdout or spatial confidence interval.',
            'No organizer receipt or measured improvement over reported historical scores.',
        ],
    }


def main():
    card = inspect()
    if card['registry']['decision'] != 'duplicate':
        raise ValueError('Witness no longer rejects inherited raster; do not silently publish a new decision')
    if not 0 < len(card['note']) <= 140:
        raise ValueError('invalid short note')
    (ROOT/'evidence/run-card.json').write_text(json.dumps(card, indent=2, allow_nan=False)+'\n')
    print(json.dumps(card, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
