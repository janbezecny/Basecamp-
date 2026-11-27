# Prompt: Forecast GM1 na rok 2027 (E-shop CZ a E-shop SK)

> Zkopíruj vše pod čarou do nového chatu s Claudem s připojeným rozšířením Claude in Chrome a přihlášeným Power BI v Chromu.

---

## Role a cíl

Jsi senior datový analytik a specialista na forecasting v e-commerce. Tvým úkolem je připravit **forecast GM1 (hrubá marže 1) na rok 2027 po měsících**, a to **zvlášť pro trh CZ a trh SK**. Výstupem je **jeden Excel sešit (.xlsx)** s daty, několika forecastovacími modely, backtestem, nastavitelnými parametry a písemným závěrem, který model je nejvhodnější.

Pracuj pečlivě, postup popiš transparentně a všechny předpoklady výslovně uveď. Kde si nejsi jistý (chybějící data, nejasná definice metriky), zastav se a zeptej se, místo abys hádal.

## Kontext byznysu

- E-shop Růžový slon, dva trhy: **CZ (ruzovyslon.cz)** a **SK (ruzovyslon.sk)**.
- Sortiment je rozdělen podle **ABC klasifikace**; skupiny **AA a A jsou naše privátní značka**.
- **Od 1. 9. 2026 proběhlo přecenění skupin AA a A.** Od té doby je GM1 (zejména GM1 %) mírně nižší než před přeceněním. Jde o strukturální zlom, který modely musí zohlednit — nesmí ho považovat za náhodný šum ani ho slepě ignorovat.
- Dnešní datum: 27. 11. 2026 → **listopad 2026 je neúplný měsíc**. Buď ho dopočítej (run-rate dle dnů / dle loňského průběhu měsíce, s uvedením metody), nebo ho v modelech označ jako odhad. Nikdy ho nepoužívej jako kompletní skutečnost bez úpravy.
- Měna: v Power BI jsou **oba trhy (CZ i SK) v CZK**. Forecast proto počítej v CZK pro oba trhy, aby byl přímo porovnatelný s reportem. Na kurz EUR/CZK nic nepřepočítávej.

## Zdroje dat

**Přístup:** Power BI otevři v prohlížeči **Chrome přes Claude in Chrome** (uživatel je v Chromu přihlášený). Reporty otevírej v nové záložce, filtry nastavuj přímo v reportu a data stahuj exportem z vizuálů. Když export není dostupný, data opiš z tabulkového vizuálu (případně si tabulku zobraz přes „Zobrazit jako tabulku“). Po každém stažení zkontroluj, že je správně nastavený filtr trhu a období.

### a) Prodejní data / GM1 (Power BI – Sales report)
URL: https://app.powerbi.com/groups/me/apps/44b71cd3-f671-4188-a650-ad58ff34bd8a/reports/3d51adb4-0b12-4eb6-b590-9ede39fac3bf/salesreport000000002?experience=power-bi

- Trh CZ = filtr **„E-shop CZ“**, trh SK = filtr **„E-shop SK“**.
- Vytáhni **měsíčně od 1/2023 do 11/2026**, pro každý trh zvlášť:
  - Tržby bez DPH, GM1 (absolutně), GM1 %, počet objednávek, průměrná hodnota objednávky (AOV), případně prodané kusy.
  - Totéž **rozpadnuté podle ABC klasifikace** (AA, A, B, C, … — dle tříd, které report obsahuje): tržby, GM1, GM1 % za každou třídu a měsíc.
- Postup v Chromu: nastav filtr trhu (E-shop CZ, pak E-shop SK) a časovou granularitu „měsíc“, potom vizuál → „…“ (Více možností) → **Exportovat data** → souhrnná data → CSV/XLSX. Každý trh exportuj zvlášť a stažené soubory pojmenuj podle trhu a obsahu.

### b) Google Analytics data (Power BI – GA report)
URL: https://app.powerbi.com/groups/me/apps/44b71cd3-f671-4188-a650-ad58ff34bd8a/reports/55d1c0d4-98d7-4af0-a7d9-df94ea364fb9/3f2f3737d53fdc3817e1?experience=power-bi

- CZ = **ruzovyslon.cz**, SK = **ruzovyslon.sk**.
- Měsíčně od 1/2023 do 11/2026: sessions (návštěvy), uživatelé, transakce, konverzní poměr (CR), tržby dle GA, ideálně rozpad podle kanálů (organic, paid, direct, e-mail, …).

