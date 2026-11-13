# Prompt: Vyhodnocení odkrytí C produktů v zahraničí (k 11. 11. 2026)

> Zdroj: Basecamp to-do „Odkrytí C produktů v zahraničí“ (bucket 40643108, to-do 10272661744) včetně všech komentářů 4. 9. – 16. 10. 2026.
> Použití: vložit celý blok „PROMPT“ do AI a přiložit datové soubory podle sekce „Potřebná data“.

---

## PROMPT

### Role
Jsi senior analytik e-commerce (nákup + výkonnostní marketing). Připravuješ vyhodnocení experimentu „odkrytí C produktů v zahraničí“ pro CEO (Adam Durčák), nákup (Jan Bezecný) a automatizaci (Miloš Murárik), v kopii Gabriel a marketing (Tereza). Výstup bude vložen jako komentář do Basecampu, česky, stručně, s čísly.

### Rozsah – striktně dodržet
- **Pouze BO tier „C“.** Na otázky o jiných tierech (AA, A, B1, B2, private label, kanibalizace) **neodpovídáme**. Ostatní tiery ani celý web nepočítej a nekomentuj.
- **Pouze zahraniční trhy Sexy Elephant:** HU, SI, HR, RO, BG (+ „BO“ dle zadání – viz otevřené otázky). Website filtr = všechny weby **kromě** ruzovyslon.cz, ruzovyslon.sk, kondomshop.cz, kondomshop.sk, flagranti.cz, flagranti.sk. CZ/SK a weby Růžový slon nepoužívej ani jako kontrolu.
- **Produkty:** EANy z Google Sheetu „Produkty k odkrytí v zahraničí 11.9.2026“ (~6 350 EAN, odkrytí pro všechny uvedené země).

### Kontext experimentu
- C produkty byly v zahraničí skryté, **20. 9. 2026 odkryty importem** (parametr „Zobrazit v listingu“). První plný den efektu = **21. 9. 2026**.
- **Varianty:** odkrytí jedné varianty odkryje všechny včetně hlavní; položky s konfliktem (jedna varianta skrýt, druhá odkrýt) import přeskočil. Pracuj se skutečně odkrytou množinou a rozdíl oproti seznamu vyčísli.
- **Rozsah odkrytí:** C je zatím zařazené **jen v hlavní kategorii**, ne ve všech podkategoriích. Plný efekt (vč. organiky a retence) se čeká až po zařazení do podkategorií a s odstupem několika měsíců – interpretuj jako efekt částečného odkrytí.
- **Známý datový problém:** v GA4 reportu se nedočítala data od 29. 9. 2026 – ověř úplnost, neúplné dny vyřaď a uveď to.

### Co už víme (průběžné vyhodnocení k 6. 10. 2026, jen C) – aktualizuj
- Do 20. 9. mělo C stabilní traffic, srpnová špička 1 081 zobrazení/den.
- Po odkrytí: C 776 → 1 275 zobrazení/den (+499), nejvyšší hodnota za sledované období.
- 201 C produktů bez prodeje v zahraničí do 20. 9. (171 nikdy, ani v 2025) se po odkrytí prodalo, 180 z nich jen 1 ks („probuzení mrtvého skladu“).
- Přírůstek C hlavně z placených Google kanálů (PLA, SEA, PMAX, brand +2,7 tis. Kč/den = 60 % přírůstku); Direct + organika +0,5 tis. Kč/den. Podíl C v PLA 33 % → 71 %.
- Ověř, zda „Kč/den“ znamená tržby, nebo marži, a uveď definici.

### Období
- **Před:** 1. 7. – 20. 9. 2026. **Po:** 21. 9. – 10. 11. 2026 (rozpad 21.–30. 9. / říjen / 1.–10. 11.).
- **Meziročně:** stejná období 2025 jako kontrola sezónnosti (listopad = Black Week / 11.11).
- Vše jako **průměr na den**, absolutní hodnoty + změna (abs. i %), po zemích i celkem.

