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

VSTUPNÍ DATA (přiložena)
1) BI exporty „AOV allocated“ – měsíčně per kanál, CZ eshop (filtr: E-shop = CZ eshop,
   DivisionSubType = eshop), leden 2025 – říjen 2026, ~24 kanálů.
   Metriky: Sales allocated, Orders allocated, AOV allocated, GM1, Ads costs, PNO.
   AOV = Sales allocated / Orders allocated. Používej jen „allocated“, ne „estimated“.
   Báze obsahuje produkty + služby (poštovné, balné).
2) „Vývoj AOV 2023-2026 CZ SK HU.xlsx“ – měsíční produktové AOV (ERP, BEZ služeb),
   I/2023–X/2026. Použij jen CZ.
3) RS Budget 27 (Google Sheet / export) – měsíční ERP tržby a objednávky 2025–2027 pro CZ eshop
   (2026 X–XII a 2027 jsou PLAN). Slouží k vážení, ke „mostu“ služeb a ke komparaci.
4) [volitelně] Předchozí model AOV_2027_model_CZ.xlsx – jen pro kontrolu, nepřebírej z něj závěry.

DŮLEŽITÉ VLASTNOSTI DAT (ošetři)
- Říjen 2026 v BI = jen 1.–30. 10. → pro AOV bez vlivu, objemy jsou neúplné.
- Listopad–prosinec 2026 nejsou skutečnost → nejdřív je dopočítej (viz krok 4).
- BI vs. ERP: BI má o ~3 % více objednávek (alokované vs. realizované) a o ~3,5 % vyšší tržby.
  Porovnávej růsty, ne koruny. Převod: služby_t = BI tržby_t − ERP tržby_t;
  σ = podíl služeb na BI tržbách; r = BI obj. / ERP obj.; c = (1−σ)·r. Produktové AOV = BI AOV × c
  (ověř, že vážený výsledek = ERP AOV; služby plánuj zvlášť v Kč/objednávku).
- Kanály agreguj do 7 skupin: Brand (paid+organic sloučeně – atribuce mezi nimi skáče),
  Organic non-brand, Direct, Paid search non-brand, Shopping/Pmax/srovnávače,
  CRM (Newsletter+SMS), Social/Affil/Referral/Other.
- Ověř podezřelé měsíce (např. únor 2026 v ERP/RSB27, červenec 2026 jako anomálně silný).

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
   - Metriky: MAPE, bias (+ = přestřelení), chyba ročního/průměrného AOV za testované období.
   - Ex post varianty (např. B2 se skutečným mixem) uváděj jen jako diagnostiku, ne pro výběr.
   Pravidla výběru: nejnižší MAPE na hlavním řezu, |bias| < 2 %, stabilita přes řezy;
   modely, které extrapolují pokles 2023–25 (trend), preferuj jen jako dolní okraj.
4) Dopočet XI–XII/2026 vybranými modely (tři varianty podle toho, kolik z propadu IX–X 2026
   přeteče: w = 0 / 0,5 / 1; spočti autokorelaci odchylek a w zdůvodni). Z toho 2026E.
5) Forecast 2027 oběma vybranými modely: měsíčně, roční hodnota vážená objednávkami
   (profil z RSB27), YoY vs. 2026E, pásmo dolní/střed/horní (pásmo z backtest chyb nebo
   scénářů mixu).
6) Komparace s RS Budget 27 (AOV 2026E a 2027, rozdíl v Kč a %) a implikace pro plán tržeb
   +[15] %: kolik růstu přinese AOV a kolik musí dodat objednávky.

VÝSTUP
A) V chatu (max. 1 obrazovka):
   - Tabulka backtestu „jako v březnu 2026“ pro obě báze: model | MAPE | bias | ex ante?
   - Dva vybrané modely (1× GA/BI, 1× ERP) a proč.
   - Tabulka forecast 2027: měsíce I–XII + rok, pro oba modely, + RSB27 pro srovnání.
   - Doporučená plánová hodnota AOV 2027 (BI i ERP báze) a pásmo.
   - 3–5 bodů: hlavní předpoklady, rizika, co data nevysvětlí (promo, produktový mix).
B) Excel „AOV_2027_CZ_final.xlsx“ – listy: Návod, Souhrn, Data_BI, Data_ERP, Most_služby,
   Backtest, Model_GA (vybraný), Model_ERP (vybraný), Forecast_2027, Komparace_RSB27.
   Konvence: modrá = vstupní data, černá = vzorce, zelená = odkaz na jiný list,
   žlutá = měnitelné parametry (α, γ, w, váhy, c) a klíčové výsledky. Výstupy Pythonu,
   které nejdou vzorcem (SARIMA), vlož jako modré hodnoty. Po uzavření měsíce stačí
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
| RS Budget 27 – AOV 2027 | 1 069 Kč |
| Služby (most BI − ERP) | 2025: 37,7 Kč/obj. (σ 3,5 %), 2026 I–IX: 45,1 Kč/obj. (σ 4,1 %), r ≈ 1,03 |

Hlavní poznatky: modely s trendem mají záporný bias (−3 až −7 %); měsíční AOV má šum ±3–6 %,
roční hodnota je plánovatelná s přesností ±1,5–2 %; zlomy v létě a na podzim 2026 nejsou
z časové řady vysvětlitelné (vnitrokanálový pokles košíku při vyšších mediálních výdajích).