**Data nikdy nevymýšlej.** Když se k některému vizuálu nebo filtru přes Chrome nedostaneš (chybí oprávnění, vizuál nejde exportovat, nejsou vidět filtry), zastav se a řekni mi přesně, co potřebuješ (vizuál, filtry, sloupce, období).

### Kontrola kvality dat (před modelováním)
- Sedí součet ABC tříd na celkový GM1 za měsíc? (tolerance ±0,5 %)
- Sedí GA transakce řádově na počet objednávek ze Sales reportu? Uveď poměr GA/Sales po měsících (pokrytí trackingu, vliv cookie lišty).
- Chybějící měsíce, extrémy (Black Friday, Vánoce, výpadky trackingu, mimořádné akce) — označ je a popiš, jak s nimi zacházíš.

## Úkoly

### c) Historický vývoj GM1 od 2023
V listu **`Data_GM1`** připrav přehlednou tabulku (měsíc × trh) a v listu **`Historie`**:
- měsíční GM1, GM1 %, tržby; meziroční změny (YoY) v % ;
- roční součty 2023, 2024, 2025, 2026 (YTD + odhad celého roku);
- grafy: GM1 v čase (CZ, SK), GM1 % v čase s vyznačeným přeceněním 1. 9. 2026, sezónní profil (podíl měsíce na roku).

### d) Forecast více způsoby (pro CZ i SK zvlášť)

**1. Modely časových řad** (list `FC_TS_CZ`, `FC_TS_SK`)
- Seasonal naive (stejný měsíc loni × trend YoY) — jako benchmark.
- ETS / Holt-Winters (aditivní i multiplikativní sezónnost, s tlumeným trendem).
- SARIMA (výběr řádu dle AIC; pozor na malý počet pozorování ≈ 47 měsíců).
- Prophet nebo regrese s měsíčními dummy proměnnými + **dummy proměnná pro přecenění od 9/2026**.
- Modeluj buď přímo GM1, nebo (doporučeno) zvlášť **tržby × GM1 %** — porovnej obojí.

**2. Forecast na základě GA dat** (list `FC_GA_CZ`, `FC_GA_SK`)
- Rozklad: **GM1 = Sessions × CR × AOV × GM1 %** (příp. korekce GA→Sales poměrem pokrytí).
- Každou složku forecastuj zvlášť (sessions sezónně + trend, CR a AOV jako sezónní průměry s trendem, GM1 % s ohledem na přecenění).
- Uveď, která složka nejvíc ovlivňuje výsledek (citlivostní tabulka ±10 % na každou složku).

**3. Forecast na základě poměrů ABC klasifikace** (list `FC_ABC_CZ`, `FC_ABC_SK`)
- Forecast celkových tržeb (z nejlepšího TS modelu) → rozpad do tříd ABC podle historických podílů (sezónních, po měsících) → GM1 % pro každou třídu → GM1 = Σ (tržby třídy × GM1 % třídy).
- Pro třídy **AA a A použij GM1 % po přecenění** (9–11/2026), pro ostatní třídy dlouhodobý sezónní průměr. Sleduj i posun mixu (zvyšuje/snižuje se podíl privátky po přecenění?).

**4. Kombinovaný (ensemble) forecast** (list `FC_Ensemble`)
- Vážený průměr modelů; výchozí váhy = inverzní WAPE z backtestu, váhy musí jít ručně přepsat.

### e) Nastavitelný vliv posledních 3 měsíců (9., 10., 11. 2026)
V listu **`Parametry`** vytvoř žlutě označené vstupní buňky, na které se všechny forecasty odkazují vzorci (žádné natvrdo vložené výsledky — sešit se musí přepočítat po změně parametru):

| Parametr | Výchozí hodnota | Význam |
|---|---|---|
| `w_recent` – váha posledních 3 měsíců | 50 % | 0 % = čistě dlouhodobý model; 100 % = forecast plně přizpůsoben úrovni a GM1 % z 9–11/2026 |
| `delta_GM1pct_AA_A` – dopad přecenění na GM1 % AA+A | vypočteno z dat (p.b.) | lze ručně přepsat |
| `podil_AA_A` – podíl privátky na tržbách | vypočteno z dat | scénář změny mixu |
| `trend_override` – ruční úprava růstu tržeb 2027 | 0 % | manažerský scénář |
| váhy modelů v ensemblu | z backtestu | ruční přepis |
| volba trhu / měny pro přehled | CZ | — |

