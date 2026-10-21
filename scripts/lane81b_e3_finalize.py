#!/usr/bin/env python3
"""E3 (final experiment): emit PCD poisson44090 buf2 on FULL catalogue, registry
lane checks vs winner/d28/ASB binary rasters, fail-closed writer, run card.
Science verdict is NEGATIVE from E2 -- this file is a measured negative
deliverable, NOT promoted for a weekly slot (selector step decides otherwise)."""
import hashlib, json, sys, time
import numpy as np, rasterio
from pathlib import Path
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from gems81.emission import poisson_thin_priority
from gems81.submission_writer import write_submission

try:
    S = np.load("/tmp/PCD_piedmont.npy")
    S_asb = np.load("/tmp/ASB_control_rebuilt.npy")
except FileNotFoundError:
    from gems81.surfaces81b import build_all
    from gems81.surface import build as build_asb
    S = build_all(ROOT / "data")[0]["PCD_piedmont"]
    S_asb, _, _ = build_asb(ROOT / "data")
with rasterio.open(ROOT / "data/sample_submission.tif") as ds: foot = np.isfinite(ds.read(1))
with rasterio.open(ROOT / "data/labels.tif") as ds: labels = (ds.read(1) > 0) & foot
allowed = foot & (distance_transform_edt(~labels) > 2)
mask = poisson_thin_priority(S, allowed, 44090) & foot & ~labels
print("dots:", int(mask.sum()), flush=True)

REG = {
 "winner_h33-2-b2_ORGANIZER-REPORTED_0.2778": "/tmp/reg81/winner.tif",
 "d28_base_REPORTED_0.2600": "/tmp/reg81/d28.tif",
 "gems81_ASB_20261021_UNSCORED": str(ROOT / "docs/downloads/gems81-asb-poisson44090-buf2-20261021T221522Z-1a12c8f1-zeros.tif"),
}
rng = np.random.default_rng(81)
samp = rng.choice(np.flatnonzero(foot), 300000, replace=False)
reg = {}
for name, p in REG.items():
    with rasterio.open(p) as ds: r = np.nan_to_num(ds.read(1))
    rm = r > 0
    corr = float(spearmanr(S.ravel()[samp], r.ravel()[samp]).statistic)
    ov = float((distance_transform_edt(~rm)[mask] <= 3).mean())
    reg[name] = dict(surface_rank_corr_sampled=corr, dot_overlap_within_3px=ov,
                     lane_violation=bool(abs(corr) > 0.90 or ov > 0.70))
    print("REG", name, reg[name], flush=True)
reg["surface_vs_ASB_surface_rank_corr_sampled"] = float(spearmanr(S.ravel()[samp], S_asb.ravel()[samp]).statistic)
assert not any(v.get("lane_violation") for v in reg.values() if isinstance(v, dict)), reg

stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
sha8 = hashlib.sha256(mask.tobytes()).hexdigest()[:8]
name = f"gems81-pcd-poisson44090-buf2-{stamp}-{sha8}-zeros"
out = ROOT / f"docs/downloads/{name}.tif"
rep = write_submission(mask, ROOT / "data/sample_submission.tif", out, labels=labels, footprint=foot)
note = f"GEMSDOE81 PCD piedmont-curvature poisson44090 buf2 {int(mask.sum())} dots zeros HOLDOUT-NEGATIVE"
assert len(note) <= 140, len(note)
e1 = json.loads((ROOT / "evidence/e1_canary_81b.json").read_text())
e2 = json.loads((ROOT / "evidence/e2_holdout_81b.json").read_text())
cand = e2["PCD_piedmont_poisson44090_buf2"]
card = {
 "hypothesis": "PCD: 100 m piedmont slope-break (|Laplacian detrended elevation| x gradmag(det_elev_slope) rank geometric mean, low-slope gated) marks alluvial/piedmont faults below 1 m-lidar scarp thresholds, off-catalogue.",
 "mechanism": "Label-free rank surface (training_features bands 12 det_elev, 19 det_elev_slope only) -> Poisson-disk priority thinning (min_dist 2.8px) at 44,090 dots, catalogue exclusion buffer 2px, binary {0,1}, zeros outside footprint.",
 "named_nonfault_mimic": "Terrace riser / paleo-shoreline / alluvial fan-lobe boundary (slope break with no fault offset).",
 "holdout_DTI": {"label": "HOLDOUT-DTI", "evaluator": e2["evaluator"],
   "candidate_PCD_poisson44090_buf2": cand["holdout_dti_pooled"], "per_draw": cand["per_draw"],
   "ci95_draw_range_n2_disclosed_not_bootstrap": cand["ci95_draw_range"],
   "n_hidden_positives_total": cand["n_hidden_total"],
   "same_instrument_controls": {
     "d28_as_is_HOLDOUT-DTI": e2["control_d28_as_is"]["holdout_dti_pooled"],
     "ASB_strategy_reemitted_HOLDOUT-DTI": e2["ASB_control_rebuilt_poisson44090_buf2"]["holdout_dti_pooled"],
     "PGX_PCDxGMD_HOLDOUT-DTI": e2["PGX_piedmont_x_gravmag_poisson44090_buf2"]["holdout_dti_pooled"],
     "RXF_HOLDOUT-DTI": e2["RXF_ratio_front_poisson44090_buf2"]["holdout_dti_pooled"],
     "GMD_concord_HOLDOUT-DTI": e2["GMD_concord_poisson44090_buf2"]["holdout_dti_pooled"],
     "fixed_raster_caveat": "Winner (0.0043) and shipped-ASB (0.0081) fixed rasters are mechanically depressed: their buf2 deletion used the FULL catalogue incl. hidden components. d28 was not buf2-deleted, hence is the operative same-instrument bar (re-measured identical to ASB session: 0.0992, ASB 0.0831)."},
   "canary_AUCs_all_below_0.90": {k: round(v["auc"], 4) for k, v in e1.items()}},
 "correlation_overlap_vs_registry": reg,
 "registry_irregularity_IR-81-DENSE": "Literal >0 reading vs dense 17GEMSDOE continuous witness rejects every nonempty candidate (evidence/preflight.json). Uniqueness here follows the merged ASB precedent vs BINARY registry rasters; final interpretation is the selector's. Not silently exempted.",
 "raster_sha256": rep["sha256"], "validator": rep,
 "submission_name": name + ".tif", "submission_note": note,
 "verdict": "negative",
 "verdict_reason": "FORMAT valid (validator all-pass; finite [0,1] everywhere, zeros not NaN outside footprint - cannot trigger the reported '[0,1]' rejection) but SCIENCE negative: HOLDOUT-DTI 0.0742 < d28 control 0.0992 and < ASB strategy 0.0831 on the identical instrument. DO NOT SUBMIT / do not spend a weekly slot on P(win) grounds. Live score UNSCORED; no claim of beating 0.2778 (organiser-reported for winner) or 0.4413 (leaderboard observation).",
 "experiments_used": "3 of 3 (E1 canary, E2 holdout, E3 finalize)",
 "weekly_slots_used": 0}
(ROOT / "evidence/run_card_81b.json").write_text(json.dumps(card, indent=2))
(ROOT / f"docs/downloads/{name}.receipt.json").write_text(json.dumps(card, indent=2))
print(json.dumps(card, indent=2))
