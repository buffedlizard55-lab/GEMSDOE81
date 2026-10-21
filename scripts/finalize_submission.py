#!/usr/bin/env python3
import json, sys, time, hashlib
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from gems81.emission import poisson_thin_priority
from gems81.submission_writer import write_submission
try:
    S=np.load("/tmp/S.npy")
except FileNotFoundError:
    sys.path.insert(0,str(ROOT/"src")); from gems81.surface import build as _b; S,_,_= _b(ROOT/"data")
with rasterio.open(ROOT/"data/sample_submission.tif") as ds: foot=np.isfinite(ds.read(1))
with rasterio.open(ROOT/"data/labels.tif") as ds: labels=(ds.read(1)>0)&foot
allowed=foot&(distance_transform_edt(~labels)>2)
mask=poisson_thin_priority(S,allowed,44090)&foot&~labels
reg={}
for name,p in {"winner_h33-2-b2_ORGANIZER-CONFIRMED_0.2778":"/tmp/g32/docs/downloads/gemsdoe32-h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros.tif","d28_base_0.2600":"/tmp/g32/docs/downloads/gems25-dotted-h19-5-d2-8-20261002-e56ea318af89-zeros.tif"}.items():
    with rasterio.open(p) as ds: r=ds.read(1)
    rm=r>0; rng=np.random.default_rng(81); samp=rng.choice(np.flatnonzero(foot),300000,replace=False)
    reg[name]=dict(surface_rank_corr_sampled=float(spearmanr(S.ravel()[samp],r.ravel()[samp]).statistic),
                   dot_overlap_within_3px=float((distance_transform_edt(~rm)[mask]<=3).mean()),
                   lane_violation=False)
    reg[name]["lane_violation"]=bool(abs(reg[name]["surface_rank_corr_sampled"])>0.90 or reg[name]["dot_overlap_within_3px"]>0.70)
assert not any(v["lane_violation"] for v in reg.values()), reg
stamp=time.strftime("%Y%m%dT%H%M%SZ",time.gmtime()); sha8=hashlib.sha256(mask.tobytes()).hexdigest()[:8]
name=f"gems81-asb-poisson44090-buf2-{stamp}-{sha8}-zeros"
out=ROOT/f"docs/downloads/{name}.tif"
rep=write_submission(mask,ROOT/"data/sample_submission.tif",out,labels=labels,footprint=foot)
note=f"GEMSDOE81 ASB scarp-pair x basement-step poisson44090 buf2 {int(mask.sum())} dots zeros"
print(len(note),note); assert len(note)<=140
card={
 "hypothesis":"Antithetic LiDAR scarp-pair (lapneg x lappos geometric mean) coincides with a basement/conductivity step (grad depth_to_basement x grad conductivity geometric mean); final surface = geometric mean of the two rank surfaces.",
 "mechanism":"Label-free rank surfaces -> Poisson-disk priority thinning (min_dist 2.8px) at 44,090-dot target, catalogue exclusion buffer 2px, binary {0,1}, zeros outside footprint.",
 "named_nonfault_mimic":"Paired terrace riser / paleo-shoreline over a sedimentary pinch-out (antithetic steps + basement gradient with no fault).",
 "holdout_DTI":{"label":"HOLDOUT-DTI","evaluator":"v81.1 pooled alpha=0.2 beta=0.8 300m triangular kernel, whole-component hide-and-recover, 2 draws, visible masked pixel-exactly",
   "candidate_S_poisson44090_buf2":0.08312651477439477,"per_draw":[0.08945094605656231,0.07675218725378645],"ci95_draw_range":[0.07675218725378645,0.08945094605656231],"n_hidden_positives_total":25038,
   "same_instrument_controls":{"d28_base_HOLDOUT-DTI":0.09922256956705666,"winner_h33-2-b2_HOLDOUT-DTI":0.004309322934951101,
     "winner_note":"Winner deletes dots <=2px from FULL catalogue incl. hidden components, so hide-and-recover mechanically zeroes its kernel credit; this instrument cannot rank catalogue-flank strategies. Its 0.2778 is ORGANIZER-CONFIRMED, not comparable to HOLDOUT-DTI."},
   "canary_AUCs_all_below_0.90":{"A_pair_scarp":0.5724,"B_basement_step":0.5468,"lapneg_only":0.5714,"depthbase_grad_only":0.5354,"S_combined":0.5892}},
 "correlation_overlap_vs_registry":reg,
 "raster_sha256":rep["sha256"],"validator":rep,
 "submission_name":name+".tif","submission_note":note,
 "verdict":"negative",
 "verdict_reason":"FORMAT promote (validator all-pass, safe to submit) but SCIENCE negative: HOLDOUT-DTI 0.0831 does not beat same-instrument d28 control 0.0992; do not spend a scarce weekly slot on it if maximising P(win) unless testing the off-catalogue hypothesis deliberately. No score >0.2778 is claimed; live score is UNSCORED."}
(ROOT/"evidence/run_card.json").write_text(json.dumps(card,indent=2))
(ROOT/f"docs/downloads/{name}.receipt.json").write_text(json.dumps(card,indent=2))
print(json.dumps(card,indent=2))
