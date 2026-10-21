#!/usr/bin/env python3
"""Audit an existing GEMS GeoTIFF without writing or repairing it.

A local format pass is not uniqueness clearance, scientific promotion, or
organizer acceptance. This command uses the pinned shared validator and literal
uniqueness definition; it never clips, fills, or writes prediction rasters.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from audit import check_template, domain_proof, read_verified, sha256  # noqa: E402
from gems57.uniqueness import (  # noqa: E402
    _dots,
    _near,
    OVERLAP_LIMIT,
    representation_class,
)
from gems57.validate import validate  # noqa: E402


def _grid(ds):
    return (ds.crs.to_string() if ds.crs else None, ds.shape, tuple(ds.transform))


def audit_candidate(candidate_path: Path, *, root: Path = ROOT) -> dict:
    """Return format and literal-registry checks for an existing candidate."""
    candidate_path = Path(candidate_path)
    if not candidate_path.is_absolute():
        candidate_path = root / candidate_path
    if not candidate_path.is_file():
        raise FileNotFoundError(candidate_path)

    pin = check_template(root)
    manifest = {
        entry["id"]: entry
        for entry in json.loads((root / "registry/data_manifest.json").read_text())["files"]
    }
    witness_source = json.loads(
        (root / "registry/witness_sources.json").read_text()
    )["dense_witness"]
    sample_path = root / "data/bridge/sample_submission.tif"
    catalogue_path = root / "data/bridge/existing_faults.tif"
    witness_path = root / ".cache/registry/dense_witness.tif"

    sample, sample_grid = read_verified(
        sample_path, manifest["sample_submission"]["sha256"]
    )
    catalogue, catalogue_grid = read_verified(
        catalogue_path, manifest["existing_faults"]["sha256"]
    )
    witness, witness_grid = read_verified(witness_path, witness_source["sha256"])
    if sample_grid != catalogue_grid or sample_grid != witness_grid:
        raise ValueError("sample, catalogue, and registry witness grids must match")

    with rasterio.open(candidate_path) as ds:
        if ds.count != 1:
            raise ValueError("candidate must be a single-band GeoTIFF")
        prediction = ds.read(1)
        candidate_grid = _grid(ds)
    grid_matches = candidate_grid == sample_grid
    if prediction.shape != sample.shape:
        raise ValueError("candidate shape differs from the sample-submission grid")

    footprint = np.isfinite(sample)
    mapped = np.isfinite(catalogue) & (catalogue > 0)
    format_report = validate(candidate_path, footprint=footprint, catalogue=mapped)
    format_report["file"] = candidate_path.name
    # Keep this explicit even though the shared validator also checks the fixed
    # competition grid: exact equality to this sample file is the required test.
    format_report["checks"]["exact_sample_crs_shape_transform"] = grid_matches
    format_report["checks"]["all_passed"] = bool(
        all(value for key, value in format_report["checks"].items() if key != "all_passed")
    )
    candidate_dots = _dots(prediction) & footprint
    witness_dots = _dots(witness) & footprint
    witness_representation = representation_class(
        int(witness_dots.sum()), int(footprint.sum())
    )
    near_witness = _near(witness_dots, radius_px=3.0)
    overlap = float(near_witness[candidate_dots].mean()) if candidate_dots.any() else None

    # Before emission, this proof covers every possible nonempty support in the
    # allowed footprint. It is stronger than measuring one proposal surface.
    allowed = footprint & ~mapped
    preplacement = domain_proof(allowed, np.where(footprint, witness, 0))
    witness_values = witness[footprint]
    prediction_values = prediction[footprint]
    final_rho = None
    rho_reason = None
    if not np.isfinite(prediction_values).all():
        rho_reason = "Candidate contains nonfinite footprint values; correlation is not evaluated."
    elif np.ptp(witness_values) == 0 or np.ptp(prediction_values) == 0:
        rho_reason = "Spearman correlation is undefined because one compared raster is constant on the footprint."
    else:
        from scipy.stats import spearmanr

        final_rho = float(spearmanr(prediction_values, witness_values).statistic)
        if not np.isfinite(final_rho):
            final_rho = None
            rho_reason = "Spearman correlation was numerically undefined."

    return {
        "schema": "gems81-candidate-audit-v1",
        "evidence_class": "LOCAL-FORMAT-VALIDATION and REGISTRY-MEASUREMENT; not a performance score",
        "candidate": {
            "name": candidate_path.name,
            "sha256": sha256(candidate_path),
            "bytes": candidate_path.stat().st_size,
            "positive_pixels_in_footprint": int(candidate_dots.sum()),
            "grid_matches_sample": grid_matches,
            "pre_emission_surface_retained": False,
        },
        "template": {"commit": pin["commit"], "hashes_verified": True},
        "input_sha256": {
            "sample_submission": manifest["sample_submission"]["sha256"],
            "existing_faults": manifest["existing_faults"]["sha256"],
            "dense_witness": witness_source["sha256"],
        },
        "validator": format_report,
        "registry": {
            "evidence_class": "REGISTRY-MEASUREMENT",
            "witness": witness_source,
            "witness_positive_pixels_in_footprint": int(witness_dots.sum()),
            "witness_representation": witness_representation,
            "candidate_dot_overlap_within_3px": overlap,
            "overlap_limit_strictly_greater_than": OVERLAP_LIMIT,
            "duplicate_by_literal_overlap": bool(
                overlap is not None and overlap > OVERLAP_LIMIT
            ),
            "shared_template_two_phase_note": (
                "The pinned two_phase_summary classifies this support as a "
                "continuous_surface and does not treat its overlap firing as "
                "duplication evidence. The user's dot-field semantics are "
                "unresolved; this audit reports the literal overlap and keeps "
                "the artifact unauthorized."
            ),
            "final_raster_spearman_vs_witness": final_rho,
            "final_raster_spearman_status": rho_reason or "computed on footprint",
            "pre_emission_surface_spearman": None,
            "pre_emission_surface_status": "NOT MEASURED: un-emitted surface bytes were not retained",
            "preplacement_universal_overlap_proof": preplacement,
            "scope": "One hash-verified witness is a candidate-independent stop under the literal finite-positive support definition; this is not a complete registry scan or a resolved like-for-like dot-field finding.",
        },
        "authorized_to_download_and_submit": False,
        "verdict": "negative",
        "verdict_reason": (
            "Under the literal finite-positive support definition the overlap gate fires. "
            "The pinned template's two-phase continuous-surface interpretation creates "
            "a semantic conflict, and lane assignment, full dot-field registry clearance, "
            "and protocol-compliant shared HOLDOUT-DTI are absent. Keep this artifact "
            "unauthorized; local format validity is not submission approval."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="existing candidate GeoTIFF to audit")
    parser.add_argument("--out", type=Path, help="optional JSON report destination")
    args = parser.parse_args()
    try:
        result = audit_candidate(args.candidate)
    except (OSError, ValueError, KeyError, TypeError, rasterio.errors.RasterioError) as exc:
        result = {
            "schema": "gems81-candidate-audit-v1",
            "decision": "STOP_INPUT_ERROR",
            "error": str(exc),
            "authorized_to_download_and_submit": False,
            "verdict": "negative",
        }
        code = 3
    else:
        code = 0 if result["validator"]["all_checks_passed"] else 3
        if result["registry"]["duplicate_by_literal_overlap"]:
            code = 2
    rendered = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.out:
        out = args.out if args.out.is_absolute() else ROOT / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(out.suffix + ".partial")
        tmp.write_text(rendered)
        tmp.replace(out)
    print(rendered, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
