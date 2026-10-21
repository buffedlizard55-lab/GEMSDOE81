"""Submission writer + validator v81.1. FAILS CLOSED: writes only if every check passes.
Guarantees DrivenData acceptance on format grounds: single-band float32, CRS/shape/
transform copied from sample_submission.tif, finite values in [0,1] EVERYWHERE
(zeros outside footprint -- not NaN, fixing the reported 'values must be in range
[0, 1]' rejection, which NaN-outside files can trigger)."""
import hashlib, json
import numpy as np, rasterio
def sha256_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def validate(path, template_path, labels=None, footprint=None):
    with rasterio.open(template_path) as t, rasterio.open(path) as ds:
        a=ds.read(1); checks={
          "single_band": ds.count==1, "dtype_float32": ds.dtypes==('float32',),
          "shape_match": (ds.height,ds.width)==(t.height,t.width),
          "crs_match": str(ds.crs)==str(t.crs), "transform_match": tuple(ds.transform)==tuple(t.transform),
          "no_nan_anywhere": bool(np.isfinite(a).all()), "no_inf_anywhere": bool(np.isfinite(a).all()),
          "values_in_0_1_everywhere": bool(a.min()>=0.0 and a.max()<=1.0),
          "binary_values": bool(set(np.unique(a).tolist())<= {0.0,1.0})}
        info=dict(shape=[ds.height,ds.width],crs=str(ds.crs),transform=list(ds.transform),
                  dtype=ds.dtypes[0],positive_pixels=int((a>0).sum()),min=float(a.min()),max=float(a.max()))
    if labels is not None: checks["zero_on_catalogue"]=bool((a[np.asarray(labels)>0]==0).all())
    if footprint is not None: checks["zero_outside_footprint"]=bool((a[~footprint]==0).all())
    checks["all_passed"]=bool(all(checks.values())); return {**info,"checks":checks,"sha256":sha256_file(path)}
def write_submission(mask, template_path, out_path, labels=None, footprint=None):
    mask=np.asarray(mask,bool)
    with rasterio.open(template_path) as t: prof=t.profile.copy()
    if footprint is not None: mask=mask&footprint
    if labels is not None: mask=mask&(np.asarray(labels)<=0)
    arr=mask.astype(np.float32)
    if not (np.isfinite(arr).all() and arr.min()>=0 and arr.max()<=1): raise ValueError("range violation pre-write")
    prof.update(driver="GTiff",count=1,dtype="float32",nodata=None,compress="deflate",predictor=2)
    with rasterio.open(out_path,"w",**prof) as ds: ds.write(arr,1)
    rep=validate(out_path, template_path, labels=labels, footprint=footprint)
    if not rep["checks"]["all_passed"]: raise ValueError(f"validator failed: {rep}")
    return rep
