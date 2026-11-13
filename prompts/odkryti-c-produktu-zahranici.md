# Prompt: Vyhodnocení odkrytí C produktů v zahraničí (k 11. 11. 2026)

> Zdroj: Basecamp to-do „Odkrytí C produktů v zahraničí“ (bucket 40643108, to-do 10272661744) včetně všech komentářů 4. 9. – 16. 10. 2026.
> Použití: vložit celý blok „PROMPT“ do AI a přiložit datové soubory podle sekce „Potřebná data“.

---

## PROMPT

### Role
Jsi senior analytik e-commerce (nákup + výkonnostní marketing). Připravuješ vyhodnocení experimentu „odkrytí C produktů v zahraničí“ pro CEO (Adam Durčák), nákup (Jan Bezecný) a automatizaci (Miloš Murárik), v kopii Gabriel a marketing (Tereza). Výstup bude vložen jako komentář do Basecampu, česky, stručně, s čísly.

### Kontext experimentu
- **Co se změnilo:** produkty v tieru **C** (dle Google Sheetu „Seznam produktů“), které byly v zahraničí skryté, byly **20. 9. 2026 odkryty importem** (parametr „Zobrazit v listingu“). První plný den efektu = **21. 9. 2026**.
- **Země experimentu:** HU, BG, RO, SI (v zadání „SL“ = Slovinsko), HR – tj. všechny země RS mimo CZ/SK. **CZ a SK = kontrolní skupina** (zde se nic neměnilo).
- **Varianty:** odkrytí jedné varianty odkryje všechny varianty včetně hlavní. Skutečně odkrytá množina proto může být **větší než seznam EANů**. Položky, kde byla jedna varianta „skrýt“ a jiná „odkrýt“, import přeskočil (info hláška). Pracuj se **skutečně odkrytou množinou** (seznam + dotažené varianty − přeskočené) a rozdíl oproti seznamu vyčísli.
- **Rozsah odkrytí:** C produkty jsou zatím zařazené **jen v hlavní kategorii**, ne ve všech podkategoriích. Plný efekt se čeká až po zařazení do všech podkategorií a po náběhu organiky a retence (řádově měsíce). Interpretuj výsledky jako **efekt částečného odkrytí**.
- **Tiery:** AA, A = private label (PL); B1, B2 = B; C. CEO bere **B2 a C jako téměř totéž** – kanibalizace B2 mu nevadí, kanibalizace PL (AA/A) ano.
- **Známé datové problémy:** v reportu „Privátní značky“ (GA4) se nedočítala data od 29. 9. 2026. Ověř úplnost dat za celé období po 29. 9. a pokud chybí, explicitně to uveď a nepočítej z neúplných dní.

### Co už víme (průběžné vyhodnocení, data k 6. 10. 2026) – navaž a aktualizuj
- Do 20. 9.: C mělo trvale 80–90 % trafficu B2 a ~1,5× traffic PL.
- Po odkrytí (zobrazení/den, před → po): C 776 → 1 275 (+499; nad srpnovou špičkou 1 081); B2 911 → 755 (−156); B1 613 → 606; PL −53 (AA −12 na 92, A −41); celý web +316. Odhad: ~45 % přírůstku C je přesun z ostatních tierů, ~55 % nový traffic.
- C vs. B: 776 vs. 1 524 před → 1 275 vs. 1 361 po; C = 3× PL (426).
- 201 C produktů bez prodeje v zahraničí do 20. 9. (171 nikdy, ani v 2025) se po odkrytí prodalo, 180 z nich jen 1 ks („probuzení mrtvého skladu“).
- Kanály: přírůstek C hlavně placené Google kanály (PLA, SEA, PMAX, brand +2,7 tis. Kč/den = 60 % přírůstku); Direct + organika jen +0,5 tis. Kč/den. Podíl C v PLA 33 % → 71 %. Kanibalizace: Shopping B2 (−457 Kč/den), brand/PMAX AA (−203/−165) a B2 (−162/−111), srovnávače AA (−140), organika A (−250/−135).
- Pozor: v průběžném vyhodnocení nesedí součet (C +499 − 216 = +283, ne +316) a u „Kč/den“ není jasné, zda jde o tržby nebo marži. **Ověř aritmetiku a definice metrik a uveď je.**

