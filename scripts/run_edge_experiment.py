#!/usr/bin/env python3
"""Experiment 2: EDGE consensus + EDGE x ASB fusion, same holdout instrument/config
as run_rad_experiment.py (poisson44090 buf2, HOLDOUT-DTI v81.1, 2 draws).
Outputs evidence/run_edge.json only; final writing is done by finalize_rad_submission.py
which picks the best-holdout NEW surface across experiments."""
import json, sys, time
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "vendor"))
from gems81.surface import rank_unit
from gems81.surface_edge import build_edge
from gems81.holdout import make_draws, auc_score
from gems81.emission import poisson_thin_priority
from gems81.metric import dti_binary, dti_from_components

DATA = ROOT / "data"


def read1(p):
    with rasterio.open(p) as ds:
        return ds.read(1)


def hold(surf, draws, foot, budget=44090, buf=2):
    TP = FP = FN = 0.0; per = []
    for d in draws:
        allowed = foot & (distance_transform_edt(~d["visible"]) > buf)
        m = poisson_thin_priority(surf, allowed, budget) & ~d["visible"]
        r = dti_binary(m, d["hidden"], valid=foot, known=d["visible"])
        per.append(float(r["dti"])); TP += r["tp"]; FP += r["fp"]; FN += r["fn"]
    return dict(holdout_dti_pooled=float(dti_from_components(TP, FP, FN)), per_draw=per,
                ci95_draw_range=[float(min(per)), float(max(per))],
                n_hidden_total=int(sum(int(d["n_hidden"]) for d in draws)), budget=budget, buffer_px=buf)


def main():
    t0 = time.time()
    with rasterio.open(DATA / "sample_submission.tif") as ds:
        foot = np.isfinite(ds.read(1))
    labels = (read1(DATA / "labels.tif") > 0) & foot
    E, names = build_edge(DATA, foot)
    np.save("/tmp/E_EDGE.npy", E)
    S = np.load("/tmp/S_ASB.npy") if Path("/tmp/S_ASB.npy").exists() else None
    if S is None:
        from gems81.surface import build as build_asb
        S, _, _ = build_asb(DATA)
    F_EX = np.sqrt(rank_unit(E, foot) * rank_unit(S, foot)).astype(np.float32)
    np.save("/tmp/F_EX.npy", F_EX)
    draws = make_draws(labels, foot)
    out = {"evaluator": "HOLDOUT-DTI v81.1 pooled alpha=0.2 beta=0.8 300m triangular, 2 draws, visible masked",
           "edge_planes": names, "surfaces": {}}
    for nm, surf in [("EDGE", E), ("F_EDGExASB", F_EX)]:
        a = float(auc_score(surf, labels, foot))
        h = hold(surf, draws, foot)
        out["surfaces"][nm] = dict(auc_vs_full_catalogue=a,
                                   auc_flag="LEAKAGE-SUSPECT >0.90" if a > 0.90 else "ok", **h)
        print(nm, json.dumps(out["surfaces"][nm]), flush=True)
    out["elapsed_s"] = round(time.time() - t0, 1)
    (ROOT / "evidence/run_edge.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
