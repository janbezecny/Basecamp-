# Prompt: Vyhodnocení odkrytí C produktů v zahraničí k 11. 11. 2026

> Zdroj zadání: Basecamp to-do „Odkrytí C produktů v zahraničí“ (bucket 40643108, to-do 10272661744), komentáře 4. 9. – 16. 10. 2026.
> Použití: vložit blok „PROMPT“ do AI, která má přístup k Power BI reportům, nebo k němu přiložit exporty podle sekce „Data k dodání“.

---

## PROMPT

Připravuješ velké vyhodnocení experimentu „odkrytí C produktů v zahraničí“ k 11. 11. 2026. Čtenáři jsou CEO (Adam Durčák), nákup (Jan Bezecný), automatizace (Miloš Murárik), Gabriel a marketing (Tereza). Experiment znají, ale neviděli data od 6. 10. Výsledek půjde jako komentář do Basecampu a rozhoduje se podle něj, jestli odkrytí nechat, rozšířit do všech podkategorií a které C produkty přeřadit do B.

### Rozsah

Vyhodnocuj jen to, co spadá do všech tří vymezení současně. Vše ostatní vynech, i kdyby to data nabízela.

- **Tier:** pouze BO tier **C**. Ostatní tiery (AA, A, B1, B2), private label, celý web ani kanibalizaci mezi tiery nepočítej a nekomentuj. Bylo to tak rozhodnuto; CEO navíc bere B2 a C jako téměř totéž.
- **Trhy:** pouze zahraniční weby Sexy Elephant: HU, SI, HR, RO, BG. Weby ruzovyslon.cz, ruzovyslon.sk, kondomshop.cz, kondomshop.sk, flagranti.cz a flagranti.sk do analýzy nepatří, ani jako kontrolní skupina.
- **Produkty:** EANy z Google Sheetu „Produkty k odkrytí v zahraničí 11.9.2026“ (asi 6 350 EAN, odkrytí platí pro všechny uvedené země).

### Co se stalo

- C produkty byly na zahraničních webech skryté z listingu. **20. 9. 2026 je import odkryl** (parametr „Zobrazit v listingu“), první plný den efektu je **21. 9. 2026**.
- Odkrytí jedné varianty odkryje všechny varianty včetně hlavní. Položky, kde měla jedna varianta „skrýt“ a jiná „odkrýt“, import přeskočil. Skutečně odkrytá množina se proto od seznamu liší oběma směry.
- C produkty jsou zatím zařazené jen v hlavní kategorii, ne v podkategoriích. Plný efekt se čeká až po zařazení do všech podkategorií a po několika měsících, kdy naběhne organika a retence. Výsledky tedy popisují částečné odkrytí po sedmi týdnech.
- V GA4 reportu se od 29. 9. 2026 nedočítala data. Než začneš počítat, ověř po dnech, že je řada úplná. Neúplné dny vyřaď a napiš které.

### Stav k 6. 10. 2026 (průběžné vyhodnocení)

Tato čísla ber jako kontrolní bod. Nejdřív je na stejném období zreprodukuj. Pokud ti vyjdou výrazně jinak, napiš rozdíl a jeho pravděpodobnou příčinu (jiný filtr, jiná metrika) dřív, než budeš pokračovat.

- Traffic C: 776 → 1 275 zobrazení/den (+499), nejvyšší hodnota za sledované období včetně srpnové špičky (1 081).
- 201 C produktů, které se do 20. 9. v zahraničí neprodávaly (171 z nich nikdy, ani v roce 2025), se po odkrytí prodalo; 180 z nich po jediném kusu.
- Přírůstek C přišel hlavně z placených Google kanálů: PLA, SEA, PMAX a brand dohromady +2,7 tis. Kč/den, tj. 60 % přírůstku. Direct a organika +0,5 tis. Kč/den. Podíl C v PLA vzrostl z 33 % na 71 %.
- U „Kč/den“ není v průběžném vyhodnocení řečeno, zda jde o tržby, nebo marži. Zjisti to z dat a u každé peněžní metriky uváděj, co přesně znamená.

### Zdroje dat