### Období
- **Před (baseline):** 1. 7. – 20. 9. 2026 (zvlášť označ srpnovou špičku).
- **Po:** 21. 9. – 10. 11. 2026, rozpad: 21.–30. 9. / říjen / 1.–10. 11.
- **Meziročně:** stejná období 2025 (sezónnost – listopad = start Black Week / 11.11 akcí).
- Vyhodnocuj **průměr na den**, ne součty. Vyřaď dny s neúplnými daty.

### Metodika
1. **Difference-in-differences:** změna v zemích experimentu minus změna v CZ/SK (kontrola sezónnosti, kampaní, celkového trendu webu). Kde to jde, i po jednotlivých zemích.
2. **Vše v rozpadu tierů:** AA, A, B1, B2, C a agregace **PL (AA+A)**, **B2+C** a **celý web**.
3. **Kanibalizace vs. inkrement:** kolik z přírůstku C je přesun z jiných tierů a kolik nový objem – pro traffic, objednávky, tržby i marži.
4. U všech čísel uváděj **absolutní hodnoty i změnu** (abs. + %), CEO chce **absolutní hodnoty kategorií AA/A, B, C**.
5. Odliš korelaci od kauzality; pokud se během období měnily kampaně, ceny, feed nebo sortiment, uveď to jako rušivý vliv.

### Otázky, na které musí vyhodnocení odpovědět
**A. Traffic (aktualizace k 10. 11.)**
1. Vývoj zobrazení/den po tierech (AA, A, B1, B2, C, PL, B, web) – trend v čase, ne jen dva body. Drží se efekt, nebo slábne?
2. Přesun vs. nový traffic – aktualizace odhadu 45/55.

**B. Tržby a podíl C**
3. Navázat na graf „Průběh podílu C (+B2) v revenue 2026“ – prodloužit do 10. 11. 2026, rozpad po zemích a CZ/SK jako kontrola.
4. Objednávky, kusy, tržby, AOV, konverzní poměr po tierech.

**C. Marže (požadavek CEO)**
5. Je **celková marže (Kč/den)** díky odkrytí **vyšší nebo nižší**? Rozlož na: marže získaná z C − marže ztracená kanibalizací (zejména PL, který má typicky vyšší marži %).
6. **Marketing profit = marže − MKT1 náklady**: je vyšší nebo nižší? Po tierech, po kanálech, po zemích. Uveď, jak jsou MKT1 náklady alokovány na produkty/tiery.
7. Vliv na marži % a na mix (B2+C vs. PL).

**D. Stal se z C produktů B? (otázka CEO)**
8. Kolik C produktů po odkrytí splnilo kritéria tieru B (podle platných pravidel klasifikace ABC) – v zahraničí, v CZ/SK, celkem. Pokud reklasifikace ještě neproběhla, simuluj ji podle pravidel na datech „po“.
9. Rozlišit „jednorázové probuzení“ (1 ks) vs. **opakovaný prodej** (≥ 2 ks, ≥ 2 objednávky, prodej ve více týdnech). Aktualizovat čísla 201 / 171 / 180.
10. Top 20 C produktů podle přírůstku marže + seznam kandidátů na přeřazení do B.

**E. Marketingové kanály (Sales/MKT, Tereza)**
11. Rozpad přírůstku C a ztrát ostatních tierů po kanálech (PLA/Shopping, SEA, PMAX, brand, srovnávače, Direct, organika, e-mail).
12. Proč C tolik sebralo v Shoppingu/PMAX (podíl C v PLA 33 → 71 %)? Ověřit hypotézu: interní odkazy + zařazení do kategorie → lepší skóre produktu. Sledovat náklady, ROAS/PNO po tierech – nejde jen o přesun rozpočtu kampaní na C?
13. Organika a retence: je vidět první náběh (organická zobrazení C, opakované nákupy zákazníků, kteří poprvé koupili C)?

**F. Sklad a provoz**
14. Úbytek mrtvého skladu C v zahraničí (ks, Kč v nákupních cenách), obrátkovost před/po.
15. Rizika: vratky/reklamace C v zahraničí, vyprodání C pro CZ/SK, dopravné vs. hodnota objednávky u levných C položek.

**G. Import a varianty (Miloš)**
16. Počet EANů v seznamu vs. skutečně odkrytých (vč. dotažených variant) vs. přeskočených, s důvodem.

