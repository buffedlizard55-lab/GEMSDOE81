#!/usr/bin/env python3
"""Validate the promoted submission (or a path given as argv[1]) against the
sample template. No human inspection needed: exit 0 only if all checks pass."""
import sys
sys.path.insert(0, "src")
from gems81.submission_writer import validate
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) > 1:
    f = sys.argv[1]
else:
    card = json.loads((ROOT / "evidence/run_card.json").read_text())
    f = str(ROOT / "docs/downloads" / card["submission_name"])
rep = validate(f, str(ROOT / "data/sample_submission.tif"))
print(json.dumps(rep, indent=2))
raise SystemExit(0 if rep["checks"]["all_passed"] else 1)