Logika zapracování váhy:
- `recent_ratio` = skutečnost 9–11/2026 ÷ předpověď modelu pro 9–11/2026 (model trénovaný jen do 8/2026), zvlášť pro tržby a pro GM1 %.
- **Forecast_final = Forecast_base × (1 + w_recent × (recent_ratio − 1))**.
- Zobraz i 3 scénáře vedle sebe: w = 0 %, 50 %, 100 % (pesimistický / střední / optimistický) a graf, jak se roční GM1 2027 mění se změnou `w_recent` (tabulka citlivosti po 10 %).

### f) Backtest a výběr nejlepšího modelu
List **`Backtest`**:
- Simuluj situaci, jako bys forecastoval **na konci března 2026**: modely trénuj jen na datech **1/2023 – 3/2026** a předpovídej **4/2026 – 11/2026**. Porovnej se skutečností (11/2026 s dopočtem, viz výše).
- Pro každý model a trh spočti: **MAPE, WAPE, bias (průměrná odchylka v %), RMSE** a **chybu součtu za celé období 4–11** (nejdůležitější pro roční plán).
- Vyhodnoť zvlášť **období 4–8/2026 (před přeceněním)** a **9–11/2026 (po přecenění)** — model z března o přecenění nevěděl, takže ukaž, jak velkou část chyby vysvětluje právě přecenění a jak si model vede po aplikaci korekce z bodu e).
- Doplňkově (pokud zbude prostor): rolling-origin backtest (forecast z konce každého měsíce 3–8/2026, horizont 3 měsíce) pro robustnější srovnání.
- Tabulka pořadí modelů + graf skutečnost vs. předpovědi všech modelů.

### Závěry (list `Závery` + shrnutí v chatu)
- Který model je nejlepší pro CZ a který pro SK a **proč** (přesnost, stabilita, bias, interpretovatelnost, citlivost na malý vzorek dat).
- Teoretické zdůvodnění: kdy jsou lepší TS modely (stabilní sezónnost), kdy GA rozklad (změny návštěvnosti/marketingu), kdy ABC přístup (změny marže a mixu – zde přecenění privátky).
- Doporučený finální forecast 2027 (měsíčně + rok celkem, oba trhy v CZK) s intervalem (např. 80 % predikční interval nebo rozpětí scénářů).
- Hlavní rizika a předpoklady (vývoj po přecenění, Black Friday/Vánoce 2026 ještě nejsou v datech, změny trackingu GA).
- Doporučení, co sledovat měsíčně a kdy forecast přepočítat.

## Požadovaná struktura sešitu

1. `README` – popis listů, zdrojů, datum exportu, předpoklady
2. `Parametry` – vstupní buňky (bod e)
3. `Data_GM1` – měsíční data Sales (CZ, SK, rozpad ABC)
4. `Data_GA` – měsíční GA data (CZ, SK)
5. `Historie` – vývoj GM1 od 2023 + grafy
6. `FC_TS_CZ`, `FC_TS_SK`
7. `FC_GA_CZ`, `FC_GA_SK`
8. `FC_ABC_CZ`, `FC_ABC_SK`
9. `FC_Ensemble` – kombinace + scénáře
10. `Backtest` – metriky, pořadí, grafy
11. `Forecast_2027` – finální měsíční forecast CZ a SK (tržby, GM1 %, GM1), scénáře
12. `Závery`

Formátování: vstupy žlutě, vzorce černě, data z exportu modře; čísla s oddělovačem tisíců; GM1 % na 1 desetinné místo; zmrazené záhlaví. Statistické modely (SARIMA, ETS, Prophet) můžeš spočítat v Pythonu a do sešitu vložit jejich základní předpovědi; veškerá navazující logika (váhy, korekce posledních 3 měsíců, ensemble, scénáře) musí být **živými Excel vzorci**.

## Postup práce

1. Nejprve potvrď, jaká data máš k dispozici, a vypiš kontrolu kvality dat.
2. Ukaž historický vývoj a krátký komentář (sezónnost, trend, dopad přecenění v 9–11/2026 v p.b. GM1 %).
3. Proveď backtest všech modelů a ukaž srovnávací tabulku.
4. Teprve pak vytvoř forecast 2027 a sestav sešit.
5. Na závěr shrň v chatu: doporučený model pro CZ a SK, roční GM1 2027 ve třech scénářích a 3–5 klíčových rizik.
