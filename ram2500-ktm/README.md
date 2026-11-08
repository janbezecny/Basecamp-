# RAM 2500 – KTM „Design 20 / Total Crazy 2“ – výrobní podklady polepu

Polep **není celopolep**. Černá v návrhu = černý lak vozu a nevyrábí se.
Vyrábí se jen barevné segmenty (oranžová, modrá, červená, bílá) z řezané fólie.
Každý kus se lepí samostatně na lak.

> ⚠️ **STAV: DRAFT – všech 15 dílů zpracováno, 576 kusů, originální logo KTM dosazeno.** Rozměry dílů jsou ODHAD (Gemini a proporce z vizualizace).
> Před řezáním je nutné je ověřit na voze. Viz „Co je potřeba“ níže.

## Co najdete kde

- **`out/PREHLED_dilu.png`**: přehled všech 15 dílů na jednom listu
- **`out/SOUHRN.md`**: počty kusů a spotřeba fólie po barvách a po dílech
- `out/<DÍL>/<DÍL>.svg`: montážní a kontrolní soubor 1:1 v mm s vrstvami
  `LAK_NAHLED`, `OBRYS_DILU`, `PREKAZKY`, `MODRA`, `CERVENA`, `ORANZOVA`, `BILA`, `KODY`, `REGISTRACE`
- `out/<DÍL>/<DÍL>_CUT_<BARVA>.svg`: čisté řezací kontury, jedna barva = jeden soubor
- `out/<DÍL>/<DÍL>_preview.png` a `<DÍL>_kusy.md`: náhled a tabulka kusů
- `panels/<DÍL>.json`: definice dílu (obrys v pixelech návrhu, výřezy podběhů, překážky, loga, měřítko)
- `tools/`: skripty (`vectorize_panel.py` převádí jeden díl, `build_overview.py` skládá přehled a souhrn)

| Kód | Díl |
|---|---|
| LFF / RFF | přední blatník L / P |
| LFD / RFD | přední dveře L / P (plech pod oknem) |
| LRD / RRD | zadní dveře L / P |
| LBS / RBS | bok korby L / P |
| HOOD | kapota |
| ROOF | střecha |
| TG | víko korby |
| FBMP-L / FBMP-R | přední nárazník, levý / pravý roh |
| RBMP-L / RBMP-R | zadní nárazník, levá / pravá část |

Kód kusu: `[díl]-[barva]-[číslo]`, např. `LRD-WH-003` (OR oranžová, BL modrá, RD červená, WH bílá).
Každý výkres je **pohled zvenku na díl**. 0;0 = levý horní roh výkresu.

## Měřítko

- Boky: jednotné měřítko odvozené z rozvoru (3 792 mm = 542 px, tj. 7,0 mm/px). Tvary na sousedních dílech proto na sebe navazují.
- Kapota, střecha, víko korby: rozměr podle odhadu (kapota 1 660 × 1 310, střecha 1 700 × 1 580, víko 1 640 × 620 mm).
- Nárazníky: měřítko z šířky vozu (2 120 mm).

**Po změření vozu** zapište do `panels/<DÍL>.json` hodnotu `"size_mm": [šířka, výška]` a spusťte znovu:

```bash
for f in panels/*.json; do c=$(basename $f .json); python3 -I tools/vectorize_panel.py source/navrh_design20_total_crazy2.webp $f out/$c; done
python3 -I tools/build_overview.py out
```

Po změně polohy loga KTM nejdřív: `python3 -I tools/fit_logo.py source/ktm_logo_original.webp source`

## Pravidla použitá ve vektorizaci

- min. šířka tvaru 5 mm (užší části a ostré špičky se zaoblí nebo odstraní)
- kusy pod 150 mm² (rozstřiky) a neodloupnutelné dírky se vypouští
- barvy se nepřekrývají, spodní barva zasahuje 2 mm pod horní (pořadí: modrá → červená → oranžová → bílá navrchu)
- tvary dosahující na hranu dílu pokračují 6 mm do spáry nebo za hranu (i do lemu podběhu)
- odstup 3 mm od klik, světel, antény, nasávání kapoty a emblémů (emblémy zůstávají originální, nebo se vloží vektor)

## Rozhodnutí zákazníka (platí)

