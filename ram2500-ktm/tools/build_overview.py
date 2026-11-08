"""Assemble all panel previews into one overview sheet and a material summary.

Usage: python3 -I build_overview.py <out_dir>
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LAYOUT = [
    ("LEVÁ STRANA (předek vlevo)", ["LFF", "LFD", "LRD", "LBS"]),
    ("PRAVÁ STRANA (předek vpravo)", ["RBS", "RRD", "RFD", "RFF"]),
    ("KAPOTA / STŘECHA / VÍKO KORBY", ["HOOD", "ROOF", "TG"]),
    ("NÁRAZNÍKY", ["FBMP-R", "FBMP-L", "RBMP-L", "RBMP-R"]),
]
COLORS = ["ORANZOVA", "MODRA", "CERVENA", "BILA"]
PX_PER_MM = 0.25  # preview images are 2 px/mm with 40 mm padding
RESERVE = 1.15


def font(size):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main(out_dir):
    out = Path(out_dir)
    k = PX_PER_MM / 2
    rows, width = [], 0
    for title, codes in LAYOUT:
        tiles = []
        for c in codes:
            im = Image.open(out / c / f"{c}_preview.png")
            tiles.append((c, im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)))
        w = sum(t.width for _, t in tiles) + 30 * (len(tiles) - 1)
        h = max(t.height for _, t in tiles) + 100
        rows.append((title, tiles, h))
        width = max(width, w)
    width += 80
    H = 160 + sum(h for *_, h in rows) + 40 * len(rows)
    sheet = Image.new("RGB", (width, H), "white")
    d = ImageDraw.Draw(sheet)
    d.text((40, 30), "RAM 2500 – KTM „Total Crazy 2“ – přehled dílů (DRAFT – jednotné měřítko, rozměry = odhad)", font=font(30), fill="black")
    d.text((40, 80), "Černá = lak vozu (nevyrábí se). Šedé obdélníky = klika / světlo / emblém (nepolepovat).", font=font(20), fill="#555")
    y = 150
    for title, tiles, h in rows:
        d.text((40, y), title, font=font(24), fill="#d94f00")
        x = 40
        for c, t in tiles:
            sheet.paste(t, (x, y + 70))
            d.text((x, y + 38), c, font=font(22), fill="black")
            x += t.width + 30
        y += h + 40
    sheet.save(out / "PREHLED_dilu.png")

    totals = {c: [0, 0.0] for c in COLORS}
    lines = ["| díl | název | rozměr (mm) | " + " | ".join(COLORS) + " | kusů |", "|---|---|---|" + "---|" * (len(COLORS) + 1)]
    for _, codes in LAYOUT:
        for c in codes:
            s = json.loads((out / c / f"{c}_summary.json").read_text())
            cells, n = [], 0
            for col in COLORS:
                v = s["colors"].get(col, {"pieces": 0, "area_m2": 0})
                cells.append(f'{v["pieces"]} ks / {v["area_m2"]:.2f} m²' if v["pieces"] else "–")
                totals[col][0] += v["pieces"]
                totals[col][1] += v["area_m2"]
                n += v["pieces"]
            lines.append(f'| {c} | {s["name"]} | {s["size_mm"][0]} × {s["size_mm"][1]} | ' + " | ".join(cells) + f" | {n} |")
    all_pcs = sum(v[0] for v in totals.values())
    tot = ["| barva | kusů | čistá plocha (m²) | s rezervou 15 % (m²) | role 1520 mm – metrů (orientačně) |", "|---|---|---|---|---|"]
    for col in COLORS:
        n, a = totals[col]
        # cut vinyl nests poorly (diagonal shards), assume ~55 % roll utilisation
        tot.append(f"| {col} | {n} | {a:.2f} | {a * RESERVE:.2f} | {a * RESERVE / 0.55 / 1.52:.1f} |")
    md = ["# RAM 2500 – KTM „Total Crazy 2“ – souhrn kusů a fólie (DRAFT)", "",
          f"Celkem **{all_pcs} kusů** z barevné fólie. Rozměry dílů jsou odhad, plochy se po přeměření změní.", "",
          "## Spotřeba fólie", ""] + tot + ["", "## Po dílech", ""] + lines + [""]
    (out / "SOUHRN.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(tot))


if __name__ == "__main__":
    main(sys.argv[1])
