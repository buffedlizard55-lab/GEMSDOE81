#!/usr/bin/env python3
"""Experiment 3: fault-continuation gate.
CONT_draw = exp(-d_visible/4px) from VISIBLE faults only per draw (protocol:
catalogue features derived from visible only); final uses full catalogue.
Surfaces: CONT alone (canary), F_CONT = sqrt(rank(ASB)*rank(CONT)),
          F_CONT3 = (rank(ASB)*rank(CONT)*rank(EDGE))^(1/3) if EDGE cache exists.
Same instrument/config: HOLDOUT-DTI v81.1, poisson44090 buf2, visible masked.
Named mimic: alluvial fan channels / roads continuing a mapped lineament trend.
"""
import json, sys, time
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gems81.surface import rank_unit, build as build_asb
from gems81.holdout import make_draws, auc_score
from gems81.emission import poisson_thin_priority
from gems81.metric import dti_binary, dti_from_components

DATA = ROOT / "data"


def read1(p):
    with rasterio.open(p) as ds:
        return ds.read(1)


def main():
    t0 = time.time()
    with rasterio.open(DATA / "sample_submission.tif") as ds:
        foot = np.isfinite(ds.read(1))
    labels = (read1(DATA / "labels.tif") > 0) & foot
    S = np.load("/tmp/S_ASB.npy") if Path("/tmp/S_ASB.npy").exists() else build_asb(DATA)[0]
    E = np.load("/tmp/E_EDGE.npy") if Path("/tmp/E_EDGE.npy").exists() else None
    s_rank = rank_unit(S, foot)
    e_rank = rank_unit(E, foot) if E is not None else None
    draws = make_draws(labels, foot)
    out = {"evaluator": "HOLDOUT-DTI v81.1 pooled alpha=0.2 beta=0.8 300m triangular, 2 draws, visible masked",
           "surfaces": {}}
    acc = {}
    for nm in ["CONT", "F_CONT", "F_CONT3"]:
        if nm == "F_CONT3" and e_rank is None:
            continue
        acc[nm] = dict(TP=0.0, FP=0.0, FN=0.0, per=[], aucs=[])
    for d in draws:
        dvis = distance_transform_edt(~d["visible"])
        cont = np.exp(-dvis / 4.0).astype(np.float32)
        c_rank = rank_unit(cont, foot)
        surfs = {"CONT": cont,
                 "F_CONT": np.sqrt(s_rank * c_rank).astype(np.float32)}
        if e_rank is not None:
            surfs["F_CONT3"] = (s_rank * c_rank * e_rank) ** (1.0 / 3.0)
        # canary: AUC of each draw-surface vs HIDDEN truth, off visible
        valid = foot & ~d["visible"]
        for nm, surf in surfs.items():
            a = auc_score(surf, d["hidden"], valid)
            acc[nm]["aucs"].append(float(a))
            allowed = foot & (dvis > 2)
            m = poisson_thin_priority(surf, allowed, 44090) & ~d["visible"]
            r = dti_binary(m, d["hidden"], valid=foot, known=d["visible"])
            acc[nm]["per"].append(float(r["dti"])); acc[nm]["TP"] += r["tp"]; acc[nm]["FP"] += r["fp"]; acc[nm]["FN"] += r["fn"]
            print(nm, "draw", len(acc[nm]["per"]), r["dti"], "auc", a, flush=True)
        # stash final-draw-independent full-catalogue continuation for finalizer
    for nm, a in acc.items():
        out["surfaces"][nm] = dict(
            auc_vs_hidden_per_draw=a["aucs"],
            auc_flag="LEAKAGE-SUSPECT >0.90" if max(a["aucs"]) > 0.90 else "ok",
            holdout_dti_pooled=float(dti_from_components(a["TP"], a["FP"], a["FN"])),
            per_draw=a["per"], ci95_draw_range=[float(min(a["per"])), float(max(a["per"]))],
            n_hidden_total=int(sum(int(d["n_hidden"]) for d in draws)), budget=44090, buffer_px=2)
    # full-catalogue continuation surface for the finalizer
    dlab = distance_transform_edt(~labels)
    cont_full = np.exp(-dlab / 4.0).astype(np.float32)
    np.save("/tmp/CONT_full.npy", cont_full)
    np.save("/tmp/F_CONT_full.npy", np.sqrt(s_rank * rank_unit(cont_full, foot)).astype(np.float32))
    if e_rank is not None:
        np.save("/tmp/F_CONT3_full.npy", ((s_rank * rank_unit(cont_full, foot) * e_rank) ** (1.0 / 3.0)).astype(np.float32))
    out["elapsed_s"] = round(time.time() - t0, 1)
    (ROOT / "evidence/run_cont.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
