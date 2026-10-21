#!/usr/bin/env python3
"""Session-2 experiment runner (budget: E1 surfaces, E2 budget/buffer, E3 final).

E1: leakage canary (AUC alone, flag >0.90) + pooled HOLDOUT-DTI v81.1 at the
    shipped ASB config (poisson44090, buf2) for S_ASB, R_rad, F_ASBxRAD,
    F3_ASBxRADxMAG, plus same-instrument mask controls (d28, winner) evaluated
    as fixed masks (documented instrument limitation for catalogue-flank masks).
E2: budget/buffer sweep on the E1-winning fusion surface.
E3: final mask on FULL catalogue, registry lane check vs winner+d28
    (rank-corr <=0.90 and dot-overlap <=70%), shared writer, receipt + run card.

Fails closed: any lane violation -> no TIF written, verdict negative-duplicate.
"""
import hashlib, json, sys, time
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gems81.surface_rad import build_rad
from gems81.holdout import make_draws, evaluate, auc_score
from gems81.emission import poisson_thin_priority
from gems81.submission_writer import write_submission

DATA = ROOT / "data"
REG = {  # learning / registry only, never copied into the candidate
    "winner_h33-2-b2": "/tmp/reg/winner.tif",
    "d28_base": "/tmp/reg/d28.tif",
}
BUDGETS_FINAL = 44090


def read1(p):
    with rasterio.open(p) as ds:
        return ds.read(1)


def holdout_for_surface(surf, draws, foot, budget, buf):
    ms = []
    for d in draws:
        allowed = foot & (distance_transform_edt(~d["visible"]) > buf)
        ms.append(poisson_thin_priority(surf, allowed, budget) & ~d["visible"])
    # pooled: evaluate() re-masks visible per draw, so pass a per-draw union is
    # wrong; do manual pooling identical to gems81.metric via evaluate per draw
    from gems81.metric import dti_binary, dti_from_components
    TP = FP = FN = 0.0
    per = []
    for m, d in zip(ms, draws):
        r = dti_binary(m, d["hidden"], valid=foot, known=d["visible"])
        per.append(float(r["dti"])); TP += r["tp"]; FP += r["fp"]; FN += r["fn"]
    return dict(holdout_dti_pooled=float(dti_from_components(TP, FP, FN)),
                per_draw=per, ci95_draw_range=[float(min(per)), float(max(per))],
                n_hidden_total=int(sum(int(d["n_hidden"]) for d in draws)),
                budget=budget, buffer_px=buf, emitter="poisson_thin_priority(min_dist=2.8)")


