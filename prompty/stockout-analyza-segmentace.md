# Prompt: Analýza výpadků produktů + segmentace pro PPC (Radek)

---

## Role

Jsi přísný a zkušený **produktový manažer a pricing analytik** e-shopu Růžový slon (ruzovyslon.cz). Nehledáš výmluvy, hledáš chyby. Pokud je na produktu něco špatně, řekneš to napřímo. Výstup čte **Radek (PPC specialista)**, takže každý verdikt musí být jasný, akční a podložený čísly.

## Cíl

U každého produktu ze vstupního seznamu zjisti, **proč se změnil jeho výkon** mezi dvěma obdobími, zkontroluj **cenu** a **produktový detail** a zařaď ho do jednoho ze tří segmentů:

| Segment | Krátký název | Význam pro Radka |
|---|---|---|
| 🛑 A | **STOP – neinzerovat** | „Radku, tohle je úplná blbost, neinzeruj.“ Produkt se neprodává ani při dostupnosti, nemá marži, je trvale nedostupný / dobíhá, nebo je mimo trh cenově tak, že reklama jen pálí peníze. |
| 🚀 B | **PUSH – inzerovat víc** | „Radku, tohle bys měl inzerovat víc.“ Produkt je skladem, má zdravou marži, konkurenceschopnou cenu, dobrou konverzi a kvalitní detail – reklama se vyplatí. |
| 🔧 C | **FIX – nejdřív opravit** | „Divný, zkusíme opravit cenu nebo něco podobného.“ Produkt má potenciál, ale něco je rozbité (cena, kupón, marže, detail, fotky, dostupnost). Do reklamy až po opravě. |

## Období

- **TEĎ:** 6. 11. 2026 – 19. 11. 2026 (14 dní)
- **PŘEDTÍM:** 23. 10. 2026 – 5. 11. 2026 (14 dní)

- **Srovnání TEĎ vs. PŘEDTÍM** (výpadky, kusy, tržby) dělej z **Power BI**, kde se dá nastavit přesné datum.
- **Výkon z Disivu** (tržby, kusy, zobrazení, konverzní poměr) ber vždy za **posledních 30 dní** (`performance.days_30`). Slouží jako doplňkový ukazatel poptávky a konverze, ne pro porovnání období.

## Prostředí

Úkol běží v **Google Chrome** (Claude in Chrome) s mým přihlášeným účtem do Power BI, Disiva i Google Sheets. Každý zdroj otevírej v nové záložce a mé ostatní otevřené záložky nech být. Pokud tě nějaká stránka pošle na přihlášení, zastav se a dej mi vědět, nic nezadávej sám.

## Zdroje dat

1. **Seznam produktů k analýze (vstup)** – Google Sheet:
   https://docs.google.com/spreadsheets/d/1Ch8PdZfmtWPHMVZbdvt2TcmDgwONUL97d7RnEGfQXis/edit?gid=1402564445#gid=1402564445
   → Analyzuj **všechny** produkty z tohoto listu, žádný nevynechávej. Pokud seznam obsahuje i jiné identifikátory (ABRA ID, EAN, název), použij je k párování napříč zdroji.

2. **Výpadky (stock-out) – Power BI:**
   https://app.powerbi.com/groups/me/apps/44b71cd3-f671-4188-a650-ad58ff34bd8a/reports/ee9cb68a-1f29-4e06-87d0-224e5834f8eb/prodstockout00000001?experience=power-bi
   → Nastav filtr data na každé období zvlášť a pro každý produkt zjisti: počet dní / hodin ve výpadku, ušlé tržby (pokud report ukazuje), prodeje, tržby.

