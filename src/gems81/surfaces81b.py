"""GEMSDOE81 session-2 candidate surfaces (see docs/hypotheses-81b.md).
Label-free rank surfaces. Bands verified from file metadata 2026-10-21:
training_features: 2 rtp, 3 tmi_hg, 6 tc, 11 iso_grav_vg, 12 det_elev,
13 iso_grav_anom, 18 iso_grav_hg, 19 det_elev_slope (15 depth_base, 17 cond
are the ASB lane's, not used here). geodawn_extensions_u8: 1 ThK 2 UK 3 UTh
4 TMI_up150. geodawn_rad_u8: 1 K 2 Th 3 U 4 TC. u8 nodata=0 -> NaN.
"""
import numpy as np, rasterio
from scipy.ndimage import gaussian_filter, laplace
from .surface import rank_unit, _gradmag

def _band(path, i, u8=False):
    with rasterio.open(path) as ds:
        a = ds.read(i).astype(np.float32)
    if u8:
        a[a <= 0] = np.nan
    else:
        a[a < -1e38] = np.nan
    return a

def _fill(a, foot, sigma=1.0):
    v = foot & np.isfinite(a)
    med = float(np.median(a[v])) if v.any() else 0.0
    return gaussian_filter(np.where(v, a, med).astype(np.float32), sigma, mode="nearest")

def build_all(data_dir):
    with rasterio.open(f"{data_dir}/sample_submission.tif") as ds:
        foot = np.isfinite(ds.read(1))
    tf = f"{data_dir}/training_features.tif"
    ex = f"{data_dir}/geodawn_extensions_u8.tif"
    out = {}
    # --- RXF components
    g_thk = _gradmag(_band(ex, 1, True), foot)
    g_uk  = _gradmag(_band(ex, 2, True), foot)
    g_uth = _gradmag(_band(ex, 3, True), foot)
    rtp = _band(tf, 2)
    g_rtp = _gradmag(rtp, foot)
    R = (rank_unit(g_thk, foot) * rank_unit(g_uk, foot) * rank_unit(g_uth, foot)) ** (1/3)
    out["RXF_ratio_front"] = np.sqrt(rank_unit(R, foot) * rank_unit(g_rtp, foot)).astype(np.float32)
    out["ratio_grad_only"] = rank_unit(R, foot)
    out["grad_rtp_only"] = rank_unit(g_rtp, foot)
    out["tmi_hg_direct"] = rank_unit(np.abs(_band(tf, 3)), foot)
    out["tc_direct"] = rank_unit(np.abs(_band(tf, 6)), foot)
    out["grad_TMIup150"] = rank_unit(_gradmag(_band(ex, 4, True), foot), foot)
    # --- GMD components
    g_grav = _gradmag(_band(tf, 13), foot)
    rg, rm = rank_unit(g_grav, foot), rank_unit(g_rtp, foot)
    out["GMD_discord"] = (rg * (1.0 - rm)).astype(np.float32)
    out["GMD_concord"] = np.sqrt(rg * rm).astype(np.float32)
    out["grad_grav_only"] = rg
    out["iso_grav_hg_direct"] = rank_unit(np.abs(_band(tf, 18)), foot)
    # --- PCD components
    de = _fill(_band(tf, 12), foot)
    slope = _band(tf, 19)
    lap = np.abs(laplace(de))
    g_slope = _gradmag(slope, foot)
    r_slope = rank_unit(np.abs(slope), foot)
    pcd = np.sqrt(rank_unit(lap, foot) * rank_unit(g_slope, foot)) * (0.5 + 0.5 * (1.0 - r_slope))
    out["PCD_piedmont"] = pcd.astype(np.float32)
    out["lap_detelev_only"] = rank_unit(lap, foot)
    # --- smooth-field canaries (informational only)
    out["geod_2ndinv"] = rank_unit(_band(tf, 4), foot)
    out["ieq_density"] = rank_unit(_band(tf, 16), foot)
    for k in out:
        out[k][~foot] = 0.0
    return out, foot
