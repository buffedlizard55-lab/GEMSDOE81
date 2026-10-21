"""EXPLORATORY (E1/E2) runner - superseded by scripts/finalize_submission.py for the shipped raster; exact greedy noted in IR-81-04."""
#!/usr/bin/env python3
"""3 experiments max (budget rule): E1 canary, E2 emission/budget, E3 final+registry."""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np, rasterio
from scipy.ndimage import distance_transform_edt
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from gems81.surface import build
from gems81.holdout import make_draws, evaluate, auc_score
from gems81.emission import batch_greedy_cover as greedy_cover, poisson_thin_priority
from gems81.submission_writer import write_submission, sha256_file
from gems81.metric import dti_binary
DATA=ROOT/"data"; REGISTRY_TIFS={
 "winner_h33-2-b2_0.2778":"/tmp/g32/docs/downloads/gemsdoe32-h33-h33-2-b2-20261004T220000Z-e5eb6e7e-zeros.tif",
 "d28_base_0.2600":"/tmp/g32/docs/downloads/gems25-dotted-h19-5-d2-8-20261002-e56ea318af89-zeros.tif"}
def read1(p):
    with rasterio.open(p) as ds: return ds.read(1)
def main():
    t0=time.time(); ev={"evaluator":"HOLDOUT-DTI v81.1 pooled alpha0.2 beta0.8 300m triangular, 2 draws x20% whole-components hidden"}
    S,comps,foot=build(DATA)
    labels=(read1(DATA/"labels.tif")>0)&foot
    draws=make_draws(labels,foot)
    ev["n_hidden_per_draw"]=[d["n_hidden"] for d in draws]
    def allowed_for(vis,buf): return foot & (distance_transform_edt(~vis)>buf)
    def hold(mask_fn):
        ms=[]
        for d in draws: ms.append(mask_fn(allowed_for(d["visible"],mask_fn.buf))&~d["visible"])
        # pooled via per-draw masks: evaluate() expects one mask; do manual pooling
        from gems81.metric import dti_from_components
        TP=FP=FN=0.; per=[]
        for m,d in zip(ms,draws):
            r=dti_binary(m,d["hidden"],valid=foot,known=d["visible"]); per.append(r["dti"]); TP+=r["tp"];FP+=r["fp"];FN+=r["fn"]
        # bootstrap 95% CI over hidden components is costly; report draw-cell CI via per-draw spread + pooled
        return dict(holdout_dti_pooled=dti_from_components(TP,FP,FN),per_draw=per,
                    ci95_note="per-draw range shown; n_draws=2 so CI is draw-range, not component bootstrap",
                    ci95=[float(min(per)),float(max(per))],n_hidden_total=int(sum(d["n_hidden"] for d in draws)))
    # E1 canary: AUC alone + holdout at 37654 poisson
    ev["E1_canary"]={}
    for name,surf in comps.items():
        a=auc_score(surf,labels,foot)
        def mf(allowed,s=surf): return poisson_thin_priority(s,allowed,37654)
        mf.buf=2; h=hold(mf)
        ev["E1_canary"][name]=dict(auc_vs_full_catalogue=float(a),auc_flag="LEAKAGE if >0.90" if a>0.90 else "ok",**h)
        print("E1",name,ev["E1_canary"][name],flush=True)
    def mfS(allowed): return poisson_thin_priority(S,allowed,37654)
    mfS.buf=2; ev["E1_canary"]["S_combined"]=dict(auc_vs_full_catalogue=float(auc_score(S,labels,foot)),**hold(mfS))
    print("E1 S",ev["E1_canary"]["S_combined"],flush=True)
    # E2 budgets/emitters/buffer on S
    ev["E2"]={}
    for budget in (20000,37654,44090):
        def mf(allowed,b=budget): return poisson_thin_priority(S,allowed,b)
        mf.buf=2; ev["E2"][f"poisson_b{budget}_buf2"]=hold(mf); print("E2",budget,ev["E2"][f"poisson_b{budget}_buf2"],flush=True)
    def mfg(allowed): return greedy_cover(S,foot,allowed,37654)
    mfg.buf=2; ev["E2"]["greedy_b37654_buf2"]=hold(mfg); print("E2 greedy",ev["E2"]["greedy_b37654_buf2"],flush=True)
    def mf3(allowed): return poisson_thin_priority(S,allowed,37654)
    mf3.buf=3; ev["E2"]["poisson_b37654_buf3"]=hold(mf3); print("E2 buf3",ev["E2"]["poisson_b37654_buf3"],flush=True)
    best_name=max(ev["E2"],key=lambda k:ev["E2"][k]["holdout_dti_pooled"])
    ev["E2_best"]=best_name; (ROOT/"evidence/run_partial.json").write_text(json.dumps(ev,indent=2)); print("BEST",best_name,flush=True)
    # E3 final mask with FULL catalogue (visible=all labels for final)
    buf=3 if "buf3" in best_name else 2; budget=int(best_name.split("_b")[1].split("_")[0]) if "_b" in best_name else 37654
    allowed=foot&(distance_transform_edt(~labels)>buf)
    final=greedy_cover(S,foot,allowed,budget) if best_name.startswith("greedy") else poisson_thin_priority(S,allowed,budget)
    final&=foot&~labels
    # registry lane check: rank corr (sampled footprint) + dot overlap within 3px
    ev["registry_check"]={}
    rng=np.random.default_rng(81); fidx=np.flatnonzero(foot)
    samp=rng.choice(fidx,size=300000,replace=False)
    from scipy.stats import spearmanr
    for name,p in REGISTRY_TIFS.items():
        if not Path(p).exists(): ev["registry_check"][name]="registry raster not present locally; NOT VERIFIED"; continue
        reg=read1(p); regmask=reg>0
        corr=float(spearmanr(S.ravel()[samp],reg.ravel()[samp]).statistic) if regmask.any() else 0.
        d=distance_transform_edt(~regmask); overlap=float((d[final]<=3).mean()) if final.any() else 0.
        ev["registry_check"][name]=dict(surface_rank_corr_sampled=corr,dot_overlap_within_3px=float(overlap),
            lane_violation=bool(abs(corr)>0.90 or overlap>0.70))
        print("REG",name,ev["registry_check"][name],flush=True)
    if any(isinstance(v,dict) and v.get("lane_violation") for v in ev["registry_check"].values()):
        ev["verdict"]="negative-duplicate-lane"; (ROOT/"evidence/run.json").write_text(json.dumps(ev,indent=2)); print("DUPLICATE LANE - STOP"); return 1
    stamp=time.strftime("%Y%m%dT%H%M%SZ",time.gmtime()); sha8=hashlib.sha256(final.tobytes()).hexdigest()[:8]
    name=f"gems81-asb-{best_name}-{stamp}-{sha8}-zeros"
    out=ROOT/f"docs/downloads/{name}.tif"; out.parent.mkdir(parents=True,exist_ok=True)
    rep=write_submission(final,DATA/"sample_submission.tif",out,labels=labels,footprint=foot)
    note=f"GEMSDOE81 ASB scarp-pair x basement-step {best_name} {int(final.sum())} dots buf{buf}px zeros-outside"
    assert len(note)<=140, len(note)
    ev.update(final=dict(file=out.name,submission_note=note,note_len=len(note),dots=int(final.sum()),
        buffer_px=buf,budget=budget,emitter=best_name,validator=rep,elapsed_s=round(time.time()-t0,1)),
        verdict="promote" if ev["E2"][best_name]["holdout_dti_pooled"]>max(v["holdout_dti_pooled"] for k,v in ev["E1_canary"].items() if k!="S_combined") else "promote-best-available (see run card; holdout-best config)")
    (ROOT/"evidence/run.json").write_text(json.dumps(ev,indent=2))
    card=dict(hypothesis="Antithetic LiDAR scarp-pair coincides with basement/conductivity step (ASB)",
      mechanism="sqrt(rank geometric-mean lapneg*lappos) x sqrt(rank grad(depth_to_basement)*grad(conductivity)); greedy/poisson kernel-cover emission",
      named_nonfault_mimic="paired terrace riser / paleo-shoreline over a sedimentary pinch-out",
      holdout_dti=ev["E2"][best_name],correlation_overlap_vs_registry=ev["registry_check"],
      raster_sha256=rep["sha256"],validator=rep,submission_name=name+".tif",submission_note=note,verdict=ev["verdict"])
    (ROOT/"evidence/run_card.json").write_text(json.dumps(card,indent=2))
    print(json.dumps(card,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
