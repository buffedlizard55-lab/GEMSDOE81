#!/usr/bin/env bash
# Audit inputs only. No incomplete or unverified training-feature download.
set -euo pipefail
cd "$(dirname "$0")/.."
python_bin="${PYTHON:-python}"
exec "$python_bin" scripts/restore_inputs.py
