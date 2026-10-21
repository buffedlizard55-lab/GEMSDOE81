#!/usr/bin/env python3
"""E2: hide-and-recover HOLDOUT-DTI v81.1 (same instrument/seeds as ASB session).
Per-draw: catalogue exclusion (buf 2px) derived from VISIBLE faults only;
visible masked pixel-exactly. Fixed rasters (d28/winner/ASB-shipped) evaluated
as-is controls. Pooled over 2 draws; CI = per-draw range (n=2, disclosed)."""
import json, sys, time
import numpy as np, rasterio
from pathlib import Path
from scipy.ndimage import distance_transform_edt
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from gems81.surface import rank_unit
from gems81.holdout import make_draws
from gems81.emission import poisson_thin_priority
from gems81.metric import dti_binary, dti_from_components

t0 = time.time()
with rasterio.open(ROOT / "data/sample_submission.tif") as ds: foot = np.isfinite(ds.read(1))
with rasterio.open(ROOT / "data/labels.tif") as ds: labels = (ds.read(1) > 0) & foot
draws = make_draws(labels, foot)
print("hidden per draw:", [d["n_hidden"] for d in draws], flush=True)

def pooled(masks):
    TP = FP = FN = 0.0; per = []
    for m, d in zip(masks, draws):
        r = dti_binary(m & ~d["visible"], d["hidden"], valid=foot, known=d["visible"])
        per.append(float(r["dti"])); TP += r["tp"]; FP += r["fp"]; FN += r["fn"]
    return dict(holdout_dti_pooled=float(dti_from_components(TP, FP, FN)), per_draw=per,
                ci95_draw_range=[min(per), max(per)],
                n_hidden_total=int(sum(d["n_hidden"] for d in draws)))

def emit_per_draw(S, n, buf=2):
    ms = []
    for d in draws:
        allowed = foot & (distance_transform_edt(~d["visible"]) > buf)
        ms.append(poisson_thin_priority(S, allowed, n) & foot)
    return ms

def fixed(p):
    with rasterio.open(p) as ds: a = ds.read(1)
    m = (np.nan_to_num(a) > 0) & foot
    return [m, m]

S = {k: np.load(f"/tmp/{k}.npy") for k in ["RXF_ratio_front", "GMD_concord", "PCD_piedmont", "ASB_control_rebuilt"]}
S["PGX_piedmont_x_gravmag"] = np.sqrt(rank_unit(S["PCD_piedmont"], foot) * rank_unit(S["GMD_concord"], foot)).astype(np.float32)
np.save("/tmp/PGX_piedmont_x_gravmag.npy", S["PGX_piedmont_x_gravmag"])
from gems81.holdout import auc_score
print("PGX canary AUC:", float(auc_score(S["PGX_piedmont_x_gravmag"], labels, foot)), flush=True)

ev = {"evaluator": "HOLDOUT-DTI v81.1 pooled alpha0.2 beta0.8 300m triangular, 2 draws whole-components, buf2 from visible only"}
for name in ["PGX_piedmont_x_gravmag", "PCD_piedmont", "GMD_concord", "RXF_ratio_front", "ASB_control_rebuilt"]:
    ev[name + "_poisson44090_buf2"] = pooled(emit_per_draw(S[name], 44090))
    print(name, ev[name + "_poisson44090_buf2"], f"{time.time()-t0:.0f}s", flush=True)
    (ROOT / "evidence/e2_holdout_81b.json").write_text(json.dumps(ev, indent=2))
best = max((k for k in ev if k.endswith("44090_buf2")), key=lambda k: ev[k]["holdout_dti_pooled"])
ev["best_44090"] = best
bname = best.replace("_poisson44090_buf2", "")
ev[bname + "_poisson37654_buf2"] = pooled(emit_per_draw(S[bname], 37654))
print("best@37654", bname, ev[bname + "_poisson37654_buf2"], flush=True)
ev["control_d28_as_is"] = pooled(fixed("/tmp/reg81/d28.tif"))
ev["control_winner_h33_as_is"] = pooled(fixed("/tmp/reg81/winner.tif"))
ev["control_ASB_shipped_as_is"] = pooled(fixed(ROOT / "docs/downloads/gems81-asb-poisson44090-buf2-20261021T221522Z-1a12c8f1-zeros.tif"))
print("controls:", {k: ev[k]["holdout_dti_pooled"] for k in ev if k.startswith("control")}, flush=True)
(ROOT / "evidence/e2_holdout_81b.json").write_text(json.dumps(ev, indent=2))
print(json.dumps(ev, indent=2))
