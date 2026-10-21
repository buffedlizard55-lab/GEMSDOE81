#!/usr/bin/env python3
"""E1 canary: AUC of every candidate transform alone vs catalogue (AUC>0.90 = leakage stop)."""
import json, sys
import numpy as np, rasterio
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from gems81.surfaces81b import build_all
from gems81.surface import build as build_asb
from gems81.holdout import auc_score

surfs, foot = build_all(ROOT / "data")
S_asb, comps_asb, _ = build_asb(ROOT / "data")
surfs["ASB_control_rebuilt"] = S_asb
surfs["ASB_A_pair_scarp"] = comps_asb["A_pair_scarp"]
with rasterio.open(ROOT / "data/labels.tif") as ds:
    labels = (ds.read(1) > 0) & foot
res = {}
for name, s in surfs.items():
    a = float(auc_score(s, labels, foot))
    res[name] = dict(auc=a, flag="LEAKAGE>0.90 STOP" if a > 0.90 else "ok")
    print(f"{name:26s} AUC={a:.4f} {res[name]['flag']}", flush=True)
keep = ["RXF_ratio_front", "GMD_discord", "GMD_concord", "PCD_piedmont", "ASB_control_rebuilt"]
for k in keep:
    np.save(f"/tmp/{k}.npy", surfs[k].astype(np.float32))
(ROOT / "evidence/e1_canary_81b.json").write_text(json.dumps(res, indent=2))
print("saved surfaces:", keep)
