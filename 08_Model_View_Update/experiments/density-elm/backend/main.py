from __future__ import annotations

import math
from typing import Any, Dict, List

import numpy as np
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from matplotlib import pyplot as plt


# -----------------------------
# Sample dataset (Old Faithful-like)
# Replace with your own points if needed.
# -----------------------------
def sample_points(n: int = 272, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    # Two clusters: short eruptions + long eruptions (roughly Old Faithful structure)
    c1 = rng.multivariate_normal(
        mean=[2.0, 55.0], cov=[[0.08, 0.0], [0.0, 30.0]], size=n // 2
    )
    c2 = rng.multivariate_normal(
        mean=[4.3, 80.0], cov=[[0.10, 0.0], [0.0, 40.0]], size=n - n // 2
    )
    pts = np.vstack([c1, c2]).astype(np.float64)
    return pts


PTS = sample_points()


# -----------------------------
# KDE + contour extraction
# -----------------------------
def kde2d_gaussian_grid(
    points: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    bandwidth: float,
) -> np.ndarray:
    """
    Simple isotropic Gaussian KDE on a grid.
    points: (N,2)
    x: (nx,) grid coords
    y: (ny,) grid coords
    returns density: (ny,nx)
    """
    if bandwidth <= 0:
        raise ValueError("bandwidth must be > 0")

    nx = x.shape[0]
    ny = y.shape[0]

    X, Y = np.meshgrid(x, y)  # (ny,nx)
    dx = X[..., None] - points[:, 0][None, None, :]  # (ny,nx,N)
    dy = Y[..., None] - points[:, 1][None, None, :]  # (ny,nx,N)

    inv2h2 = 1.0 / (2.0 * bandwidth * bandwidth)
    # Unnormalized Gaussian sum
    z = np.exp(-(dx * dx + dy * dy) * inv2h2).sum(axis=-1)  # (ny,nx)

    # Normalize as a density (optional; relative scale usually sufficient for contours)
    norm = 1.0 / (2.0 * math.pi * bandwidth * bandwidth * points.shape[0])
    return z * norm


def extract_contours_matplotlib(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    levels: List[float],
) -> List[Dict[str, Any]]:
    """
    Extract contour paths as lists of polylines using matplotlib's contouring.
    Returns list of objects:
      { "level": float, "paths": [ [ [x,y], ... ], ... ] }
    """
    fig = plt.figure()
    try:
        cs = plt.contour(x, y, z, levels=levels)
        out: List[Dict[str, Any]] = []
        for lev, coll in zip(cs.levels, cs.collections):
            paths = []
            for p in coll.get_paths():
                v = p.vertices  # (M,2)
                if v.shape[0] >= 2:
                    paths.append(v.tolist())
            out.append({"level": float(lev), "paths": paths})
        plt.close(fig)
        return out
    finally:
        plt.close(fig)


def compute_contours_payload(
    points: np.ndarray,
    bandwidth: float,
    n_levels: int,
    grid_size: int = 200,
    pad_frac: float = 0.08,
) -> Dict[str, Any]:
    """
    Compute KDE over a grid and extract n_levels contours.
    Contour levels chosen as quantiles of the positive density mass.
    """
    pts = np.asarray(points, dtype=np.float64)
    x_min, y_min = pts.min(axis=0)
    x_max, y_max = pts.max(axis=0)

    # pad domain a bit (like D3 does implicitly by bandwidth)
    dx = x_max - x_min
    dy = y_max - y_min
    x_min -= pad_frac * dx
    x_max += pad_frac * dx
    y_min -= pad_frac * dy
    y_max += pad_frac * dy

    x = np.linspace(x_min, x_max, grid_size)
    y = np.linspace(y_min, y_max, grid_size)

    z = kde2d_gaussian_grid(pts, x, y, bandwidth=bandwidth)

    # Choose levels: quantiles of z (avoid zeros)
    zz = z[z > 0]
    if zz.size == 0:
        levels = np.linspace(float(z.min()), float(z.max()), max(n_levels, 1))
    else:
        # higher quantiles give outer-ish contours; tweak as desired
        qs = np.linspace(0.70, 0.995, max(n_levels, 1))
        levels = np.quantile(zz, qs)

    contours = extract_contours_matplotlib(x, y, z, levels=levels.tolist())

    return {
        "domain": {
            "xMin": float(x_min),
            "xMax": float(x_max),
            "yMin": float(y_min),
            "yMax": float(y_max),
        },
        "points": pts.tolist(),
        "contours": contours,
    }


# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI()

# Allow your Elm dev server / static hosting origin. For local dev, this is fine.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Serve static files (index.html + elm.js) at /
# Put compiled elm.js and index.html into ../static
app.mount("/", StaticFiles(directory="../static", html=True), name="static")


@app.get("/api/contours")
def api_contours(
    bandwidth: float = Query(2.0, ge=0.05, le=20.0),
    levels: int = Query(15, ge=3, le=40),
    grid: int = Query(200, ge=80, le=400),
) -> Dict[str, Any]:
    payload = compute_contours_payload(
        PTS, bandwidth=bandwidth, n_levels=levels, grid_size=grid
    )
    return payload
