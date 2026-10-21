"""GEMSDOE81 LANE (unique, preregistered in registry/hypotheses.json):
Antithetic-scarp-pair x basement-step coincidence (ASB).
A blind fault is predicted ONLY where (A) a 1 m-LiDAR crest-convexity scarplet
(lapneg) and base-concavity scarplet (lappos) co-occur in the same 100 m cell
(geometric mean -- an antithetic pair, the cross-section of a fault scarp), AND
(B) the subsurface steps there: gradient magnitude of depth_to_basement and of
conductivity coincide (geometric mean). Final S = sqrt(A_rank * B_rank), each
rank computed inside footprint only. LABEL-FREE: never reads labels/sample.
Non-fault mimic: paired terrace riser / paleo-shoreline + sedimentary pinch-out.
Differs from GEMSDOE32-H33 (orientation-order consensus across physics, dotted
Poisson on 0.2708 base), H19/H25 (multi-line corroborated ridge surfaces),
lidar-only scarps (7GEMSDOE/GEMSDOE47) and catalogue-flank pruning (winner)."""
import numpy as np, rasterio
from scipy.ndimage import gaussian_filter
def rank_unit(a, foot):
    out=np.zeros(a.shape,np.float32); v=foot&np.isfinite(a)
    vals=a[v]; order=np.argsort(vals,kind="mergesort"); r=np.empty(vals.size,np.float32)
    r[order]=np.arange(vals.size,dtype=np.float32)/max(vals.size-1,1); out[v]=r; return out
def _gradmag(a, foot, sigma=1.0):
    v=foot&np.isfinite(a); med=float(np.median(a[v])) if v.any() else 0.
    f=gaussian_filter(np.where(v,a,med).astype(np.float32),sigma,mode="nearest")
    gy,gx=np.gradient(f); return np.hypot(gx,gy)
def build(data_dir):
    foot=None; lidar={}; feats={}
    with rasterio.open(f"{data_dir}/sample_submission.tif") as ds: foot=np.isfinite(ds.read(1))
    with rasterio.open(f"{data_dir}/lidar_scarp_features_u8.tif") as ds:
        for i,name in [(4,"lapneg"),(5,"lappos"),(3,"step")]: lidar[name]=ds.read(i).astype(np.float32)
    with rasterio.open(f"{data_dir}/training_features.tif") as ds:
        for i,name in [(15,"depth_base"),(17,"cond"),(12,"det_elev")]: feats[name]=ds.read(i)
    for k in feats: feats[k][feats[k]<-1e38]=np.nan
    A=np.sqrt(rank_unit(lidar["lapneg"],foot)*rank_unit(lidar["lappos"],foot))* (0.5+0.5*rank_unit(lidar["step"],foot))
    B=np.sqrt(rank_unit(_gradmag(feats["depth_base"],foot),foot)*rank_unit(_gradmag(feats["cond"],foot),foot))
    S=np.sqrt(rank_unit(A,foot)*rank_unit(B,foot)).astype(np.float32); S[~foot]=0.
    comps=dict(A_pair_scarp=A, B_basement_step=B,
               lapneg_only=rank_unit(lidar["lapneg"],foot),
               depthbase_grad_only=rank_unit(_gradmag(feats["depth_base"],foot),foot))
    return S, comps, foot
