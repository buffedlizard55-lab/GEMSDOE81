"""Compatibility imports only: all metric arithmetic belongs to shared gems57."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'vendor'))
from gems57.metric import (  # noqa: E402,F401
    ALPHA, BETA, RADIUS_PX, EPS, kernel, dti_binary, dti_from_components,
)
