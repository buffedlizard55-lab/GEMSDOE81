"""Small mathematical tests for the pinned shared metric, not geological evidence."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57.metric import dti_binary, kernel  # noqa: E402


def test_kernel():
    assert kernel(0) == 1
    assert kernel(3) == 0
    assert abs(kernel(1.5) - 0.5) < 1e-12


def test_dti_perfect():
    truth = np.zeros((9, 9), bool)
    truth[4, 4] = True
    assert dti_binary(truth.copy(), truth)["dti"] > 0.999


def test_dti_empty_prediction():
    truth = np.zeros((9, 9), bool)
    truth[4, 4] = True
    assert dti_binary(np.zeros((9, 9), bool), truth)["dti"] == 0