### Otázky (jen C, jen zahraničí SE)
**A. Traffic** – vývoj zobrazení/den C v čase (drží se efekt, nebo slábne?), po zemích; YoY.
**B. Tržby** – objednávky, kusy, tržby, AOV, konverzní poměr C; prodloužit graf „Průběh podílu C v revenue 2026“ do 10. 11.
**C. Marže (CEO)** – je marže C (Kč/den) díky odkrytí vyšší? **Marketing profit C = marže − MKT1 náklady** na C: vyšší, nebo nižší? Po kanálech a zemích; uveď, jak jsou MKT1 náklady přiřazeny k C.
**D. Stal se z C produktů B? (CEO)** – kolik C produktů po odkrytí splňuje kritéria tieru B (dle pravidel klasifikace; pokud reklasifikace neproběhla, simuluj). Rozliš jednorázové „probuzení“ (1 ks) vs. opakovaný prodej (≥ 2 objednávky, ve více týdnech). Aktualizuj 201 / 171 / 180. Top 20 C produktů dle tržeb/marže + kandidáti na přeřazení do B.
**E. Kanály (Tereza)** – přírůstek C po kanálech (PLA/Shopping, SEA, PMAX, brand, srovnávače, Direct, organika, e-mail); proč C tolik roste v Shoppingu/PMAX (hypotéza: zařazení do kategorie + interní odkazy → lepší skóre); náklady a ROAS/PNO C – nejde jen o přesun rozpočtu?
**F. Organika a retence** – první známky náběhu (organická zobrazení C, opakované nákupy zákazníků, kteří poprvé koupili C).
**G. Sklad** – úbytek mrtvého skladu C v zahraničí (ks, Kč v NC).
**H. Import (Miloš)** – EANy v seznamu vs. skutečně odkryté (vč. variant) vs. přeskočené.

### Výstup
1. **TL;DR** (3–5 odrážek): traffic, tržby, marže, marketing profit, C → B.
2. Sekce A–H: tabulka před/po/změna (+ YoY), 1–2 věty interpretace.
3. **Závěr a doporučení:** pokračovat / upravit (zařazení C do všech podkategorií, přeřazení C → B) + termín dalšího vyhodnocení (~Q1 2027).
4. **Datová omezení** (chybějící dny, definice, alokace nákladů).
5. Styl Basecamp komentáře, oslovení „Adam, Gabriel“, česky, Kč/den, zobrazení/den. Nevymýšlej čísla – co nejde spočítat, napiš „chybí data: …“.

---

## Zdroje dat

| # | Data | Zdroj | Nastavení |
|---|------|-------|-----------|
| 1 | Seznam EAN (C produkty k odkrytí) | Google Sheet „Produkty k odkrytí v zahraničí 11.9.2026“ (`1g8m_jtJmHdE8QrXTpawsNlKj59ZSW6pbx0hpD8ztYmk`) | – |
| 2 | GA data (traffic, kanály) | Power BI report `55d1c0d4-98d7-4af0-a7d9-df94ea364fb9` | filtr „zahraničí“, datum 1. 7. 2025 – 10. 11. 2026 |
| 3 | GA data per SKU | Power BI report `a983c457-ff52-4cec-94c3-deaec4530d31` | website: vše kromě ruzovyslon.cz/.sk, kondomshop.cz/.sk, flagranti.cz/.sk; datum 1. 7. 2025 – 10. 11. 2026 |
| 4 | BO tier (jen C) + pravidla klasifikace | BI / Nákup | stav k 20. 9. a po posledním přepočtu |
| 5 | Sales: objednávky, kusy, tržby bez DPH, marže/NC, vratky, anonym. ID zákazníka | BI | den × země × SKU, jen C, jen SE weby |
| 6 | MKT1 náklady na C (Google Ads per produkt, srovnávače) | Google Ads / BI | den × země × kanál |
| 7 | Sklad C v zahraničí (ks, NC) k 20. 9. a 10. 11. | ERP/WMS | – |
| 8 | Log importu 20. 9. (přeskočené položky) | Miloš | – |

Export z Power BI: u vizuálu „…“ → *Export data* → *Summarized/Underlying data* (.xlsx/.csv), granularita den × země × SKU × kanál.

### Otevřené otázky
1. „BO“ v seznamu trhů = ? (Seznam SKU obsahuje sloupce HU, BG, HR, SL, RO; předpoklad: překlep, platí HU, SI, HR, RO, BG.)
2. Proběhlo už zařazení C do všech podkategorií? Pokud ano, od kdy?
3. Byla doplněna GA4 data od 29. 9.?
4. Co přesně zahrnuje MKT1?
