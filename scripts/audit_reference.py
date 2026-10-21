#!/usr/bin/env python3
"""Study H33 bytes, never copy them into a new submission or use them as features."""
import json
from pathlib import Path

import numpy as np
from scipy.ndimage import distance_transform_edt
from scipy.spatial import cKDTree

from audit import ROOT, read_verified
from restore_inputs import restore

SOURCE = {
 'repo': 'buffedlizard55-lab/GEMSDOE32',
 'ref': 'f62038b54dcb7767d4d997f80b033cdc3d42bef9',
 'path': 'docs/downloads/gemsdoe32-h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros.tif',
 'sha256': 'c55bafc470054e8271dcb89347a17e07fefe50de6af6e6ba6c4b169ef7ab6fa9'
}


def main():
    path = Path('.cache/reference/h33.tif')
    restore(SOURCE['repo'], SOURCE['ref'], SOURCE['path'], SOURCE['sha256'], path)
    pred, grid = read_verified(ROOT/path, SOURCE['sha256'])
    man = {e['id']: e for e in json.loads((ROOT/'registry/data_manifest.json').read_text())['files']}
    sample, sg = read_verified(ROOT/'data/bridge/sample_submission.tif',man['sample_submission']['sha256'])
    cat, cg = read_verified(ROOT/'data/bridge/existing_faults.tif',man['existing_faults']['sha256'])
    if grid != sg or sg != cg:
        raise ValueError('reference grid mismatch')
    foot = np.isfinite(sample)
    dots = np.isfinite(pred) & (pred > 0)
    cat = np.isfinite(cat) & (cat > 0)
    coords = np.column_stack(np.nonzero(dots))
    spacing = cKDTree(coords).query(coords, k=2)[0][:,1]
    result = {
      'evidence_class': 'REFERENCE-BYTE-MEASUREMENT, NOT A SCORE', 'source': SOURCE,
      'purpose': 'Learning only. Never a candidate, ranking feature or submission download.',
      'grid_matches': True, 'all_values_finite': bool(np.isfinite(pred).all()),
      'values_in_0_1': bool(np.isfinite(pred).all() and (pred>=0).all() and (pred<=1).all()),
      'unique_values': np.unique(pred).tolist(), 'positive_pixels': int(dots.sum()),
      'dots_on_catalogue': int((dots & cat).sum()), 'dots_outside_footprint': int((dots & ~foot).sum()),
      'minimum_catalogue_distance_px': float(distance_transform_edt(~cat)[dots].min()),
      'nearest_dot_spacing_px_quantiles': {str(q):float(np.quantile(spacing,q)) for q in (0,0.5,1)},
      'reported_performance': {'value':0.2778,'evidence_class':'USER-REPORTED, NOT ORGANIZER-CONFIRMED',
                              'organizer_receipt':None},
      'warning':'GEMSDOE32 build receipt says UNSCORED; its projections and legacy holdout summaries are not compatible evidence of a current pooled HOLDOUT-DTI.'
    }
    (ROOT/'evidence/reference_audit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