1. **GA report (Power BI):** https://app.powerbi.com/groups/me/apps/44b71cd3-f671-4188-a650-ad58ff34bd8a/reports/55d1c0d4-98d7-4af0-a7d9-df94ea364fb9/3f2f3737d53fdc3817e1?experience=power-bi
   Ve filtraci zatrhni „zahraničí“. Datum nastav podle období níže.
2. **GA report per SKU (Power BI):** https://app.powerbi.com/groups/me/apps/44b71cd3-f671-4188-a650-ad58ff34bd8a/reports/a983c457-ff52-4cec-94c3-deaec4530d31/61708e1e317e2bd35f1a?experience=power-bi
   Website: vše kromě ruzovyslon.cz, ruzovyslon.sk, kondomshop.cz, kondomshop.sk, flagranti.cz, flagranti.sk. Data jsou zde i po SKU.
3. **Seznam EAN:** Google Sheet „Produkty k odkrytí v zahraničí 11.9.2026“ – https://docs.google.com/spreadsheets/d/1g8m_jtJmHdE8QrXTpawsNlKj59ZSW6pbx0hpD8ztYmk
4. **BO tier** (jen skupina C) a **sales data** – přiložené exporty.

Pokud se k některému zdroji nedostaneš, nehádej a nenahrazuj ho odhadem. Napiš, který zdroj chybí a jaký export potřebuješ (granularita den × země × SKU × kanál).

### Období a srovnání

- **Před:** 1. 7. – 20. 9. 2026.
- **Po:** 21. 9. – 11. 11. 2026. Uváděj i po týdnech od odkrytí, aby bylo vidět, jestli efekt drží, roste, nebo vyprchává.
- **Sezónnost:** kontrolní skupinu z jiných trhů nemáme, proto srovnávej meziročně. Spočítej poměr „po / před“ pro rok 2026 a pro stejná okna roku 2025; rozdíl těchto poměrů je odhad efektu odkrytí očištěný o sezónu. Listopadové dny označ zvlášť, začínají v nich akce (11. 11., Black Week).
- **Kontrola uvnitř C:** pokud v datech existují C produkty, které na seznamu nebyly (byly viditelné už dřív nebo zůstaly skryté), použij je jako srovnávací skupinu a řekni, jak je velká.
- Všechno počítej jako průměr na den. U každé metriky uveď hodnotu před, po, změnu absolutně i v procentech. Celkem za všech pět trhů a zvlášť po zemích.

### Na co má vyhodnocení odpovědět

**1. Traffic C.** Absolutní zobrazení/den před a po, vývoj po týdnech, po zemích. Drží se úroveň 1 275/den z 6. 10.? Kolik SKU ze seznamu má po odkrytí aspoň jedno zobrazení a kolik jich před odkrytím nemělo žádné?

**2. Tržby C.** Objednávky, kusy, tržby bez DPH, průměrná cena kusu a konverzní poměr. Prodluž řadu „podíl C v revenue 2026“ do 11. 11.

**3. Marže C** (otázka CEO). Je marže z C produktů v Kč/den po odkrytí vyšší, nebo nižší, a o kolik? Uveď i marži v procentech; změnila se, například kvůli výprodejovým cenám mrtvého skladu?

**4. Marketing profit C** (otázka CEO). Marketing profit = marže − MKT1 náklady. Je po odkrytí vyšší, nebo nižší? Rozpad po kanálech a zemích. Napiš, jak jsou MKT1 náklady k C produktům přiřazeny (přímo po produktu, nebo klíčem), protože na tom stojí spolehlivost výsledku.

**5. Stala se z některých C produktů B?** (otázka CEO)
- Rozděl SKU ze seznamu podle prodejů po odkrytí: 0 ks, 1 ks, 2–4 ks, 5 a více ks; u prodávaných i počet objednávek a počet týdnů s prodejem.
- Aktualizuj čísla 201 / 171 / 180: kolik dříve neprodávaných produktů se prodalo a kolik z nich opakovaně.
- Podle pravidel BO klasifikace urči, kolik C produktů by dnes splnilo kritéria B. Pokud pravidla nemáš, napiš to, a jako kandidáty označ produkty s opakovaným prodejem ve více týdnech.
- Přilož seznam 20 nejsilnějších C produktů podle marže (při chybějící marži podle tržeb) jako kandidáty na přeřazení.
- Jak koncentrovaný je přírůstek: jaký podíl tržeb C dělá horních 10 % SKU?

