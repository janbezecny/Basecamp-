"""Vectorize one body panel of the RAM 2500 KTM wrap design into cut-ready SVG.

Black in the design = the truck's black paint, so it is never produced.
Only orange / blue / red / white segments become vinyl pieces.

Usage: python3 -I vectorize_panel.py <design_image> <panel_json> <out_dir>
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely import affinity
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union

# bottom -> top stacking order; lower colours get a 2 mm overlap under upper ones
COLORS = [
    ("MODRA", "BL", "#1E6FE0"),
    ("CERVENA", "RD", "#E2231A"),
    ("ORANZOVA", "OR", "#FF6600"),
    ("BILA", "WH", "#FFFFFF"),
]
UPSCALE = 8
MIN_WIDTH_MM = 5.0
MIN_AREA_MM2 = 150.0  # drops splatter dots smaller than roughly 8 x 18 mm
OVERLAP_MM = 2.0
CLEARANCE_MM = 3.0
SIMPLIFY_MM = 0.4


def classify(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = [hsv[..., i].astype(int) for i in range(3)]
    masks = {
        "BL": (h >= 95) & (h <= 128) & (s > 110) & (v > 90),
        "RD": ((h <= 6) | (h >= 168)) & (s > 140) & (v > 110),
        "OR": (h > 6) & (h <= 32) & (s > 120) & (v > 130),
        "WH": (s < 55) & (v > 185),
    }
    out = {}
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    for code, m in masks.items():
        m = m.astype(np.uint8) * 255
        m = cv2.medianBlur(m, 5)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
        # bridge the thin shadow line of the body crease (bodyline) running through shapes
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 13)))
        out[code] = m
    return out


def mask_to_geom(mask, sx, sy):
    contours, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    polys = []
    if hier is None:
        return Polygon()
    hier = hier[0]
    for i, c in enumerate(contours):
        if hier[i][3] != -1 or len(c) < 3:
            continue
        shell = [(p[0][0] * sx, p[0][1] * sy) for p in c]
        holes = []
        j = hier[i][2]
        while j != -1:
            hc = contours[j]
            if len(hc) >= 3:
                holes.append([(p[0][0] * sx, p[0][1] * sy) for p in hc])
            j = hier[j][0]
        p = Polygon(shell, holes).buffer(0)
        if not p.is_empty:
            polys.append(p)
    return unary_union(polys) if polys else Polygon()


def manufacturable(g):
    """Remove parts narrower than MIN_WIDTH, round sharp tips, drop tiny dots."""
    r = MIN_WIDTH_MM / 2
    g = g.buffer(-r, join_style=1).buffer(r, join_style=1)
    return keep_big(g)


def keep_big(g):
    parts = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    out = []
    for p in parts:
        if p.is_empty or p.area < MIN_AREA_MM2:
            continue
        # fill pin-holes that cannot be weeded
        holes = [h for h in p.interiors if Polygon(h).area >= MIN_AREA_MM2]
        out.append(Polygon(p.exterior, holes))
    return unary_union(out) if out else Polygon()


def as_list(g):
    if g.is_empty:
        return []
    return list(g.geoms) if hasattr(g, "geoms") else [g]


def path_d(poly):
    def ring(coords):
        pts = list(coords)[:-1]
        return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"

    return " ".join([ring(poly.exterior.coords)] + [ring(i.coords) for i in poly.interiors])


def main(img_path, cfg_path, out_dir):
    cfg = json.loads(Path(cfg_path).read_text())
    code = cfg["code"]
    W, H = cfg["size_mm"]
    x0, y0, x1, y1 = cfg["crop_px"]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    src = np.array(Image.open(img_path).convert("RGB"))
    crop = src[y0:y1, x0:x1]
    big = cv2.resize(crop, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_CUBIC)
    big = cv2.bilateralFilter(big, 9, 40, 9)
    sx, sy = W / big.shape[1], H / big.shape[0]
    masks = classify(big)

    panel = box(0, 0, W, H)
    bl = cfg.get("bleed_mm", {})
    cut_area = box(-bl.get("left", 0), -bl.get("top", 0), W + bl.get("right", 0), H + bl.get("bottom", 0))
    obstacles = [box(*o["rect"]) for o in cfg.get("obstacles", [])]
    logos = [box(*l["rect"]) for l in cfg.get("logos", [])]
    keepout = unary_union([o.buffer(CLEARANCE_MM, join_style=2) for o in obstacles + logos]) if (obstacles or logos) else Polygon()

    geoms = {}
    for name, cc, _ in COLORS:
        g = mask_to_geom(masks[cc], sx, sy)
        # stretch geometry that touches a cut seam to the bleed line
        g = g.buffer(0)
        geoms[cc] = g

    # extrude shapes that touch a panel edge straight out into the seam allowance
    for cc, g in geoms.items():
        ext = [g]
        for side, b in bl.items():
            if b <= 0:
                continue
            band = {"left": box(0, 0, 6, H), "right": box(W - 6, 0, W, H),
                    "top": box(0, 0, W, 6), "bottom": box(0, H - 6, W, H)}[side]
            # merge contacts closer than 40 mm so the allowance is one clean tab, not a comb
            for part in as_list(g.intersection(band).buffer(20).buffer(-20).intersection(band)):
                x, y, X, Y = part.bounds
                ext.append({"left": box(-b, y, 6, Y), "right": box(W - 6, y, W + b, Y),
                            "top": box(x, -b, X, 6), "bottom": box(x, H - 6, X, H + b)}[side])
        geoms[cc] = unary_union(ext)

    # exclusive regions, upper colour wins, then lower gets 2 mm overlap under upper
    final = {}
    upper = Polygon()
    for name, cc, _ in reversed(COLORS):
        g = geoms[cc].difference(upper)
        g = manufacturable(g)
        final[cc] = g
        upper = unary_union([upper, g])
    for i, (name, cc, _) in enumerate(COLORS):
        above = unary_union([final[c[1]] for c in COLORS[i + 1:]]) if i + 1 < len(COLORS) else Polygon()
        tuck = final[cc].buffer(OVERLAP_MM, join_style=1).intersection(above)
        g = unary_union([final[cc], tuck])
        g = g.intersection(cut_area).difference(keepout)
        g = keep_big(g.buffer(0)).simplify(SIMPLIFY_MM, preserve_topology=True)
        # drop orphan seam tabs (pieces lying mostly outside the panel)
        g = unary_union([p for p in as_list(g) if p.intersection(panel).area >= 0.5 * p.area] or [Polygon()])
        final[cc] = g

    # number pieces left -> right, top -> bottom
    pieces = []
    for name, cc, hexc in COLORS:
        parts = sorted(as_list(final[cc]), key=lambda p: (round(p.centroid.x / 100), p.centroid.y))
        for n, p in enumerate(parts, 1):
            minx, miny, maxx, maxy = p.bounds
            pieces.append({
                "id": f"{code}-{cc}-{n:03d}", "layer": name, "color": hexc, "poly": p,
                "w": maxx - minx, "h": maxy - miny, "area": p.area,
            })

    pad = 40
    vb = f"{-pad} {-pad} {W + 2 * pad} {H + 2 * pad}"
    L = []
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * pad}mm" height="{H + 2 * pad}mm" viewBox="{vb}">')
    L.append(f'<title>{code} – {cfg["name"]} – RAM 2500 KTM Total Crazy 2 (DRAFT)</title>')
    L.append(f'<g id="LAK_NAHLED"><rect x="0" y="0" width="{W}" height="{H}" fill="#111111"/></g>')
    L.append(f'<g id="OBRYS_DILU" fill="none" stroke="#888" stroke-width="0.3">'
             f'<rect x="0" y="0" width="{W}" height="{H}"/>'
             f'<rect x="{cut_area.bounds[0]}" y="{cut_area.bounds[1]}" width="{cut_area.bounds[2]-cut_area.bounds[0]}" '
             f'height="{cut_area.bounds[3]-cut_area.bounds[1]}" stroke-dasharray="2 2"/></g>')
    L.append('<g id="PREKAZKY" fill="none" stroke="#bbb" stroke-width="0.5" stroke-dasharray="4 2">')
    for o in cfg.get("obstacles", []):
        x, y, X, Y = o["rect"]
        L.append(f'<rect x="{x}" y="{y}" width="{X-x}" height="{Y-y}" rx="6"/>'
                 f'<text x="{x+2}" y="{y-2}" font-size="7" fill="#bbb" stroke="none" font-family="Arial">{o["label"]}</text>')
    for l in cfg.get("logos", []):
        x, y, X, Y = l["rect"]
        L.append(f'<rect x="{x}" y="{y}" width="{X-x}" height="{Y-y}" stroke="#ff0"/>'
                 f'<text x="{x+3}" y="{y+12}" font-size="8" fill="#ff0" stroke="none" font-family="Arial">LOGO – vložit originální vektor</text>'
                 f'<text x="{x+3}" y="{y+24}" font-size="8" fill="#ff0" stroke="none" font-family="Arial">{l["label"]}</text>')
    L.append("</g>")
    for name, cc, hexc in COLORS:
        stroke = ' stroke="#9a9a9a" stroke-width="0.1"' if cc == "WH" else ""
        L.append(f'<g id="{name}" fill="{hexc}"{stroke}>')
        for pc in pieces:
            if pc["layer"] == name:
                L.append(f'<path id="{pc["id"]}" fill-rule="evenodd" d="{path_d(pc["poly"])}"/>')
        L.append("</g>")
    L.append('<g id="KODY" font-family="Arial" font-size="2.1" fill="#00e5ff">')
    for pc in pieces:
        pt = pc["poly"].representative_point()
        L.append(f'<text x="{pt.x:.1f}" y="{pt.y:.1f}" text-anchor="middle">{pc["id"]}</text>')
    L.append("</g>")
    L.append('<g id="REGISTRACE" stroke="#ff00ff" stroke-width="0.3" fill="none" font-family="Arial" font-size="6">')
    for rx, ry in cfg.get("registration", []):
        L.append(f'<circle cx="{rx}" cy="{ry}" r="4"/><path d="M{rx-8},{ry} H{rx+8} M{rx},{ry-8} V{ry+8}"/>')
        L.append(f'<text x="{rx+6}" y="{ry-6}" fill="#ff00ff" stroke="none">({rx:.0f}; {ry:.0f})</text>')
    L.append(f'<text x="0" y="{H+20}" fill="#ff00ff" stroke="none">0;0 = horní přední roh dílu (pod lištou okna u přední spáry). Kóty v mm. ROZMĚRY = ODHAD, OVĚŘIT NA VOZE.</text>')
    L.append("</g></svg>")
    (out_dir / f"{code}.svg").write_text("\n".join(L), encoding="utf-8")

    # per-colour cut files (only the cut contours, no preview layers)
    for name, cc, hexc in COLORS:
        mine = [p for p in pieces if p["layer"] == name]
        if not mine:
            continue
        C = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * pad}mm" height="{H + 2 * pad}mm" viewBox="{vb}">',
             f'<g id="{code}_{name}_CUT" fill="none" stroke="#000" stroke-width="0.1">']
        C += [f'<path id="{p["id"]}" d="{path_d(p["poly"])}"/>' for p in mine]
        C.append("</g></svg>")
        (out_dir / f"{code}_CUT_{name}.svg").write_text("\n".join(C), encoding="utf-8")

    # preview PNG (2 px per mm)
    s = 2
    im = Image.new("RGB", (int((W + 2 * pad) * s), int((H + 2 * pad) * s)), "#f2f2f2")
    d = ImageDraw.Draw(im)
    T = lambda x, y: ((x + pad) * s, (y + pad) * s)
    d.rectangle([T(0, 0), T(W, H)], fill="#111111")
    for o in cfg.get("obstacles", []) + cfg.get("logos", []):
        x, y, X, Y = o["rect"]
        d.rectangle([T(x, y), T(X, Y)], outline="#bbbbbb", width=2)
    for pc in pieces:
        for poly in as_list(pc["poly"]):
            d.polygon([T(x, y) for x, y in poly.exterior.coords], fill=pc["color"],
                      outline="#777777" if pc["layer"] == "BILA" else None)
            for hole in poly.interiors:
                d.polygon([T(x, y) for x, y in hole.coords], fill="#111111")
    im.save(out_dir / f"{code}_preview.png")

    # piece table
    rows = ["| kód kusu | barva | rozměr Š×V (mm) | plocha (cm²) |", "|---|---|---|---|"]
    for pc in pieces:
        rows.append(f'| {pc["id"]} | {pc["layer"]} | {pc["w"]:.0f} × {pc["h"]:.0f} | {pc["area"]/100:.0f} |')
    totals = {}
    for pc in pieces:
        t = totals.setdefault(pc["layer"], [0, 0.0])
        t[0] += 1
        t[1] += pc["area"]
    summary = ["| barva | kusů | plocha fólie (m²) |", "|---|---|---|"]
    for name, cc, _ in COLORS:
        if name in totals:
            summary.append(f"| {name} | {totals[name][0]} | {totals[name][1]/1e6:.3f} |")
    (out_dir / f"{code}_kusy.md").write_text(
        f"# {code} – {cfg['name']} – tabulka kusů (DRAFT)\n\n" + "\n".join(summary) + "\n\n" + "\n".join(rows) + "\n",
        encoding="utf-8")
    print(code, {k: v[0] for k, v in totals.items()}, "pieces:", len(pieces))


if __name__ == "__main__":
    main(*sys.argv[1:4])