### Výstup
1. **TL;DR** (3–5 odrážek): traffic, tržby, marže, marketing profit, C→B.
2. Sekce A–G, každá: klíčová čísla (tabulka před/po/změna + DiD vs. CZ/SK), 1–2 věty interpretace.
3. **Závěr a doporučení:** pokračovat / upravit / zastavit; co změnit (např. zařazení C do všech podkategorií, vyloučení C z brand kampaní, kanibalizujících PL; přeřazení C→B); další termín vyhodnocení (po zařazení do podkategorií + náběhu organiky a retence, tj. ~Q1 2027).
4. **Datová omezení a předpoklady** (chybějící dny, definice metrik, alokace nákladů).
5. Styl: Basecamp komentář, oslovení „Adam, Gabriel“, česky, čísla s mezerou jako oddělovačem tisíců, Kč/den, zobrazení/den. Nevymýšlej čísla – co nelze z dat spočítat, napiš jako „chybí data: …“.

---

## Potřebná data pro vyhodnocení k 11. 11. 2026

Rozsah všech časových řad: **1. 7. 2025 – 10. 11. 2026, denně** (meziroční srovnání + baseline). Rozpad vždy: **den × země (CZ, SK, HU, BG, RO, SI, HR) × tier (AA, A, B1, B2, C)**, kde jde i × produkt (EAN/ID).

| # | Data | Zdroj | Proč |
|---|------|-------|------|
| 1 | **Seznam odkrytých produktů**: Google Sheet (EAN), log importu z 20. 9. vč. info hlášky přeskočených položek, mapování EAN → produkt/varianta/hlavní varianta | GSheet, Miloš (import) | Skutečně odkrytá množina, otázka G |
| 2 | **Historie tierů ABC** – snapshot tieru každého produktu k 20. 9. a k poslednímu přepočtu + **pravidla klasifikace** (prahy, období, metrika) a datum příští reklasifikace | Nákup / BI | Segmentace, otázka „C → B“ |
| 3 | **Traffic**: zobrazení produktů (view_item), relace, přidání do košíku po produktu/tieru/zemi/kanálu | GA4 (report Privátní značky + doplnit) | Sekce A; ověřit, že je dočtena mezera od 29. 9. |
| 4 | **Prodeje**: objednávky, kusy, tržby bez DPH, vratky/storna po produktu × zemi × dni, vč. ID zákazníka (anonymizovaně) | ERP / BI | Sekce B, D, F; retence |
| 5 | **Marže**: nákupní cena / COGS, prodejní cena, slevy, případně front/back margin po produktu × zemi × dni | ERP / BI | Sekce C |
| 6 | **MKT1 náklady** po kanálu × zemi × dni a ideálně po produktu (Google Ads shopping/PMAX product-level, srovnávače po položce) + **definice MKT1** a pravidlo alokace na tiery | Google Ads, srovnávače, Finance | Marketing profit |
| 7 | **Atribuce tržeb a marže po kanálech** (PLA/Shopping, SEA, PMAX, brand, srovnávače, Direct, organika, e-mail) × tier × země | GA4 / BI | Sekce E |
| 8 | **Google Ads výkon po produktu**: impresions, kliky, cost, konverze, hodnota konverzí; změny kampaní/rozpočtů v období (change history) | Google Ads | Otázka 12, rušivé vlivy |
| 9 | **Organika**: Search Console po URL/produktu (impr., kliky) pro zahraniční domény | GSC | Náběh organiky |
| 10 | **Sklad**: zásoba ks a hodnota v NC po produktu k 20. 9. a k 10. 11., příjmy, výdeje | WMS / ERP | Sekce F |
| 11 | **Zařazení do kategorií**: v jakých kategoriích/podkategoriích jsou C produkty, a zda/kdy proběhlo zařazení do všech podkategorií | e-shop admin / Miloš | Kontext rozsahu odkrytí |
| 12 | **Log změn v období** 1. 7. – 10. 11. 2026: cenové změny, akce (Black Week, 11.11), změny feedů, nové kampaně, výpadky webu | Marketing, Nákup | Rušivé vlivy |
| 13 | Podklady z průběžného vyhodnocení (data k 6. 10.) a graf „podíl C (+B2) v revenue 2026“ | Jan | Navázání a kontrola aritmetiky |

### Otevřené otázky k ujasnění před spuštěním
1. „SL“ v seznamu zemí = Slovinsko (SI)? (předpoklad: ano)
2. Proběhlo už zařazení C do všech podkategorií? Pokud ano, od kdy – rozdělí to období „po“ na dvě fáze.
3. Byla doplněna GA4 data od 29. 9.?
4. Co přesně zahrnuje MKT1 a jak se alokuje na produkty?
5. Je „Kč/den“ v průběžném vyhodnocení tržba, nebo marže?