| Téma | Rozhodnutí | Stav |
|---|---|---|
| grafika přes okna | **useknout u oken**, na skla se nic nelepí | ✅ hotovo: dveře a boky končí na lince okna, střecha nezasahuje do skel |
| sloupky kabiny, zrcátka, prahy | **zpracujeme později** | ⏳ TODO, viz níže |
| palivová dvířka (LBS) | **neřešit**, dořízne se ručně při montáži | ✅ hotovo |
| logo KTM | **použít originální vektor** (`source/ktm_logo_original.webp` → `source/ktm_logo.svg`) | ✅ hotovo na LFD/LRD, RRD/RFD, TG |

### Logo KTM

- `tools/fit_logo.py` převede dodané logo na vektor a umístí ho na tři místa návrhu (levý bok, pravý bok, víko korby).
- Logo se jen zvětšuje, otáčí a posouvá. **Nikdy se nedeformuje** (žádné zkosení), proporce zůstávají originální.
  Doladění polohy je v `ADJUST` ve `fit_logo.py`.
- Kolem písmen zůstává 15 mm černá mezera (lak), aby bylo logo čitelné. Obkreslený nápis z vizualizace je v oblasti loga odstraněný.
- Na bocích logo přechází přes spáru dveří (LFD→LRD, RRD→RFD) a dělí se na ní s přesahem 6 mm.

### TODO – zpracujeme později

- [ ] sloupky kabiny (A, B, C) a rámy kolem oken
- [ ] zrcátka
- [ ] prahy
- [ ] přeměřit vůz a doplnit `size_mm` do `panels/*.json`
- [ ] logo RAM / RAM 2500 (zatím ponechány originální emblémy vozu, v datech jako překážky)

## Kontrola výstupu z Gemini

| Údaj | Hodnocení |
|---|---|
| celkové rozměry (délka 6 066, rozvor 3 792, korba 1 938 mm) | ✅ odpovídá specifikaci RAM HD Crew Cab 6'4" |
| dveře, blatník, bok korby, víko | 🟡 věrohodné odhady, ověřit metrem |
| kapota 1 310 mm délka | ⚠️ u HD pravděpodobně podhodnoceno, změřit po povrchu |
| „přídavek +50–75 mm (bleed)“ | ❌ platí pro tištěný celopolep, **ne pro náš případ**. Používáme 6 mm do spár a 10 mm na spodní hraně. |
| klika „520 mm od spodní hrany“ | ⚠️ podle návrhu je klika cca 140 mm pod lištou okna. Změřit. |
| mezera kabina–korba 22–28 mm | ✅ důležité: segmenty musí končit na obou stranách mezery, nesmí přes ni přecházet |

## Analýza dílů

| Díl | Kód | Barvy | Poznámka |
|---|---|---|---|
| levý přední blatník | LFF | O, B, R, W | navazuje na kapotu a LFD, výřez světla a podběhu |
| levé přední dveře | LFD | O, B, R, W | začátek bílého „K“ na zadní hraně |
| levé zadní dveře | LRD | O, B, R, W | nese většinu loga KTM, navazuje na LFD |
| levý bok korby | LBS | O, B, R, W | palivová dvířka, zadní světlo, mezera ke kabině |
| pravá strana | RFF, RFD, RRD, RBS | O, B, R, W | není zrcadlo levé, KTM přechází přes spáru předních a zadních dveří |
| kapota | HOOD | O, B, R, W | silně zakřivená, větší kusy dělit |
| střecha | ROOF | O, B, R, W | 5 pozičních světel, anténa |
| víko korby | TG | O, B, R, W | KTM uprostřed, RAM a 2500, madlo a kamera |
| nárazníky | FBMP, RBMP | O, B, W | jen lakované části, senzory |

## Co je potřeba pro finální data

1. **Naměřit vůz** podle měřicího protokolu (Gemini) a hodnoty zapsat do `panels/*.json`.
2. **Zdrojový návrh ve vyšším rozlišení.** Vizualizace má na dveřích jen cca 166 px na 1 110 mm,
   tedy cca 7 mm na pixel. Tvary jsou proto interpretace. Originální soubor od designéra
   (ideálně vektor, nebo boční pohledy min. 4000 px na šířku) zásadně zpřesní výsledek.
3. ~~Originální vektor loga KTM~~ ✅ dodáno. Případně vektor RAM, pokud se má lepit.
4. Grafik zkontroluje v Illustratoru/Inkscapu a udělá nesting na šíři role. Na první díl zkušební tisk 1:1 na papír.
