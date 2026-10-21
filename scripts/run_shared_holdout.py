#!/usr/bin/env python3
"""Reconciliation revalidation on the PINNED SHARED evaluator
(vendor/gems57, gems57-pooled-hide-v2): quadrant folds, whole segments wholly
inside a 12px-eroded domain withheld, catalogue features from visible only,
visible masked pixel-exactly, pooled DTI alpha=0.2 beta=0.8 300m triangular,
spatial-block bootstrap CI via pooled_summary (20km blocks).

Arms (per-cell emission, budget scaled by fold-domain area, buf2, poisson):
  ASB   = shipped session-1 surface (control surface)
  CONT  = exp(-d_visible/4px) alone
  F_CONT= sqrt(rank(ASB)*rank(CONT))  (candidate)
Fixed-mask controls (d28, winner) are scored as-is per cell; they were built
with the full catalogue, so this instrument penalises them (known bias).
Modes: 'all' (primary) and 'detached' (conservative live-analogue: withheld
segments >=4px from every other component, continuation cannot help by
construction). No private evaluator is used anywhere here.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.ndimage import distance_transform_edt, binary_erosion

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "vendor"))
from gems57.grid import load_grid
from gems57.holdout import build_holdout, quadrant_ids, DOMAIN_ERODE
from gems57.evaluate_holdout import evaluate as eval_terms, pooled_summary, VERSION
from gems81.emission import poisson_thin_priority
from gems81.surface import rank_unit

TOTAL_BUDGET = 44090


def read1(p):
    import rasterio
    with rasterio.open(p) as ds:
        return ds.read(1)


def main():
    t0 = time.time()
    grid = load_grid()
    foot, cat = grid.footprint, grid.catalogue
    ctx = build_holdout(grid)
    print(f"cells: {len(ctx.cells)}", [c.key for c in ctx.cells][:4], flush=True)
    S = np.load("/tmp/S_ASB.npy") if Path("/tmp/S_ASB.npy").exists() else None
    if S is None:
        from gems81.surface import build as build_asb
        S, _, _ = build_asb(ROOT / "data")
    s_rank = rank_unit(S, foot)
    quad = quadrant_ids(foot)

    arms = ["ASB", "CONT", "F_CONT"]
    terms = {mode: {a: None for a in arms} for mode in ("all", "detached")}
    pooled = {mode: {a: dict(tp=0.0, fp=0.0, fn=0.0, n=0) for a in arms} for mode in ("all", "detached")}
    fixed = {}
    fixed_masks = {}
    for nm, p in [("d28_fixed", "/tmp/reg/d28.tif"), ("winner_fixed", "/tmp/reg/winner.tif")]:
        if Path(p).exists():
            fixed_masks[nm] = read1(p) > 0
            fixed[nm] = {mode: dict(tp=0.0, fp=0.0, fn=0.0, n=0) for mode in ("all", "detached")}

    for cell in ctx.cells:
        mode = cell.mode
        visible = ctx.visible(cell.key)
        hidden = ctx.hidden_by_cell[cell.key]
        domain = binary_erosion(quad == cell.fold, iterations=DOMAIN_ERODE) & foot
        budget = int(round(TOTAL_BUDGET * domain.sum() / foot.sum()))
        sl = cell.bbox
        dvis = distance_transform_edt(~visible)
        cont_rank = rank_unit(np.exp(-dvis / 4.0).astype(np.float32), foot)
        surfs = {"ASB": S, "CONT": np.exp(-dvis / 4.0).astype(np.float32),
                 "F_CONT": np.sqrt(s_rank * cont_rank).astype(np.float32)}
        fold = {"region": domain, "truth": hidden, "visible": visible, "masked_known": visible}
        for a in arms:
            allowed = foot & (dvis > 2)
            # emit on the cropped bbox for speed; score on the full grid
            m_crop = poisson_thin_priority(surfs[a][sl], allowed[sl], budget)
            m = np.zeros(foot.shape, bool); m[sl] = m_crop
            r, tm = eval_terms(m.astype(np.float32), fold, foot)
            terms[mode][a] = tm if terms[mode][a] is None else terms[mode][a] + tm
            P = pooled[mode][a]; P["tp"] += r["tp"]; P["fp"] += r["fp"]; P["fn"] += r["fn"]; P["n"] += r["n_truth"]
        for nm, fm in fixed_masks.items():
            r, _ = eval_terms(fm.astype(np.float32), fold, foot)
            P = fixed[nm][mode]; P["tp"] += r["tp"]; P["fp"] += r["fp"]; P["fn"] += r["fn"]; P["n"] += r["n_truth"]
        print(cell.key, "budget", budget, "done", round(time.time() - t0, 1), flush=True)

    def dti(P):
        return float(P["tp"] / (P["tp"] + 0.2 * P["fp"] + 0.8 * P["fn"] + 1e-12))

    out = {"evaluator": VERSION, "instrument": "shared gems57 quadrant segment holdout, DOMAIN_ERODE=12, modes all+detached, seeds (20,21)",
           "pooled_by_mode": {}, "fixed_mask_controls": {}, "bootstrap": {}}
    for mode in ("all", "detached"):
        out["pooled_by_mode"][mode] = {a: dict(dti=dti(pooled[mode][a]), n_truth=int(pooled[mode][a]["n"])) for a in arms}
        try:
            summ = pooled_summary(terms[mode], candidate="F_CONT")
            out["bootstrap"][mode] = {k: v for k, v in summ.items() if isinstance(v, dict)}
        except Exception as e:  # disclosed, not hidden
            out["bootstrap"][mode] = {"error": f"{type(e).__name__}: {e}"}
    for nm in fixed:
        out["fixed_mask_controls"][nm] = {mode: dict(dti=dti(fixed[nm][mode]), n_truth=int(fixed[nm][mode]["n"])) for mode in fixed[nm]}
    out["elapsed_s"] = round(time.time() - t0, 1)
    (ROOT / "evidence/run_shared_holdout.json").write_text(json.dumps(out, indent=2, default=str))
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
