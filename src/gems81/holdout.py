"""Hide-and-recover holdout v81.1: withhold whole 8-connected fault components
(20% of labelled pixels per quadrant, draws 81/82), buffer = quadrant-border
erosion is NOT applied (whole-grid scoring per draw, visible masked pixel-exactly
as `known`); every catalogue-derived operation in caller must use visible only.
Pooled DTI sums TP/FP/FN over all 8 quadrant-draw cells' parent draws (per-draw
whole-grid scores pooled over 2 draws; per-quadrant breakdown also returned)."""
import numpy as np
from scipy.ndimage import label as cc_label
from .metric import dti_binary, dti_from_components
STRUCT=np.ones((3,3),int)
def quadrant_ids(foot):
    yy,xx=np.nonzero(foot); ym,xm=int(np.median(yy)),int(np.median(xx))
    gy,gx=np.ogrid[:foot.shape[0],:foot.shape[1]]; q=np.full(foot.shape,-1,np.int8)
    q[(gy<ym)&(gx<xm)&foot]=0; q[(gy<ym)&(gx>=xm)&foot]=1; q[(gy>=ym)&(gx<xm)&foot]=2; q[(gy>=ym)&(gx>=xm)&foot]=3
    return q
def make_draws(labels, foot, seeds=(81,82), hide_frac=0.20):
    comp,n=cc_label(labels&foot, structure=STRUCT); sizes=np.bincount(comp.ravel(),minlength=n+1)
    quad=quadrant_ids(foot); draws=[]
    for s in seeds:
        hidden=np.zeros(labels.shape,bool)
        for qi in range(4):
            ids=np.unique(comp[(quad==qi)&(labels&foot)]); ids=ids[ids>0]
            rng=np.random.default_rng(1000*s+qi); perm=rng.permutation(ids)
            cum=np.cumsum(sizes[perm]); target=hide_frac*sizes[ids].sum()
            k=int(np.searchsorted(cum,target))+1; hidden|=np.isin(comp,perm[:k])
        draws.append(dict(seed=s,hidden=hidden&foot,visible=(labels&foot)&~hidden,
                          n_hidden=int((hidden&foot).sum()),quad=quad))
    return draws
def evaluate(mask, draws, foot):
    """Pooled HOLDOUT-DTI over draws; candidate must already have visible masked
    per-draw by caller for strictness -- here we also mask each draw's visible."""
    TP=FP=FN=0.; per=[]
    for d in draws:
        m=np.asarray(mask,bool)&foot&~d['visible']
        r=dti_binary(m, d['hidden'], valid=foot, known=d['visible']); per.append(r)
        TP+=r['tp']; FP+=r['fp']; FN+=r['fn']
    pooled=dti_from_components(TP,FP,FN)
    vals=np.array([r['dti'] for r in per])
    # 95% CI: normal approx over independent draws (n=2 is weak; also bootstrap cells below in runner)
    return dict(holdout_dti_pooled=pooled, per_draw=[float(v) for v in vals],
                per_draw_mean=float(vals.mean()), n_hidden_total=int(sum(r['n_truth'] for r in per)),
                tp=TP, fp=FP, fn=FN)
def auc_score(surface, truth, valid, sample=400000, seed=81):
    from scipy.stats import rankdata
    rng=np.random.default_rng(seed); idx=np.flatnonzero(valid)
    if idx.size>sample: idx=rng.choice(idx,size=sample,replace=False)
    y=truth.ravel()[idx]; x=np.asarray(surface,float).ravel()[idx]
    ok=np.isfinite(x); x,y=x[ok],y[ok]; r=rankdata(x); pos=y>0; npos=pos.sum(); nneg=(~pos).sum()
    return float((r[pos].sum()-npos*(npos+1)/2)/(npos*nneg)) if npos and nneg else float('nan')
