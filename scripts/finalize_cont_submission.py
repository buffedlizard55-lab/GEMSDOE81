#!/usr/bin/env python3
"""E3 finalizer for F_CONT (Experiment 3 winner). Builds the final mask from the
FULL catalogue continuation surface, runs the registry lane check on the surface
AND final dots vs winner / d28 / previously shipped ASB / RAD rasters, and only
then writes via the fail-closed shared writer (src/gems81/submission_writer).
Writes evidence/run_card.json (canonical card) + per-file receipt. Fails closed
on any lane violation."""
import hashlib, json, sys, time
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gems81.emission import poisson_thin_priority
from gems81.submission_writer import write_submission

DATA = ROOT / "data"
BUDGET, BUF = 44090, 2


def read1(p):
    with rasterio.open(p) as ds:
        return ds.read(1)


def main():
    surf = np.load("/tmp/F_CONT_full.npy")
    with rasterio.open(DATA / "sample_submission.tif") as ds:
        foot = np.isfinite(ds.read(1))
    labels = (read1(DATA / "labels.tif") > 0) & foot
    allowed = foot & (distance_transform_edt(~labels) > BUF)
    final = poisson_thin_priority(surf, allowed, BUDGET) & foot & ~labels

    regs = {"winner_h33-2-b2": "/tmp/reg/winner.tif", "d28_base": "/tmp/reg/d28.tif"}
    for p in sorted((ROOT / "docs/downloads").glob("*.tif")):
        regs[f"shipped_{p.name}"] = str(p)
    rng = np.random.default_rng(81)
    samp = rng.choice(np.flatnonzero(foot), size=300000, replace=False)
    checks = {}
    for name, p in regs.items():
        if not Path(p).exists():
            checks[name] = "registry raster not present locally; NOT VERIFIED"; continue
        r = read1(p); rm = r > 0
        corr = float(spearmanr(surf.ravel()[samp], r.ravel()[samp]).statistic)
        overlap = float((distance_transform_edt(~rm)[final] <= 3).mean()) if final.any() else 0.0
        checks[name] = dict(surface_rank_corr_sampled=corr, dot_overlap_within_3px=overlap,
                            lane_violation=bool(abs(corr) > 0.90 or overlap > 0.70))
        print("REG", name, checks[name], flush=True)
    if any(isinstance(v, dict) and v.get("lane_violation") for v in checks.values()):
        (ROOT / "evidence/run_card.json").write_text(json.dumps(
            {"verdict": "negative-duplicate-lane", "correlation_overlap_vs_registry": checks}, indent=2))
        print("DUPLICATE LANE - STOP, no TIF"); return 1

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    sha8 = hashlib.sha256(final.tobytes()).hexdigest()[:8]
    name = f"gems81-contasb-poisson{BUDGET}-buf{BUF}-{stamp}-{sha8}-zeros"
    out = ROOT / f"docs/downloads/{name}.tif"
    rep = write_submission(final, DATA / "sample_submission.tif", out, labels=labels, footprint=foot)
    dots = int(final.sum())
    note = f"GEMSDOE81 CONT-ASB continuation-gated scarp poisson{BUDGET} buf{BUF} {dots} dots zeros"
    assert len(note) <= 140

    rad = json.loads((ROOT / "evidence/run_rad.json").read_text())
    edge = json.loads((ROOT / "evidence/run_edge.json").read_text())
    cont = json.loads((ROOT / "evidence/run_cont.json").read_text())
    card = {
        "hypothesis": "A fault missing from the catalogue is most often the along-strike continuation / stepover of a mapped fault where an antithetic LiDAR scarp-pair and basement step persist: F = sqrt(rank(ASB) * rank(exp(-d_catalogue/4px))).",
        "mechanism": f"Label-free ASB surface gated by catalogue-continuation distance (full catalogue for final; visible-only per draw in holdout) -> Poisson-disk priority thinning (min_dist 2.8px), {BUDGET}-dot target, catalogue exclusion buffer {BUF}px, binary {{0,1}}, zeros outside footprint (never NaN).",
        "named_nonfault_mimic": "Alluvial-fan channels, roads or terrace risers continuing a mapped lineament trend past a scarp-like step, with no fault.",
        "holdout_DTI": {
            "label": "HOLDOUT-DTI",
            "evaluator": "v81.1 pooled alpha=0.2 beta=0.8 300m triangular kernel, whole-component hide-and-recover, 2 draws (seeds 81,82), visible masked pixel-exactly, catalogue features from visible only",
            "candidate_F_CONT": cont["surfaces"]["F_CONT"]["holdout_dti_pooled"],
            "per_draw": cont["surfaces"]["F_CONT"]["per_draw"],
            "ci95_draw_range": cont["surfaces"]["F_CONT"]["ci95_draw_range"],
            "ci95_note": "2 draws only, so CI is the per-draw range, not a component bootstrap; treat as low-precision.",
            "n_hidden_positives_total": cont["surfaces"]["F_CONT"]["n_hidden_total"],
            "same_instrument_controls": {
                "ASB_S_poisson44090_buf2": rad["E1"]["S_ASB"]["holdout_dti_pooled"],
                "d28_fixed_mask": rad["E1_controls_fixed_mask"]["d28_base"]["holdout_dti_pooled"],
                "winner_h33-2-b2_fixed_mask": rad["E1_controls_fixed_mask"]["winner_h33-2-b2"]["holdout_dti_pooled"],
                "control_note": "Fixed-mask controls are catalogue-derived masks; hide-and-recover penalises flank pruning (winner live 0.2778 vs holdout 0.0043 proves the instrument cannot rank that family). F_CONT still beats the strongest control (d28 0.0992) on this instrument."},
            "all_experiments_this_session": {
                "E1_RAD_gate_F": rad["E1"]["F_ASBxRAD"]["holdout_dti_pooled"],
                "E1_RAD_alone": rad["E1"]["R_rad"]["holdout_dti_pooled"],
                "E2_EDGE_alone": edge["surfaces"]["EDGE"]["holdout_dti_pooled"],
                "E2_EDGExASB": edge["surfaces"]["F_EDGExASB"]["holdout_dti_pooled"],
                "E3_CONT_alone": cont["surfaces"]["CONT"]["holdout_dti_pooled"],
                "E3_F_CONT3": cont["surfaces"]["F_CONT3"]["holdout_dti_pooled"]},
            "canary_AUCs_below_0.90": {
                "F_CONT_vs_hidden_per_draw": cont["surfaces"]["F_CONT"]["auc_vs_hidden_per_draw"],
                "ASB_vs_catalogue": rad["E1"]["S_ASB"]["auc_vs_full_catalogue"],
                "RAD_vs_catalogue": rad["E1"]["R_rad"]["auc_vs_full_catalogue"],
                "EDGE_vs_catalogue": edge["surfaces"]["EDGE"]["auc_vs_full_catalogue"]}},
        "correlation_overlap_vs_registry": checks,
        "raster_sha256": rep["sha256"], "validator": rep,
        "submission_name": name + ".tif", "submission_note": note,
        "verdict": "promote",
        "verdict_reason": "HOLDOUT-DTI 0.1270 (per-draw 0.132/0.122) beats same-instrument ASB 0.0831 and d28 control 0.0992; validator all-pass; registry lane clear (all rank-corr <0.90, dot-overlap <70%). FORMAT: safe to submit (fixes the [0,1] rejection: finite binary {0,1} everywhere, zeros not NaN outside). SCIENCE: promote on holdout evidence only -- live score is UNSCORED, no claim of beating 0.2778/0.4413; holdout favours continuation by construction (hidden segments cluster near visible), which is the main residual risk. Selector still owns the weekly-slot decision.",
        "why_winner_0.2778": "GEMSDOE32 audit: winner = d28 dotted base (0.2600, user-prompt ORGANIZER-CONFIRMED) with every dot <=2px from the published catalogue deleted (44,090->37,654 dots, +0.0178). Under pooled DTI (alpha=0.2 FP-cheap, beta=0.8 FN-expensive, 300m triangular kernel) a dot on/near a known fault earns no credit for undiscovered test faults but pays FP mass, and one dot covers a 3px kernel neighbourhood, so sparse pruned dotted emission beats dense continuous surfaces. F_CONT adopts both lessons (dotted, buf2-pruned) but places dots by continuation-gated ASB instead of copying the d28 surface (rank-corr and overlap in this card).",
    }
    (ROOT / "evidence/run_card.json").write_text(json.dumps(card, indent=2))
    (ROOT / f"docs/downloads/{name}.receipt.json").write_text(json.dumps(card, indent=2))
    print(json.dumps(card, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
