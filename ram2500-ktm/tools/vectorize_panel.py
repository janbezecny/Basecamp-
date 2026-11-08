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
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    outline_px = Polygon(cfg["outline_px"])
    bx0, by0, bx1, by1 = outline_px.bounds
    if "size_mm" in cfg:  # measured / estimated size of the panel bounding box
        W, H = cfg["size_mm"]
        sx_px, sy_px = W / (bx1 - bx0), H / (by1 - by0)
    else:  # one common scale for the whole view keeps seams between panels aligned
        sx_px = sy_px = cfg["mm_per_px"]
        W, H = (bx1 - bx0) * sx_px, (by1 - by0) * sy_px
    W, H = round(W), round(H)

    def to_mm(geom):
        g = affinity.translate(geom, -bx0, -by0)
        return affinity.scale(g, sx_px, sy_px, origin=(0, 0))

    def rect_mm(r):
        return to_mm(box(*r))

    src = np.array(Image.open(img_path).convert("RGB"))
    x0, y0, x1, y1 = int(bx0), int(by0), int(np.ceil(bx1)), int(np.ceil(by1))
    crop = src[y0:y1, x0:x1]
    big = cv2.resize(crop, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_CUBIC)
    big = cv2.bilateralFilter(big, 9, 40, 9)
    masks = classify(big)
    # mask pixel -> source px -> mm
    sx, sy = sx_px / UPSCALE, sy_px / UPSCALE
    off = ((x0 - bx0) * sx_px, (y0 - by0) * sy_px)

    panel = to_mm(outline_px)
    for c in cfg.get("cutouts_px", []):
        if "circle" in c:
            cx, cy, r = c["circle"]
            hole = Polygon([(cx + r * np.cos(t), cy + r * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 180)])
        else:
            hole = Polygon(c["poly"])
        panel = panel.difference(to_mm(hole))
    panel = panel.buffer(0)
    seam = cfg.get("seam_mm", 6)
    cut_area = panel.buffer(seam, join_style=2)
    obstacles = [dict(o, geom=rect_mm(o["rect_px"])) for o in cfg.get("obstacles_px", [])]
    logos = [dict(o, geom=rect_mm(o["rect_px"])) for o in cfg.get("logos_px", [])]
    keepout = unary_union([o["geom"].buffer(CLEARANCE_MM, join_style=2) for o in obstacles + logos]) \
        if (obstacles or logos) else Polygon()
    registration = cfg.get("registration") or [[25, 25], [W - 25, 25], [25, H - 25], [W - 25, H - 25]]

    geoms = {}
    for name, cc, _ in COLORS:
        g = affinity.translate(mask_to_geom(masks[cc], sx, sy), *off).buffer(0)
        g = g.intersection(panel)
        # shapes reaching a panel edge continue into the seam / wrap allowance
        near_edge = g.buffer(seam + 1, join_style=2).intersection(cut_area.difference(panel))
        geoms[cc] = unary_union([g, near_edge])

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
    panel_d = " ".join(path_d(p) for p in as_list(panel))
    cut_d = " ".join(path_d(p) for p in as_list(cut_area))
    L.append(f'<g id="LAK_NAHLED"><path fill="#111111" fill-rule="evenodd" d="{panel_d}"/></g>')
    L.append(f'<g id="OBRYS_DILU" fill="none" stroke="#888" stroke-width="0.3">'
             f'<path d="{panel_d}"/><path d="{cut_d}" stroke-dasharray="2 2"/></g>')
    L.append('<g id="PREKAZKY" fill="none" stroke="#bbb" stroke-width="0.5" stroke-dasharray="4 2">')
    for o in obstacles:
        x, y, X, Y = o["geom"].bounds
        L.append(f'<rect x="{x}" y="{y}" width="{X-x}" height="{Y-y}" rx="6"/>'
                 f'<text x="{x+2}" y="{y-2}" font-size="7" fill="#bbb" stroke="none" font-family="Arial">{o["label"]}</text>')
    for l in logos:
        x, y, X, Y = l["geom"].bounds
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
    for rx, ry in registration:
        L.append(f'<circle cx="{rx}" cy="{ry}" r="4"/><path d="M{rx-8},{ry} H{rx+8} M{rx},{ry-8} V{ry+8}"/>')
        L.append(f'<text x="{rx+6}" y="{ry-6}" fill="#ff00ff" stroke="none">({rx:.0f}; {ry:.0f})</text>')
    L.append(f'<text x="0" y="{H+20}" fill="#ff00ff" stroke="none">0;0 = levý horní roh výkresu, pohled zvenku na díl. Kóty v mm. ROZMĚRY = ODHAD, OVĚŘIT NA VOZE.</text>')
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
    for p in as_list(panel):
        d.polygon([T(x, y) for x, y in p.exterior.coords], fill="#111111")
        for hole in p.interiors:
            d.polygon([T(x, y) for x, y in hole.coords], fill="#f2f2f2")
    for o in obstacles + logos:
        x, y, X, Y = o["geom"].bounds
        d.rectangle([T(x, y), T(X, Y)], outline="#bbbbbb", width=2)
    for pc in pieces:
        for poly in as_list(pc["poly"]):
            d.polygon([T(x, y) for x, y in poly.exterior.coords], fill=pc["color"],
                      outline="#777777" if pc["layer"] == "BILA" else None)
            for hole in poly.interiors:
                d.polygon([T(x, y) for x, y in hole.coords], fill="#111111")
    d.text((10, 10), f'{code} – {cfg["name"]} – {W} x {H} mm (odhad)', fill="#000000")
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
    print(code, f"{W}x{H}mm", {k: v[0] for k, v in totals.items()}, "pieces:", len(pieces))
    (out_dir / f"{code}_summary.json").write_text(json.dumps({
        "code": code, "name": cfg["name"], "size_mm": [W, H],
        "colors": {k: {"pieces": v[0], "area_m2": round(v[1] / 1e6, 4)} for k, v in totals.items()},
    }, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(*sys.argv[1:4])
