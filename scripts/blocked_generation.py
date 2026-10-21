"""Shared fail-closed entry point for retired unsafe candidate runners."""
import json
from audit import audit


def main():
    try:
        proof = audit()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'decision': 'STOP_INPUT_ERROR', 'authorized_to_submit': False, 'error': str(exc)}))
        return 3
    # A future nonblocking proof is NOT clearance: requires an assigned lane,
    # full inventory gates, compliant holdout and separate selector approval.
    print(json.dumps({
        'decision': proof['decision'], 'authorized_to_submit': False,
        'reason': 'Retired runner: no experiment or TIFF write permitted. See evidence/run-card.json.',
    }))
    return 2
