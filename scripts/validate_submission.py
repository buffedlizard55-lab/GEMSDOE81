#!/usr/bin/env python3
"""Run the pinned shared local format validator; does not imply uniqueness or acceptance."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from gems57.validate import validate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prediction", type=Path, help="single-band GeoTIFF to check")
    parser.add_argument(
        "--sample",
        type=Path,
        default=ROOT / "data/bridge/sample_submission.tif",
        help="trusted local sample-submission grid",
    )
    parser.add_argument("--catalogue", type=Path, help="optional mapped-fault raster")
    args = parser.parse_args()

    with rasterio.open(args.sample) as ds:
        sample = ds.read(1)
        sample_grid = (ds.crs, ds.shape, ds.transform)
        footprint = np.isfinite(sample)
    catalogue = None
    if args.catalogue:
        with rasterio.open(args.catalogue) as ds:
            catalogue = np.isfinite(ds.read(1)) & (ds.read(1) > 0)
            if (ds.crs, ds.shape, ds.transform) != sample_grid:
                raise ValueError("catalogue grid differs from the sample-submission grid")

    with rasterio.open(args.prediction) as ds:
        prediction_grid = (ds.crs, ds.shape, ds.transform)
    if prediction_grid != sample_grid:
        raise ValueError("prediction CRS, shape, or transform differs from the sample grid")

    report = validate(args.prediction, footprint=footprint, catalogue=catalogue)
    report["exact_sample_grid_match"] = True
    report["validation_scope"] = (
        "Pinned local format/range checks only; this is not a registry-uniqueness "
        "clearance, scientific promotion, or organizer acceptance."
    )
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if report["all_checks_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