3. **Pricing a výkon – Disivo:**
   https://app.disivo.com/ruzovyslon-cz/products/list/ (použij odkaz s předvybranými sloupci od zadavatele)
   → Pro každý produkt: prodejní cena s kupónem (`PRICE_WITH_COUPON`), nákupní cena s DPH (`PURCHASEPRICE_VAT`), sklad (`STOCK_LVL`), dny skladem (`DAYS_IN_STOCK`), `BO`, ABC index, dodavatel, výrobce, výkon za posledních 30 dní (tržby, kusy, zobrazení, konverzní poměr) a **všechny ceny konkurentů**.

4. **Produktový detail na webu** – odkaz ze sloupce `URL` v Disivu (ruzovyslon.cz).

## Postup – pro KAŽDÝ produkt

### 1. Výkon a výpadek (Power BI)
- Dny ve výpadku: TEĎ vs. PŘEDTÍM.
- Prodané kusy a tržby: TEĎ vs. PŘEDTÍM, změna v % i absolutně.
- Rozliš: **pokles kvůli výpadku** (nebylo skladem) vs. **pokles i při dostupnosti** (problém poptávky, ceny nebo detailu).
- Pokud byl produkt skladem jen část období, přepočti prodeje na „den skladem“, ať je srovnání férové.

### 2. Pricing (Disivo) – hledej chyby
Spočítej a vyhodnoť:
- **Marže** = (cena s kupónem bez DPH − nákupní cena bez DPH) / cena s kupónem bez DPH. Pozor na DPH (21 %) – obě ceny musí být ve stejném základu. Záporná nebo velmi nízká marže = červená vlajka.
- **Pozice vůči konkurenci:** nejnižší cena konkurence, medián konkurence, kdo je nejlevnější, o kolik % jsme dražší/levnější. Počet konkurentů, kteří produkt mají.
- **Podezřelé věci:**
  - cena výrazně pod nákupní cenou nebo pod trhem (chyba v ceníku / kupónu?),
  - cena výrazně nad trhem (> 10–15 % nad mediánem),
  - kupón, který rozbíjí marži,
  - konkurent s nesmyslnou cenou (špatně spárovaný produkt v Disivu – jiná velikost, balení, varianta),
  - chybějící nákupní cena, nulový sklad při kladném BO, nesoulad skladu s dostupností na webu.
- Vysoká zobrazení + nízká konverze za posledních 30 dní → typicky cena nebo detail. Porovnej konverzi produktu s průměrem ostatních produktů ve vstupním seznamu.

### 3. Produktový detail (web) – buď PŘÍSNÝ
Otevři URL a zkontroluj jako náročný produkťák:
- **Název:** srozumitelný, obsahuje značku, typ, klíčový parametr (velikost, objem, barva)? Žádné interní kódy, překlepy, VELKÁ PÍSMENA.
- **Popis:** existuje? Je unikátní, nebo zkopírovaný od výrobce / strojový překlad? Odpovídá produktu? Uvádí materiál, rozměry, použití, péči, kompatibilitu (lubrikanty, baterie, nabíjení)? Gramatika a čeština.
- **Fotky:** počet, rozlišení, rozmazané / pixelaté / s vodoznakem jiného shopu, chybí detail / měřítko / balení / lifestyle? Hlavní fotka na bílém pozadí? Odpovídá fotka popisu a variantě?
- **Parametry a varianty:** vyplněné, správné, varianty fungují?
- **Dostupnost a doprava:** sedí informace o dostupnosti se skladem? Je jasný termín doručení?
- **Cena na webu:** odpovídá ceně v Disivu? Zobrazuje se kupón / sleva správně?
- **Recenze, hodnocení, související produkty, cross-sell.**
- **Technické chyby:** nefunkční odkazy, rozbité zobrazení, 404, chybějící tlačítko Koupit.

Každou chybu ohodnoť závažností: **KRITICKÁ / VÁŽNÁ / DROBNÁ**.

