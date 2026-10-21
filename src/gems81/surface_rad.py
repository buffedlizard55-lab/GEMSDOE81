"""GEMSDOE81 session-2 lane: RAD-ASB.

R  = radiometric-ratio discordance edge: geometric mean of within-footprint
     ranks of gradient-magnitude of GeoDAWN ratio grids ThK, UK, UTh
     (geodawn_extensions_u8.tif bands 1-3; USGS GeoDAWN DOI 10.5066/P93LGLVQ;
     uint8, 0 = nodata, bytes are contractor ratio grids mosaicked to this grid).
M  = magnetic step: rank of gradient-magnitude of TMI upward-continued 150 m
     (band 4).
F  = sqrt(rank(ASB) * rank(R))            -- shipped candidate surface if it wins
F3 = (rank(ASB) * rank(R) * rank(M))**(1/3) -- E1 variant only

LABEL-FREE: never reads labels. Non-fault mimic: lithologic contact /
paleo-shoreline over a sedimentary pinch-out (ratio edge + terrace pair, no fault).
"""
import numpy as np, rasterio
from scipy.ndimage import gaussian_filter
from .surface import build as build_asb, rank_unit


def _gradmag_u8(a, foot):
    v = foot & (a > 0)
    med = float(np.median(a[v])) if v.any() else 0.0
    f = gaussian_filter(np.where(v, a, med).astype(np.float32), 1.0, mode="nearest")
    gy, gx = np.gradient(f)
    return np.hypot(gx, gy), v


def build_rad(data_dir):
    S, comps, foot = build_asb(data_dir)
    with rasterio.open(f"{data_dir}/geodawn_extensions_u8.tif") as ds:
        thk = ds.read(1).astype(np.float32)
        uk = ds.read(2).astype(np.float32)
        uth = ds.read(3).astype(np.float32)
        tmi = ds.read(4).astype(np.float32)
    g_thk, v1 = _gradmag_u8(thk, foot)
    g_uk, v2 = _gradmag_u8(uk, foot)
    g_uth, v3 = _gradmag_u8(uth, foot)
    g_tmi, v4 = _gradmag_u8(tmi, foot)
    rad_valid = v1 & v2 & v3
    R = (rank_unit(g_thk, foot) * rank_unit(g_uk, foot) * rank_unit(g_uth, foot)) ** (1.0 / 3.0)
    R = rank_unit(R, foot)
    R[~rad_valid] = 0.0  # no radiometric coverage -> no discordance evidence
    M = rank_unit(g_tmi, foot)
    M[~v4] = 0.0
    s_rank = rank_unit(S, foot)
    F = np.sqrt(s_rank * R).astype(np.float32)
    F3 = (s_rank * R * M) ** (1.0 / 3.0)
    F3 = F3.astype(np.float32)
    out = dict(S_ASB=S, R_rad=R, M_mag=M, F_ASBxRAD=F, F3_ASBxRADxMAG=F3)
    out.update({f"asb_{k}": v for k, v in comps.items()})
    return out, foot, rad_valid
