"""Experiment 2: multi-method edge-consensus surface (EDGE).

Rationale: the strongest live family (h19-5 multiline-corroborated, 0.1922
user-reported; its dotted d28 derivative 0.2600, winner prune 0.2778) corroborates
a fault across independent edge detectors rather than trusting one physics.
EDGE = geometric mean of within-footprint ranks of independent edge planes:
  lidar (USGS 3DEP, lidar_scarp_features_u8): ex_max(1), step_max(3),
    lapneg_max(4), lappos_max(5), downface_max(6), upface_max(7)
  template cached geophysics (vendor/gems57/geo.py planes from
    training_features.tif): g_tmi_hg, g_tc, g_slope, g_grav_hg, g_curv,
    g_base_edge  (robust-z planes, rank-transformed here)
Non-fault mimic: road cuts / terrace risers / lithologic contacts that are
edges in several detectors at once (e.g. a basalt flow margin).
LABEL-FREE. Differs from ASB (pair x basement-step only) and RAD (ratio gate).
"""
import numpy as np, rasterio
from .surface import rank_unit

LIDAR_BANDS = [1, 3, 4, 5, 6, 7]  # ex, step, lapneg, lappos, downface, upface


def build_edge(data_dir, foot):
    from gems57.geo import load_planes  # shared template planes, unmodified
    import sys
    from pathlib import Path
    # vendor geo expects data/official/training_features.tif; pass our path
    planes = load_planes(foot, path=Path(data_dir) / "training_features.tif")
    logs = np.zeros(foot.shape, np.float64)
    n = 0
    names = []
    with rasterio.open(f"{data_dir}/lidar_scarp_features_u8.tif") as ds:
        for b in LIDAR_BANDS:
            a = ds.read(b).astype(np.float32)
            r = rank_unit(np.where(a > 0, a, 0.0), foot)
            logs += np.log(np.clip(r, 1e-6, None)); n += 1; names.append(f"lidar_b{b}")
    for k in ["g_tmi_hg", "g_tc", "g_slope", "g_grav_hg", "g_curv", "g_base_edge"]:
        r = rank_unit(planes[k], foot)
        logs += np.log(np.clip(r, 1e-6, None)); n += 1; names.append(k)
    E = np.exp(logs / n).astype(np.float32)
    E[~foot] = 0.0
    return E, names