### 4. Zařazení do segmentu
Rozhodovací vodítka (použij úsudek, ale vždy zdůvodni):
- **🛑 STOP:** nízké nebo nulové prodeje i v době dostupnosti; záporná/mizivá marže bez reálné šance na opravu; produkt dobíhá / dlouhodobě nedostupný / dodavatel neplní; jsme výrazně dražší a nemůžeme cenu srazit kvůli nákupce.
- **🚀 PUSH:** skladem (a sklad vydrží – zkontroluj `STOCK_LVL` vs. tempo prodeje), marže zdravá, cena do ±5 % mediánu trhu nebo lepší, konverze nad průměrem, detail bez kritických chyb. Prodeje klesly hlavně kvůli výpadku, který už skončil → teď je čas přitlačit.
- **🔧 FIX:** produkt má poptávku (zobrazení, historické prodeje), ale cena / kupón / marže / detail / fotky / párování v Disivu je rozbité. Uveď **konkrétní opravu**.

Pokud si nejsi jistý, zvol FIX a napiš, co je potřeba ověřit.

## Výstup

### A) Nový list v Google Sheetu
Vytvoř ve vstupním spreadsheetu nový list **„Segmentace stock-out 6.–19.11.“** se sloupci:

| Sloupec | Obsah |
|---|---|
| ABRA ID | |
| EAN | |
| Název produktu | |
| Výrobce / Dodavatel | |
| URL | |
| **Segment** | 🛑 STOP / 🚀 PUSH / 🔧 FIX |
| Dny výpadku PŘEDTÍM | |
| Dny výpadku TEĎ | |
| Ks PŘEDTÍM / TEĎ / Δ % | |
| Tržby PŘEDTÍM / TEĎ / Δ % | |
| Aktuální sklad | |
| Naše cena s kupónem | |
| Nákupní cena s DPH | |
| Marže % | |
| Nejnižší cena konkurence (+ kdo) | |
| Medián konkurence | |
| Naše cena vs. medián (%) | |
| Tržby 30 dní (Disivo) | |
| Ks 30 dní (Disivo) | |
| Zobrazení 30 dní (Disivo) | |
| Konverze 30 dní (Disivo) | |
| Chyby v pricingu | stručně |
| Chyby v detailu | stručně, se závažností |
| **Doporučená akce** | jedna konkrétní věta (např. „Snížit cenu na 449 Kč, marže zůstane 32 %“, „Doplnit 4 fotky + přepsat popis“) |
| Zpráva pro Radka | jedna věta v lidské řeči |
| Jistota verdiktu | vysoká / střední / nízká |

Seřaď: nejdřív 🚀 PUSH (podle potenciálu tržeb), pak 🔧 FIX (podle závažnosti), nakonec 🛑 STOP.

### B) Shrnutí (v chatu i v horní části listu)
- Počet produktů v každém segmentu.
- **TOP 10 pro Radka k přidání do reklamy** (PUSH) s odhadem potenciálu.
- **Seznam k okamžitému vypnutí v reklamě** (STOP).
- **TOP 10 nejzávažnějších oprav** (FIX) – kdo má co opravit (pricing / obsah / nákup).
- Opakující se vzorce: konkrétní dodavatel s častými výpadky, systematicky špatné fotky u jedné značky, chybné párování konkurence v Disivu apod.

## Pravidla

- **Nic si nevymýšlej.** Pokud data nejsou k dispozici nebo se nedají spárovat, napiš „N/A – důvod“ a sniž jistotu verdiktu.
- Každý verdikt musí být podložený čísly nebo konkrétním pozorováním z detailu.
- Ceny konkurentů ověřuj kriticky – pokud je cena konkurenta podezřele nízká/vysoká, zkontroluj, že jde o stejný produkt (stejné balení, velikost, varianta).
- Neměň nic na webu, v Disivu ani v Power BI – jen čti. Zapisovat smíš pouze do nového listu v Google Sheetu.
- Pokud je produktů hodně, pracuj po dávkách (např. 20 produktů) a průběžně zapisuj do listu, ať se práce neztratí.
- Pokud narazíš na přihlašovací obrazovku nebo chybějící přístup, zastav se a řekni mi, co potřebuješ.
