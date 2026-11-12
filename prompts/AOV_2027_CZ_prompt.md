# Prompt: AOV 2027 – CZ e-shop (2 nejlepší modely + forecast 2027)

> Konsolidovaná verze předchozí vícekrokové konverzace. Vložte celý blok níže do nového chatu
> a přiložte uvedené soubory. Hodnoty v hranatých závorkách upravte, pokud se změnily.

---

```text
ROLE
Jsi senior analytik pro forecasting e-commerce KPI. Pracuješ samostatně, výpočty děláš v Pythonu
(pandas, statsmodels) a výstup dodáš jako jeden Excel se živými vzorci + stručné shrnutí v chatu.
Odpovídej česky, čísla v Kč s mezerou jako oddělovačem tisíců.

CÍL
Najdi 2 nejlepší použitelné modely průměrné hodnoty objednávky (AOV) pro CZ e-shop a dej jejich
forecast na rok 2027 (měsíčně I–XII/2027 + roční hodnota + pásmo). Jeden model na GA/BI bázi,
jeden na sales/ERP bázi. Výběr musí být podložen backtestem, ne intuicí.
Modeluješ pouze CZ eshop. Jiné existující forecasty/plány nepoužívej a nesrovnávej se s nimi.

VSTUPNÍ DATA (přiložena)
1) BI exporty „AOV allocated“ – měsíčně per kanál, CZ eshop, I/2025–X/2026, ~24 kanálů.
   Filtr exportu: E-shop = CZ eshop, DivisionSubType = eshop.
   Soubory (22 měsíců):
   - 2025: Leden_AOV_2025_2.xlsx, Únor_AOV_2025.xlsx, Březen_AOV_2025.xlsx, Duben_AOV_2025.xlsx,
     Květen_AOV_2025.xlsx, Červen_AOV_2025.xlsx, Červenec_AOV_2025.xlsx, Srpen_AOV_2025.xlsx,
     Září_AOV_2025.xlsx, Říjen_AOV_2025.xlsx, Listopad_AOV_2025.xlsx, Prosinec_AOV_2025.xlsx
     (každý soubor = 1 měsíc, list Sheet1)
   - 2026 I–V: Leden_AOV_2026.xlsx, Únor_AOV_2026.xlsx, Březen_AOV_2026.xlsx,
     Duben_AOV_2026.xlsx, Květen_AOV_2026.xlsx (list Sheet1)
   - 2026 VI–X: AOV_data_2025-2026.xlsx – jeden soubor, měsíc = list:
     Sheet1 (4) = VI/2026, Sheet1 (3) = VII, Sheet1 (2) = VIII, Sheet1 (1) = IX, Sheet1 = X/2026
   Sloupce: Channel, Sales allocated, Orders allocated, AOV allocated, GM1 allocated, Ads costs,
   PNO allocated, Orders measured (+ estimated varianty – nepoužívat).
   AOV = Sales allocated / Orders allocated (ověř na všech řádcích).
   Báze obsahuje produkty + služby (poštovné, balné).
2) „Vývoj AOV 2023-2026 CZ SK HU.xlsx“ – měsíční produktové AOV (sales/ERP, BEZ služeb),
   I/2023–X/2026. Použij jen list/řadu CZ.

DŮLEŽITÉ VLASTNOSTI DAT (ošetři)
- Říjen 2026 v BI = jen 1.–30. 10. → pro AOV bez vlivu, objemy jsou neúplné.
- Listopad–prosinec 2026 nejsou skutečnost → nejdřív je dopočítej (viz krok 4).
- BI vs. ERP: báze se liší definicí objednávek (BI alokované, ERP realizované) i obsahem
  (BI včetně služeb). Porovnávej růsty, ne koruny. Spočti měsíční koeficient k = AOV BI / AOV ERP
  a jeho stabilitu; služby z těchto dat přímo izolovat nejde – uveď to jako omezení.
- Roční AOV počítej vážené objednávkami; jako váhy použij Orders allocated z BI
  (pro 2023–2024 ERP řady prostý průměr).
- Kanály agreguj do 7 skupin: Brand (paid+organic sloučeně – atribuce mezi nimi skáče),
  Organic non-brand, Direct, Paid search non-brand, Shopping/Pmax/srovnávače,
  CRM (Newsletter+SMS), Social/Affil/Referral/Other.
- Ověř podezřelé měsíce (např. leden–únor 2026 slabé, červenec 2026 anomálně silný,
  propad IX–X 2026).

CÍL RŮSTU TRŽEB 2027 (YoY, pro výpočet implikací)
Měsíc:     1    2    3    4    5    6    7    8    9   10   11   12  CELKEM
CZ eshop:  5%   5%   5%  10%  10%   5%   8%   8%   5%   5%   5%   5%   6%
SK eshop: 15%  15%  15%  15%  15%  15%  15%  15%  15%  15%  15%  15%  15%
(SK jen pro kontext – modeluje se pouze CZ.)

POSTUP
1) Načti a sjednoť data, zkontroluj AOV = Sales/Orders, spočti sezónní indexy, YoY, LTM,
   klouzavý 12M průměr. Pro BI rozlož meziroční změnu AOV na mixový a vnitrokanálový efekt.
2) Kandidátní modely:
   GA/BI báze:
   - A0 sezónní naivní (= stejný měsíc loni)
   - A1 sezónní naivní × YoY posledních známých měsíců
   - A  top-down: sezónní profil × trend z log-lineární regrese s měsíčními dummy
   - B1 bottom-up mix: Σ (podíl objednávek skupiny × AOV skupiny), mix LTM
   - B3 bottom-up mix s mixem posledních 4 měsíců
   - ensemble A1+B1
   ERP báze (časová řada 2023–2026):
   - TS1 Holt-Winters / ETS(A,N,A) bez trendu, α=γ=0,1 (+ varianta s optimalizovanými parametry)
   - TS2 SARIMA(0,1,1)(0,1,1)12 „airline“ (+ auto-ARIMA dle AIC)
   - TS3 sezónní naivní (drift 0 a drift = YoY 12M)
   - Holt-Winters s tlumeným trendem (aditivní i multiplikativní)
   - log-lineární regrese s trendem a sezónou
   - ensemble TS1+TS3
3) BACKTEST (rolling origin, jen ex ante informace – žádná znalost budoucího mixu ani trendu):
   - Hlavní řez: data do 31. 3. 2026 → predikce IV–XII/2026, vyhodnoť na IV–X/2026.
   - Kontrolní řezy: do X/2025 (h=12), do IV/2026, do VI/2026, do VIII/2026 (→ IX–X).
   - Metriky: MAPE, bias (+ = přestřelení), chyba průměrného AOV za testované období.
   - Ex post varianty (např. B2 se skutečným mixem) uváděj jen jako diagnostiku, ne pro výběr.
   Pravidla výběru: nejnižší MAPE na hlavním řezu, |bias| < 2 %, stabilita přes řezy;
   modely, které extrapolují pokles 2023–25 (trend), preferuj jen jako dolní okraj.
4) Dopočet XI–XII/2026 vybranými modely (tři varianty podle toho, kolik z propadu IX–X 2026
   přeteče: w = 0 / 0,5 / 1; spočti autokorelaci odchylek a w zdůvodni). Z toho 2026E.
5) Forecast 2027 oběma vybranými modely: měsíčně, roční hodnota vážená objednávkami,
   YoY vs. 2026E, pásmo dolní/střed/horní (pásmo z backtest chyb nebo scénářů mixu).
6) Implikace pro cíl tržeb CZ (tabulka výše): pro každý měsíc 2027 a celý rok spočti
   potřebný růst objednávek = (1 + cíl tržeb) / (1 + růst AOV) − 1, pro oba modely.
   Označ měsíce, kde je cíl (např. IV–V +10 %, VII–VIII +8 %) bez růstu objednávek
   nad historický rámec nereálný.

VÝSTUP
A) V chatu (max. 1 obrazovka):
   - Tabulka backtestu „jako v březnu 2026“ pro obě báze: model | MAPE | bias | ex ante?
   - Dva vybrané modely (1× GA/BI, 1× ERP) a proč.
   - Tabulka forecast 2027: měsíce I–XII + rok, pro oba modely, YoY vs. 2026E.
   - Tabulka implikací: cíl tržeb CZ | růst AOV | potřebný růst objednávek, po měsících + rok.
   - Doporučená plánová hodnota AOV 2027 (BI i ERP báze) a pásmo.
   - 3–5 bodů: hlavní předpoklady, rizika, co data nevysvětlí (promo, produktový mix, služby).
B) Excel „AOV_2027_CZ_final.xlsx“ – listy: Návod, Souhrn, Data_BI, Data_ERP, BI_vs_ERP,
   Backtest, Model_GA (vybraný), Model_ERP (vybraný), Forecast_2027, Cíl_2027.
   Konvence: modrá = vstupní data, černá = vzorce, zelená = odkaz na jiný list,
   žlutá = měnitelné parametry (α, γ, w, váhy, k, cíle růstu) a klíčové výsledky. Výstupy
   Pythonu, které nejdou vzorcem (SARIMA), vlož jako modré hodnoty. Po uzavření měsíce stačí
   přepsat vstupy a vše se přepočte.

Nepiš mezikroky ani průběžné komentáře – dodej jen finální výsledek podle bodů A a B.
```

