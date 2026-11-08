"""Vectorize the original KTM logo and place it onto the design at each KTM position.

Each placement fits four logo landmarks (K bottom-left foot, T bar top-left corner,
M top-right corner, M bottom-right corner) onto the same landmarks read from the
design with a least-squares SIMILARITY transform (scale + rotation + shift only),
so the official logo keeps its exact proportions and is never skewed.

Usage: python3 -I fit_logo.py <logo_image> <out_dir>
Writes <out_dir>/ktm_logo.svg (clean vector logo) and <out_dir>/ktm_placements.json
(logo polygons in design-image pixel coordinates).
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# landmarks in design pixels: [K bottom-left, T bar top-left, M top-right, M bottom-right]
PLACEMENTS = {
    "LEFT_SIDE": [[483.3, 306.7], [530.0, 239.2], [674.2, 242.5], [640.8, 257.5]],   # LFD + LRD
    "RIGHT_SIDE": [[376.7, 581.7], [440.8, 552.5], [575.8, 601.7], [556.7, 645.0]],  # RRD + RFD
    "TAILGATE": [[1182.5, 623.3], [1224.2, 575.8], [1305.8, 557.5], [1290.8, 600.0]],  # TG
}
# visual fine-tuning after the least-squares fit: scale, rotation (deg), shift (px) about the logo centre
ADJUST = {
    "LEFT_SIDE": {"scale": 1.12, "rot": -4.0, "dx": 0.0, "dy": 3.0},
    "RIGHT_SIDE": {"scale": 1.0, "rot": 0.0, "dx": 0.0, "dy": 0.0},
    "TAILGATE": {"scale": 1.08, "rot": 0.0, "dx": 2.0, "dy": 3.0},
}


def logo_polygons(path):
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, "white")
    gray = np.array(Image.alpha_composite(bg, im).convert("L"))
    mask = (gray < 128).astype(np.uint8) * 255
    contours, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    polys = []
    for i, c in enumerate(contours):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < 50:
            continue
        shell = cv2.approxPolyDP(c, 1.0, True)[:, 0, :].tolist()
        holes = []
        j = hier[0][i][2]
        while j != -1:
            if cv2.contourArea(contours[j]) >= 50:
                holes.append(cv2.approxPolyDP(contours[j], 1.0, True)[:, 0, :].tolist())
            j = hier[0][j][0]
        polys.append({"shell": shell, "holes": holes})
    return polys, mask.shape


def landmarks(polys):
    pts = np.array([p for poly in polys for p in poly["shell"]], dtype=float)
    miny, maxy = pts[:, 1].min(), pts[:, 1].max()
    bottom = pts[pts[:, 1] >= maxy - 3]
    k_foot = bottom[bottom[:, 0].argmin()]
    top = pts[pts[:, 1] <= miny + 3]
    t_bar = top[top[:, 0].argmin()]
    m_top = pts[pts[:, 0].argmax()]
    right_bottom = bottom[bottom[:, 0].argmax()]
    return np.float32([k_foot, t_bar, m_top, right_bottom])


def main(logo_path, out_dir):
    out = Path(out_dir)
    polys, (h, w) = logo_polygons(logo_path)
    src = landmarks(polys)

    # clean vector logo (black, original proportions)
    d = " ".join("M" + " L".join(f"{x},{y}" for x, y in ring) + " Z"
                 for p in polys for ring in [p["shell"]] + p["holes"])
    (out / "ktm_logo.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
        f'<path fill="#000" fill-rule="evenodd" d="{d}"/></svg>', encoding="utf-8")

    result = {"landmarks_logo_px": src.tolist(), "placements": {}}
    for name, dst in PLACEMENTS.items():
        A, _ = cv2.estimateAffinePartial2D(src, np.float32(dst), ransacReprojThreshold=1e9)
        adj = ADJUST.get(name, {})
        c = np.float32(dst).mean(axis=0)
        R = cv2.getRotationMatrix2D((float(c[0]), float(c[1])), -adj.get("rot", 0.0), adj.get("scale", 1.0))
        R[0, 2] += adj.get("dx", 0.0)
        R[1, 2] += adj.get("dy", 0.0)
        A = (np.vstack([R, [0, 0, 1]]) @ np.vstack([A, [0, 0, 1]]))[:2]
        tf = lambda ring: [[float(A[0, 0] * x + A[0, 1] * y + A[0, 2]), float(A[1, 0] * x + A[1, 1] * y + A[1, 2])]
                           for x, y in ring]
        result["placements"][name] = [{"shell": tf(p["shell"]), "holes": [tf(hh) for hh in p["holes"]]} for p in polys]
    (out / "ktm_placements.json").write_text(json.dumps(result), encoding="utf-8")
    print("logo parts:", len(polys), "landmarks:", src.tolist())


if __name__ == "__main__":
    main(*sys.argv[1:3])
