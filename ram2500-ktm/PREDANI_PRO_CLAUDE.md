# Předání projektu do Claude (claude.ai)

## Jak pokračovat v novém chatu

1. Na claude.ai zapněte **Nastavení → Funkce → Code execution and file creation**.
2. Založte nový chat (ideálně v Projektu, aby soubory zůstaly po ruce).
3. Přiložte **`ram2500-ktm_podklady.zip`**.
4. Vložte text níže (sekce „Úvodní zpráva“).

---

## Úvodní zpráva (zkopírujte celé)

```
Pokračujeme v rozpracovaném projektu: výrobní podklady polepu RAM 2500 Crew Cab,
design KTM „Total Crazy 2“. V příloze je ZIP s celým projektem.

KLÍČOVÉ ZADÁNÍ
- NENÍ to celopolep. Auto je černě lakované, černá v návrhu = lak, nevyrábí se.
- Vyrábí se jen barevné segmenty (oranžová, modrá, červená, bílá) z řezané fólie,
  každý kus se lepí samostatně na lak.

ROZHODNUTÍ, KTERÁ PLATÍ
- Grafika přes okna: useknout u oken (na skla nic).
- Palivová dvířka: neřešit, dořízne se ručně.
- Logo KTM: originální vektor (source/ktm_logo_original.webp), nikdy nedeformovat,
  jen zvětšit/otočit/posunout. 15 mm černá mezera kolem písmen.
- Sloupky kabiny, zrcátka, prahy: zpracujeme později (TODO).

PRAVIDLA VÝROBY
min. šířka tvaru 5 mm; kusy pod 150 mm² pryč; barvy se nepřekrývají, spodní 2 mm
pod horní (modrá → červená → oranžová → bílá navrchu); 6 mm přesah do spár a za hrany;
3 mm odstup od klik, světel, antény a emblémů.

STAV
Hotovo všech 15 dílů (LFF, LFD, LRD, LBS, RFF, RFD, RRD, RBS, HOOD, ROOF, TG,
FBMP-L/R, RBMP-L/R), 576 kusů, originální logo KTM dosazené. Rozměry jsou ODHAD.

POSTUP
1. Rozbal ZIP, přečti README.md a tento soubor PREDANI_PRO_CLAUDE.md.
2. pip install opencv-python-headless shapely pillow
3. Ověř, že vše běží:
   python3 tools/fit_logo.py source/ktm_logo_original.webp source
   for f in panels/*.json; do c=$(basename $f .json); python3 tools/vectorize_panel.py source/navrh_design20_total_crazy2.webp $f out/$c; done
   python3 tools/build_overview.py out
4. Pak mi napiš, že je projekt načtený, a čekej na další úkol
   (např. naměřené rozměry, sloupky/zrcátka/prahy).
Na konci každé práce mi vrať aktualizovaný ZIP.
```

---

## Co je v ZIPu

| Cesta | Obsah |
|---|---|
| `README.md` | kompletní dokumentace: pravidla, rozhodnutí, TODO, kontrola rozměrů |
| `PREDANI_PRO_CLAUDE.md` | tento soubor |
| `source/navrh_design20_total_crazy2.webp` | schválená vizualizace |
| `source/ktm_logo_original.webp`, `source/ktm_logo.svg` | dodané logo KTM a jeho vektor |
| `source/ktm_placements.json` | umístění loga na voze (generuje `fit_logo.py`) |
| `panels/*.json` | definice 15 dílů: obrys v px návrhu, výřezy podběhů, překážky, emblémy, měřítko, `ktm_logo` |
| `tools/vectorize_panel.py` | převod jednoho dílu na řezací SVG |
| `tools/fit_logo.py` | vektorizace a umístění loga KTM |
| `tools/build_overview.py` | přehledový list a souhrn fólie |
| `out/PREHLED_dilu.png` | přehled všech dílů |
| `out/SOUHRN.md` | kusy a spotřeba fólie |
| `out/<DÍL>/` | montážní SVG, řezací SVG po barvách, náhled, tabulka kusů |

## Jak upravit díl

- **Skutečný rozměr po změření:** do `panels/<DÍL>.json` přidat `"size_mm": [šířka, výška]`
  (rozměr obdélníku, který díl obepíná, v mm) a znovu spustit převod.
- **Překážka (klika, světlo…):** `"obstacles_px": [{"label": "...", "rect_px": [x0, y0, x1, y1]}]`
  v pixelech návrhu (obrázek 1448 × 1086 px).
- **Emblém, který zůstává na voze:** `"logos_px"` (stejný formát).
- **Podběh kola:** `"cutouts_px": [{"circle": [cx, cy, r]}]`.
- **Poloha loga KTM:** `ADJUST` v `tools/fit_logo.py`, pak spustit `fit_logo.py` a převod dílů LFD, LRD, RRD, RFD, TG.

## Souřadnice dílů v návrhu (px, obrázek 1448 × 1086)

- Levý bok: vůz zhruba x 105–955, y 105–415. Přední kolo ve středu (248, 348), zadní (790, 348). Měřítko 7,0 mm/px.
- Pravý bok: přední část vpravo. Zadní kolo (242, 685), přední (790, 685).
- Pohled zepředu: x 1020–1400, y 100–420. Pohled zezadu: x 1030–1390, y 455–700.
- Kapota shora: x 20–360, y 805–1040. Střecha shora: x 370–760, y 795–1040 (vlevo = čelní sklo).