def main():
    t0 = time.time()
    ev = {"evaluator": "HOLDOUT-DTI v81.1 pooled alpha=0.2 beta=0.8 300m triangular, "
                       "whole-component hide-and-recover, 2 draws (seeds 81,82), visible masked pixel-exactly",
          "label_note": "All performance numbers below are HOLDOUT-DTI unless explicitly "
                        "ORGANIZER-CONFIRMED (organizer scores exist only for registry rasters, from the user prompt)."}
    surfaces, foot, rad_valid = build_rad(DATA)
    np.save("/tmp/S_ASB.npy", surfaces["S_ASB"]); np.save("/tmp/F.npy", surfaces["F_ASBxRAD"])
    labels = (read1(DATA / "labels.tif") > 0) & foot
    ev["footprint_pixels"] = int(foot.sum()); ev["label_pixels"] = int(labels.sum())
    ev["rad_valid_pixels"] = int(rad_valid.sum())
    draws = make_draws(labels, foot)
    ev["n_hidden_per_draw"] = [int(d["n_hidden"]) for d in draws]

    # ---- E1 canary + holdout at fixed config
    ev["E1"] = {}
    for name in ["S_ASB", "R_rad", "F_ASBxRAD", "F3_ASBxRADxMAG"]:
        a = float(auc_score(surfaces[name], labels, foot))
        h = holdout_for_surface(surfaces[name], draws, foot, BUDGETS_FINAL, 2)
        ev["E1"][name] = dict(auc_vs_full_catalogue=a,
                              auc_flag="LEAKAGE-SUSPECT >0.90" if a > 0.90 else "ok", **h)
        print("E1", name, json.dumps(ev["E1"][name]), flush=True)
    # same-instrument fixed-mask controls (not surfaces)
    ev["E1_controls_fixed_mask"] = {}
    for name, p in REG.items():
        if not Path(p).exists():
            ev["E1_controls_fixed_mask"][name] = "registry raster missing; NOT VERIFIED"
            continue
        m = read1(p) > 0
        r = evaluate(m, draws, foot)
        ev["E1_controls_fixed_mask"][name] = dict(
            holdout_dti_pooled=r["holdout_dti_pooled"], per_draw=r["per_draw"],
            instrument_note="Fixed catalogue-derived mask: hide-and-recover zeroes kernel credit "
                            "near hidden components it was pruned against; ranks discovery surfaces, "
                            "not flank-pruning. Live score (user prompt) is a separate evidence class.")
        print("E1 control", name, r["holdout_dti_pooled"], flush=True)

    cands = {k: v for k, v in ev["E1"].items() if k != "S_ASB"}
    best = max(cands, key=lambda k: cands[k]["holdout_dti_pooled"])
    ev["E1_best_fusion"] = best
    (ROOT / "evidence/run_rad_partial.json").write_text(json.dumps(ev, indent=2))

    # ---- E2 sweep on best fusion
    surf = surfaces[best]
    ev["E2"] = {}
    for budget, buf in [(37654, 2), (44090, 3), (30000, 2)]:
        key = f"{best}_poisson{budget}_buf{buf}"
        ev["E2"][key] = holdout_for_surface(surf, draws, foot, budget, buf)
        print("E2", key, ev["E2"][key]["holdout_dti_pooled"], flush=True)
    e2_best_key = max(ev["E2"], key=lambda k: ev["E2"][k]["holdout_dti_pooled"])
    # compare E2 configs against the E1 config of the same surface
    e1_cfg = ev["E1"][best]
    options = {f"{best}_poisson44090_buf2 (E1)": e1_cfg, **ev["E2"]}
    final_key = max(options, key=lambda k: options[k]["holdout_dti_pooled"])
    final_cfg = options[final_key]
    budget = int(final_cfg["budget"]); buf = int(final_cfg["buffer_px"])
    ev["E2_best"] = e2_best_key; ev["final_config"] = final_key
    print("FINAL CONFIG", final_key, final_cfg, flush=True)

    # ---- E3 final mask, registry lane check, write
    allowed = foot & (distance_transform_edt(~labels) > buf)
    final = poisson_thin_priority(surf, allowed, budget) & foot & ~labels
    ev["registry_check"] = {}
    rng = np.random.default_rng(81)
    samp = rng.choice(np.flatnonzero(foot), size=300000, replace=False)
    for name, p in REG.items():
        if not Path(p).exists():
            ev["registry_check"][name] = "registry raster not present locally; NOT VERIFIED"
            continue
        regm = read1(p) > 0
        corr = float(spearmanr(surf.ravel()[samp], read1(p).ravel()[samp]).statistic)
        overlap = float((distance_transform_edt(~regm)[final] <= 3).mean()) if final.any() else 0.0
        ev["registry_check"][name] = dict(surface_rank_corr_sampled=corr,
                                          dot_overlap_within_3px=overlap,
                                          lane_violation=bool(abs(corr) > 0.90 or overlap > 0.70))
        print("REG", name, ev["registry_check"][name], flush=True)
    # also check vs previously shipped ASB raster in docs/downloads
    prev = sorted((ROOT / "docs/downloads").glob("gems81-asb-*.tif"))
    for p in prev:
        regm = read1(p) > 0
        corr = float(spearmanr(surf.ravel()[samp], read1(p).ravel()[samp]).statistic)
        overlap = float((distance_transform_edt(~regm)[final] <= 3).mean()) if final.any() else 0.0
        ev["registry_check"][f"prev_shipped_{p.name[:40]}"] = dict(
            surface_rank_corr_sampled=corr, dot_overlap_within_3px=overlap,
            lane_violation=bool(abs(corr) > 0.90 or overlap > 0.70))
    if any(isinstance(v, dict) and v.get("lane_violation") for v in ev["registry_check"].values()):
        ev["verdict"] = "negative-duplicate-lane"
        (ROOT / "evidence/run_rad.json").write_text(json.dumps(ev, indent=2))
        print("DUPLICATE LANE - STOP, no TIF"); return 1

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    sha8 = hashlib.sha256(final.tobytes()).hexdigest()[:8]
    name = f"gems81-radasb-poisson{budget}-buf{buf}-{stamp}-{sha8}-zeros"
    out = ROOT / f"docs/downloads/{name}.tif"
    rep = write_submission(final, DATA / "sample_submission.tif", out, labels=labels, footprint=foot)
    dots = int(final.sum())
    note = f"GEMSDOE81 RAD-ASB rad-discordance gate poisson{budget} buf{buf} {dots} dots zeros"
    assert len(note) <= 140, len(note)
    d28_ctrl = ev["E1_controls_fixed_mask"].get("d28_base", {})
    d28_val = d28_ctrl.get("holdout_dti_pooled") if isinstance(d28_ctrl, dict) else None
    asb_val = ev["E1"]["S_ASB"]["holdout_dti_pooled"]
    cand_val = float(final_cfg["holdout_dti_pooled"])
    beats = (d28_val is not None and cand_val > d28_val) and cand_val > asb_val
    verdict = "promote" if beats else "negative"
    ev.update(final=dict(file=out.name, submission_note=note, note_len=len(note), dots=dots,
                         buffer_px=buf, budget=budget, surface=best, validator=rep,
                         elapsed_s=round(time.time() - t0, 1)), verdict=verdict)
    (ROOT / "evidence/run_rad.json").write_text(json.dumps(ev, indent=2))
    card = {
        "hypothesis": "Radiometric-ratio discordance (grad ThK x UK x UTh geometric-mean rank) gates the ASB antithetic-scarp-pair x basement-step surface: F=sqrt(rank(ASB)*rank(R)); a blind fault conduit alters radioelement ratios where a terrace/pinch-out mimic does not.",
        "mechanism": f"Label-free rank surfaces -> Poisson-disk priority thinning (min_dist 2.8px) at {budget}-dot target, catalogue exclusion buffer {buf}px, binary {{0,1}}, zeros outside footprint. Surface={best}.",
        "named_nonfault_mimic": "Lithologic contact / paleo-shoreline over a sedimentary pinch-out producing both a terrace pair and a radiometric ratio edge with no fault.",
        "holdout_DTI": {"label": "HOLDOUT-DTI", "evaluator": ev["evaluator"],
                        "candidate": cand_val, "per_draw": final_cfg["per_draw"],
                        "ci95_draw_range": final_cfg["ci95_draw_range"],
                        "n_hidden_positives_total": final_cfg["n_hidden_total"],
                        "same_instrument_controls": {
                            "ASB_S_same_config": asb_val, "d28_fixed_mask": d28_val,
                            "winner_fixed_mask": (ev["E1_controls_fixed_mask"].get("winner_h33-2-b2") or {}).get("holdout_dti_pooled"),
                            "control_note": "Fixed-mask controls are catalogue-derived; hide-and-recover mechanically penalises flank strategies (see IR-81-03). Winner 0.2778 / d28 0.2600 live scores are ORGANIZER-CONFIRMED as reported in the user prompt, a different evidence class."},
                        "canary_AUCs": {k: ev["E1"][k]["auc_vs_full_catalogue"] for k in ev["E1"]},
                        "E1_all": {k: v["holdout_dti_pooled"] for k, v in ev["E1"].items()},
                        "E2_all": {k: v["holdout_dti_pooled"] for k, v in ev["E2"].items()}},
        "correlation_overlap_vs_registry": ev["registry_check"],
        "raster_sha256": rep["sha256"], "validator": rep,
        "submission_name": name + ".tif", "submission_note": note,
        "verdict": verdict,
        "verdict_reason": ("Beats same-instrument ASB and d28 fixed-mask control on HOLDOUT-DTI v81.1; format validator all-pass."
                           if beats else
                           f"HOLDOUT-DTI {cand_val:.4f} does not beat same-instrument control(s) (ASB {asb_val:.4f}, d28 fixed-mask {d28_val}); "
                           "format-valid and downloadable, but do NOT spend a scarce weekly slot on it if maximising P(win). "
                           "No score >0.2778 is claimed; this raster is UNSCORED until an organizer receipt exists."),
    }
    (ROOT / "evidence/run_card_rad.json").write_text(json.dumps(card, indent=2))
    (ROOT / f"docs/downloads/{name}.receipt.json").write_text(json.dumps(card, indent=2))
    print(json.dumps(card, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
