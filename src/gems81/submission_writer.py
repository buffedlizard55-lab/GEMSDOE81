"""Compatibility imports ONLY; the pinned shared writer owns all validation.

No boolean coercion, clipping or automatic masking of model output. Local format
validation never guarantees organizer acceptance or permission to use a slot.
Callers must use the shared API: write_submission(path, prediction, sample,
footprint, note=..., name=..., catalogue=...).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'vendor'))
from gems57.submission_writer import write_submission  # noqa: E402,F401
from gems57.validate import validate, sha256 as sha256_file  # noqa: E402,F401
