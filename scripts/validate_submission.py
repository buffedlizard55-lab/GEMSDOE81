#!/usr/bin/env python3
"""CLI local validation only. Nonzero on failed checks; never slot approval."""
import argparse
import json

import numpy as np

from audit import ROOT, audit, read_verified
from gems57.gates import format_report
from gems57.validate import validate
from audit_existing import NAME


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='?', default=ROOT/'docs/downloads'/NAME)
    args = parser.parse_args()
    try:
        proof = audit()  # verify template/data provenance even if blocked
        sample = ROOT/'data/bridge/sample_submission.tif'
        footprint, _ = read_verified(sample, proof['input_sha256']['sample'])
        catalogue, _ = read_verified(ROOT/'data/bridge/existing_faults.tif', proof['input_sha256']['catalogue'])
        fp = np.isfinite(footprint)
        report = validate(args.file, footprint=fp, catalogue=(catalogue > 0) & fp)
        template = format_report(args.file, sample, footprint=fp)
        passed = report['all_checks_passed'] and template['ok']
        result = {'validator': report, 'template': template, 'authorized_to_submit': False,
                  'status': 'LOCAL_FORMAT_PASS' if passed else 'LOCAL_FORMAT_FAIL',
                  'registry_decision': proof['decision']}
        code = 0 if passed else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'status': 'VALIDATION_ERROR', 'error': str(exc), 'authorized_to_submit': False}
        code = 3
    print(json.dumps(result, indent=2, allow_nan=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