**6. Kanály** (pro Terezu). Přírůstek C po kanálech: PLA/Shopping, SEA, PMAX, brand, srovnávače, Direct, organika, e-mail. Platí stále, že většinu dělají placené Google kanály? Ověř hypotézu z průběžného vyhodnocení, že C získalo výkon v Shoppingu a PMAX díky zařazení do kategorie a interním odkazům. Rozliš, zda C produkty dostaly víc impresí a kliků při podobné ceně za klik, nebo se na ně jen přesunul rozpočet kampaní. Uveď náklady a PNO/ROAS C před a po.

**7. Organika a retence.** Jsou vidět první známky? Organická zobrazení a tržby C po týdnech; kolik zákazníků, kteří po 21. 9. poprvé koupili C produkt, nakoupilo znovu. Sedm týdnů je na závěr málo, stačí říct, kterým směrem to jde.

**8. Mrtvý sklad.** Kolik kusů a jaká hodnota v nákupních cenách se z dříve neprodejných C produktů prodala.

**9. Import a varianty** (pro Miloše). Počet EAN v seznamu, počet skutečně odkrytých včetně dotažených variant a počet přeskočených s důvodem. Pokud log importu nemáš, napiš to.

### Podoba výstupu

Komentář do Basecampu, česky, oslovení „Adam, Gabriel“. Čtenář má nejdřív dostat odpovědi, potom podklady:

1. **Shrnutí** v 4–6 odrážkách: traffic, tržby, marže, marketing profit, C → B, doporučení. Každá odrážka s číslem.
2. **Části 1–9**, každá s krátkou tabulkou (před / po / změna / meziroční očištění) a jednou až dvěma větami, co z toho plyne.
3. **Doporučení:** nechat běžet, nebo upravit; zda zařadit C do všech podkategorií; které produkty přeřadit do B; kdy vyhodnotit znovu (až po zařazení do podkategorií a náběhu organiky a retence).
4. **Omezení dat:** vyřazené dny, chybějící zdroje, způsob alokace nákladů, vše, co je odhad.

Čísla piš s mezerou jako oddělovačem tisíců, jednotky Kč/den a zobrazení/den. U každého závěru rozliš, co je změřeno a co je interpretace. Co z dat spočítat nejde, uveď jako „chybí data: …“ a nevymýšlej náhradní číslo.

---

## Data k dodání

AI v tomto prostředí se do Power BI nedostane (síť hostitele blokuje a report vyžaduje přihlášení). Pro výpočet jsou potřeba exporty, všechny za **1. 7. 2025 – 11. 11. 2026 po dnech**:

| # | Data | Zdroj | Granularita |
|---|------|-------|-------------|
| 1 | GA report, filtr „zahraničí“ | Power BI report 1 | den × země × kanál; zobrazení produktů, relace, tržby |
| 2 | GA report per SKU, weby dle filtru | Power BI report 2 | den × web × SKU (× kanál, pokud jde) |
| 3 | BO tier – skupina C + pravidla, kdy je produkt B | BI / Nákup | SKU, tier k 20. 9. a po posledním přepočtu |
| 4 | Sales data | BI | den × země × SKU; objednávky, kusy, tržby bez DPH, marže nebo nákupní cena, vratky, anonymizované ID zákazníka |
| 5 | MKT1 náklady na C | Google Ads / BI | den × země × kanál, ideálně po produktu |
| 6 | Sklad C (ks, nákupní ceny) k 20. 9. a 11. 11. | ERP | SKU |
| 7 | Log importu z 20. 9. s přeskočenými položkami | Miloš | – |

Export z Power BI: u tabulky „…“ → *Export data* → *Underlying data* (.xlsx nebo .csv).

## Otevřené otázky

1. Co znamená „BO“ ve výčtu trhů HU, BO, SI, HR, RO, BG? Seznam SKU má jen HU, BG, HR, SL, RO; prompt počítá s těmito pěti.
2. Jsou už C produkty zařazené do všech podkategorií? Pokud ano, od kdy (rozdělí to období „po“ na dvě fáze).
3. Jsou v GA4 dočtená data od 29. 9.?
4. Co přesně patří do MKT1 a kde ty náklady jsou?
5. Kde jsou sales data (odkaz zatím nepřišel)?