---

## Referenční výsledky z původní konverzace (pro kontrolu nového běhu)

| Ukazatel | Hodnota |
|---|---|
| Skutečnost AOV IX / X 2026 (BI) | 1 038 / 1 018 Kč |
| Skutečnost AOV IX / X 2026 (ERP) | 1 023 / 1 007 Kč |
| Vítěz backtestu GA/BI (řez 3/2026) | B3 mix posledních 4 M – MAPE 3,9 %, bias −2,6 % |
| Vítěz backtestu ERP (řez 3/2026) | TS1 ETS(A,N,A) α=γ=0,1 – MAPE 4,0 %, bias −0,9 % |
| AOV 2026E | BI 1 073 Kč (+1,4 %), ERP ≈ 1 062 Kč |
| XI / XII 2026 | BI 1 042 / 1 176 Kč (w = 0,5); ERP ≈ 1 046 / 1 154 Kč |
| AOV 2027 BI (Modely A/B) | 1 086 Kč, pásmo 1 078–1 107 Kč |
| AOV 2027 ERP (ensemble TS1+TS3) | 1 061 Kč, pásmo 1 013–1 079 Kč |
| Koeficient k = AOV BI / AOV ERP | 2025 ≈ 1,004, 2026 ≈ 1,011 (měsíčně 0,98–1,03) |

Hlavní poznatky: modely s trendem mají záporný bias (−3 až −7 %); měsíční AOV má šum ±3–6 %,
roční hodnota je plánovatelná s přesností ±1,5–2 %; zlomy v létě a na podzim 2026 nejsou
z časové řady vysvětlitelné (vnitrokanálový pokles košíku při vyšších mediálních výdajích).
