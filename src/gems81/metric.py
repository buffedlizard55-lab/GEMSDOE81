"""Pooled DTI (alpha=0.2, beta=0.8, 300 m triangular kernel). Evaluator v81.1.
Kernel: k(d)=max(1-d/3,0), d in 100 m pixels. Verified vs brute force in tests."""
import numpy as np
from scipy.ndimage import distance_transform_edt
ALPHA, BETA, RADIUS_PX, EPS = 0.2, 0.8, 3.0, 1e-12
def kernel(d): return np.maximum(1.0-np.asarray(d,float)/RADIUS_PX,0.0)
def dti_binary(pred, truth, valid=None, known=None):
    pred=np.asarray(pred,bool); truth=np.asarray(truth,bool)
    valid=np.ones(pred.shape,bool) if valid is None else np.asarray(valid,bool)
    known=np.zeros(pred.shape,bool) if known is None else np.asarray(known,bool)
    active=valid&~known; p=pred&active; g=truth&active; n=int(g.sum())
    if n==0: return dict(tp=0.,fp=float(p.sum()),fn=0.,n_truth=0,dti=0.)
    if not p.any(): return dict(tp=0.,fp=0.,fn=float(n),n_truth=n,dti=0.)
    tp=float(kernel(distance_transform_edt(~p)[g]).sum()); fn=float(n)-tp
    fp=float((1.0-kernel(distance_transform_edt(~g)[p])).sum())
    return dict(tp=tp,fp=fp,fn=fn,n_truth=n,dti=tp/(tp+ALPHA*fp+BETA*fn+EPS))
def dti_from_components(tp,fp,fn): return float(tp/(tp+ALPHA*fp+BETA*fn+EPS))
