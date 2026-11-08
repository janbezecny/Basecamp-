# RAM 2500 – KTM „Design 20 / Total Crazy 2“ – výrobní podklady polepu

Polep **není celopolep**. Černá v návrhu = černý lak vozu a nevyrábí se.
Vyrábí se jen barevné segmenty (oranžová, modrá, červená, bílá) z řezané fólie.
Každý kus se lepí samostatně na lak.

> ⚠️ **STAV: DRAFT.** Rozměry dílů jsou ODHAD (Gemini a proporce z vizualizace).
> Před řezáním je nutné je ověřit na voze. Viz „Co je potřeba“ níže.

## Struktura

| Složka | Obsah |
|---|---|
| `source/` | schválená vizualizace návrhu |
| `panels/*.json` | parametry dílu: rozměr v mm, výřez z návrhu, přesahy, překážky, loga |
| `tools/vectorize_panel.py` | převod dílu z návrhu na řezací SVG |
| `out/<DÍL>/` | výstupy pro díl |

Výstupy pro každý díl (`out/LFD/`):

- `LFD.svg` – montážní/kontrolní soubor 1:1 v mm s vrstvami
  `LAK_NAHLED`, `OBRYS_DILU`, `PREKAZKY`, `MODRA`, `CERVENA`, `ORANZOVA`, `BILA`, `KODY`, `REGISTRACE`
- `LFD_CUT_<BARVA>.svg` – čisté řezací kontury, jedna barva = jeden soubor
- `LFD_preview.png` – náhled
- `LFD_kusy.md` – tabulka kusů (kód, barva, rozměr, plocha) a spotřeba fólie

Kód kusu: `[díl]-[barva]-[číslo]`, např. `LFD-OR-002` (OR oranžová, BL modrá, RD červená, WH bílá).
Souřadnice 0;0 = horní přední roh dílu.

## Pravidla použitá ve vektorizaci

- min. šířka tvaru 5 mm (užší části a ostré špičky se zaoblí nebo odstraní)
- kusy pod 150 mm² (rozstřiky) a neodloupnutelné dírky se vypouští
- barvy se nepřekrývají, spodní barva zasahuje 2 mm pod horní (pořadí: modrá → červená → oranžová → bílá navrchu)
- tvary na spáře dveří: přesah 6 mm do spáry, spodní hrana dveří: 10 mm založení
- odstup 3 mm od kliky a od emblému RAM 2500 (emblém zůstává originální, nebo se vloží vektor)

Spuštění pro další díl:

```bash
python3 -I tools/vectorize_panel.py source/navrh_design20_total_crazy2.webp panels/LFD.json out/LFD
```

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
| **levé přední dveře** | **LFD** | O, B, R, W | **hotový draft** – 34 kusů, začátek bílého „K“ na zadní hraně |
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
3. Originální vektory loga KTM a RAM.
4. Grafik zkontroluje v Illustratoru/Inkscapu a udělá nesting na šíři role. Na první díl zkušební tisk 1:1 na papír.
