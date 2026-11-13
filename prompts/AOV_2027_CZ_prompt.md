# Prompt: AOV 2027 – CZ e-shop (GA model, model časové řady, kombinace + forecast 2027)

> Konsolidovaná verze předchozí vícekrokové konverzace. Vložte celý blok níže do nového chatu
> a přiložte uvedené soubory. Cíle růstu a názvy souborů upravte, pokud se změní.

---

```text
ROLE
Jsi senior analytik pro forecasting e-commerce KPI. Pracuješ samostatně, výpočty děláš v Pythonu
(pandas, statsmodels) a výstup dodáš jako jeden Excel se živými vzorci + stručné shrnutí v chatu.
Odpovídej česky, čísla v Kč s mezerou jako oddělovačem tisíců.

CÍL
Forecast průměrné hodnoty objednávky (AOV) CZ e-shopu na rok 2027 (měsíčně I–XII/2027 + roční
hodnota + pásmo). Výstupem jsou tři modely:
  M1 = nejlepší model podle GA/BI dat (kanálový mix, AOV VČETNĚ služeb),
  M2 = nejlepší model časové řady sales/ERP (produktové AOV BEZ služeb),
  M3 = kombinace M1 a M2 (doporučený finální model).
Každý model musí mít variantu s vahou vývoje VIII–X/2026 (parametr v, krok 5) a každý výsledek
musí být uveden v OBOU bázích: AOV včetně služeb i AOV bez služeb (produktové).
Výběr M1 a M2 musí být podložen backtestem, ne intuicí.
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
   Báze obsahuje produkty + služby (poštovné, balné) → AOV VČETNĚ služeb.
2) „Vývoj AOV 2023-2026 CZ SK HU.xlsx“ – měsíční produktové AOV (sales/ERP data) → AOV BEZ služeb
   (jen tržby za produkty, bez poštovného, balného a dalších služeb),
   I/2023–X/2026. Použij jen list/řadu CZ.
3) GA data CZ e-shop po kanálech a dnech (denní granularita, 1. 1. 2025 – 31. 10. 2026):
   - CZ_1_6_2025_GA.xlsx   (1. 1. – 30. 6. 2025)
   - CZ_7-12_2025_GA.xlsx  (1. 7. – 31. 12. 2025)
   - CZ_1_10_2026_GA.xlsx  (1. 1. – 31. 10. 2026)
   Struktura: list Sheet1, řádek 1 = popis filtrů (E-shop = CZ eshop, DivisionSubType = eshop,
   Cookie measurement type = standard, Web sessions není prázdné), řádek 2 prázdný,
   hlavička na řádku 3 (načítat header=2). 1 řádek = kanál × den, řádky nejsou seřazené.
   Sloupce: E-shops hierarchy – E-shop, E-shops hierarchy – E-shop (detail), Channel, Date,
   Sessions est, GA conversion rate, CR invoice est, Orders est, Sales est, AOV est, GM1 est,
   GP est incl services, GP est products, Ads costs, Ads clicks, PNO est,
   MP1 est incl services, MP1 est products.
   24 kanálů (Channel): Google organic, Direct, Google ads brand, Google brand organic,
   Google ads sea, Google ads pmax, Newsletter, Google ads pla, SMS, Seznam sklik brand, Other,
   Heureka, Referral, Organic other, Seznam organic, Seznam brand organic, Facebook,
   Seznam sklik sea, Zbozi, Affil, Srovname, Google ads other, Seznam sklik other,
   Seznam sklik display.
   GA data (Sales est) jsou VČETNĚ služeb (poštovné, balné) – stejně jako BI exporty;
   Služby nemají GM1 (nemají náklady), takže rozdíl GP est incl services − GP est products
   = přímo TRŽBY ZE SLUŽEB. Z GA tedy jde spočítat AOV bez služeb přímo, měsíčně i po kanálech:
   AOV_GA bez služeb = (Σ Sales est − Σ služby) / Σ Orders est.
   Pozor: GA používá metriky „est“ (odhad), BI exporty „allocated“ → AOV se v jednotlivých
   měsících liší (např. I/2025 GA 905 vs. BI 938 Kč). Porovnávej růsty a podíly, ne koruny;
   rozdíl GA vs. BI po měsících vyčísli. AOV vždy počítej jako Σ Sales est / Σ Orders est
   (nikdy neprůměruj sloupec AOV est).
   Použití: (a) přesné určení data zlomu navýšení PPC (Ads costs po dnech/týdnech),
   (b) denní/týdenní AOV a mix kanálů před a po zlomu, (c) tržby ze služeb:
   služby = GP est incl services − GP est products (Kč, Kč/objednávku, podíl na tržbách;
   měsíčně a po skupinách kanálů) → AOV bez služeb po kanálech a převod mezi bázemi.
   Kanály namapuj na stejných 7 skupin jako BI (Brand = Google ads brand + Google brand
   organic + Seznam sklik brand + Seznam brand organic; Paid search non-brand = Google ads sea
   + Seznam sklik sea + Google ads other + Seznam sklik other/display; Shopping/Pmax/srovnávače
   = Google ads pmax + Google ads pla + Heureka + Zbozi + Srovname; CRM = Newsletter + SMS;
   Organic non-brand = Google organic + Seznam organic + Organic other; Direct;
   Social/Affil/Referral/Other = Facebook + Affil + Referral + Other) a mapování ukaž.

DŮLEŽITÉ VLASTNOSTI DAT (ošetři)
- Říjen 2026 v BI = jen 1.–30. 10. → pro AOV bez vlivu, objemy jsou neúplné.
- Listopad–prosinec 2026 nejsou skutečnost → nejdřív je dopočítej (viz krok 4).
- DVĚ BÁZE AOV – klíčové pro celý výstup:
    • GA a BI data = AOV VČETNĚ služeb (produkty + poštovné, balné, další služby),
    • sales/ERP data = AOV BEZ služeb (jen produkty).
  Báze se liší i definicí objednávek (BI alokované, ERP realizované). Porovnávej růsty, ne koruny.
- PŘEVOD MEZI BÁZEMI (most služeb) – rozlož rozdíl na dvě složky:
  (a) SLUŽBY: z GA přímo, služby = GP est incl services − GP est products (služby nemají GM1);
      podíl služeb σ = služby / Sales est, Kč/objednávku, po měsících i po skupinách kanálů
      (malé košíky ze Shopping/Pmax platí poštovné častěji – ověř).
  (b) DEFINICE OBJEDNÁVEK: k_obj = AOV_GA bez služeb / AOV_ERP (GA est počítá jinak
      objednávky než ERP); totéž pro BI (k = AOV_BI / AOV_ERP).
  Celkový převod: AOV bez služeb (ERP) = AOV vč. služeb (GA) × (1 − σ) / k_obj.
  σ_2027 a k_obj_2027 jako žluté vstupy (default průměr LTM se sezónností; σ volitelně
  scénářově podle mixu kanálů). Ověř stabilitu obou složek a omezení metody uveď.
- Roční AOV počítej vážené objednávkami; jako váhy použij Orders allocated z BI
  (pro 2023–2024 ERP řady prostý průměr).
- Kanály agreguj do 7 skupin: Brand (paid+organic sloučeně – atribuce mezi nimi skáče),
  Organic non-brand, Direct, Paid search non-brand, Shopping/Pmax/srovnávače,
  CRM (Newsletter+SMS), Social/Affil/Referral/Other.
- Ověř podezřelé měsíce (např. leden–únor 2026 slabé, červenec 2026 anomálně silný,
  propad IX–X 2026). Duben 2026 = výpadek Google Ads (ban) – známá příčina, viz krok 5.

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
5) VÁHA REŽIMU VIII–X/2026 (navýšení PPC):
   Od léta 2026 se výrazně navýšily investice do PPC. Orientačně z GA: Ads costs
   VI/2026 1,25 mil. → VII 2,11 → VIII 2,64 → IX 2,61 → X 2,27 mil. Kč; PNO 7,6 % → 9,6 →
   11,2 → 13,6 → 11,6 %; AOV (GA est) VII 1 069, VIII 1 079, IX 1 006, X 987 Kč.
   Týdenní data naznačují náběh od poloviny VII a plný režim od týdne končícího 9. 8. 2026
   (PNO > 12 %), v druhé polovině X mírné snížení – ověř.
   IV/2026 = výpadek Google Ads (ban účtu): Ads costs jen 0,28 mil. Kč (PNO 2,2 %), objednávky
   z placených kanálů minimální. Data jsou správná, nejde o chybu. Duben 2026 (a náběh v V/2026)
   proto: (1) označ jako mimořádný měsíc – nepoužívej ho k odhadu běžného mixu ani PNO a ve
   forecastu 2027 s ním počítej jako s měsícem s normálním PPC; (2) využij ho jako přirozený
   experiment „bez PPC“ – porovnej AOV a mix IV/2026 s VIII–X/2026 („max PPC“) a s H1 2026
   (běžné PPC); získáš tak rozpětí vlivu intenzity PPC na AOV (Kč AOV na 1 p. b. podílu
   placených kanálů); (3) v backtestech uveď, jak výpadek ovlivnil chyby modelů v dubnu.
   a) Z denních GA dat urči datum zlomu (změna nákladů PPC / podílu paid search a Shopping
      na objednávkách) a porovnej období před a po zlomu: AOV celkem, AOV po skupinách,
      podíl objednávek po skupinách, PNO. Rozlož změnu AOV na mixový a vnitrokanálový efekt.
   b) Zaveď parametr v = váha vývoje VIII–X/2026 (žlutá buňka, 0–1):
      - v = 0 → forecast 2027 jen z dlouhodobé historie (vybrané modely bez úpravy),
      - v = 1 → režim VIII–X/2026 trvá celý rok 2027 (mix kanálů a vnitrokanálová AOV
        z období po zlomu, YoY dynamika VIII–X aplikovaná na sezónní profil),
      - mezi tím lineární kombinace: AOV_2027_m = (1 − v) · AOV_base_m + v · AOV_PPC_m.
      Spočti varianty v = 0 / 0,25 / 0,5 / 0,75 / 1 pro M1, M2 i M3 (M2 jako časová řada
      dostane režim PPC přes úroveň: AOV_PPC_m = AOV_base_m × (AOV VIII–X 2026 / forecast
      VIII–X 2026 z modelu natrénovaného do VII/2026)).
      Výsledek: samostatný „PPC-weighted“ forecast 2027 pro každý model, ne jen poznámka.
   c) Doporuč v a zdůvodni (pokračuje navýšený PPC rozpočet v 2027? autokorelace odchylek,
      backtest řezu VIII/2026 → IX–X). Volitelně zvaž v proměnné po měsících
      (např. PPC režim jen v určitých měsících 2027 – nastavitelný řádek vah).
   d) Dopočet XI–XII/2026 (krok 4) a pásmo 2027 navaž na stejné v, aby byl výstup konzistentní.
6) KOMBINOVANÝ MODEL M3 (GA/BI + časová řada ERP):
   Spoj oba přístupy tak, aby každý přispěl tím, v čem je silný:
   - ERP časová řada (M2): dlouhá historie 2023–2026 → úroveň a sezónní profil AOV bez služeb,
   - GA/BI model (M1): kanálový mix a vliv intenzity PPC → úprava úrovně podle režimu VIII–X
     (parametr v) a scénářů mixu.
   Otestuj aspoň dvě varianty kombinace a vyber podle backtestu (stejné řezy jako v kroku 3):
   (i) vážený ensemble převedený na společnou bázi: M3 = u·M1/k + (1 − u)·M2, váha u
       z inverzní MAPE backtestu (žlutá buňka);
   (ii) hybrid: M3_m = M2_m × (1 + Δmix_m), kde Δmix_m je relativní efekt změny mixu kanálů
       a PPC režimu z M1 (mixový efekt bez vnitrokanálového trendu).
   M3 počítej pro stejné varianty v jako M1 a M2.
7) Forecast 2027 všemi třemi modely (M1, M2, M3): měsíčně, roční hodnota vážená objednávkami,
   YoY vs. 2026E, pásmo dolní/střed/horní (pásmo z backtest chyb nebo scénářů mixu).
   Každou hodnotu uveď v obou bázích: AOV vč. služeb a AOV bez služeb (převod přes k).
8) Implikace pro cíl tržeb CZ (tabulka výše): pro každý měsíc 2027 a celý rok spočti
   potřebný růst objednávek = (1 + cíl tržeb) / (1 + růst AOV) − 1, pro M1, M2 a M3
   a pro doporučené v i krajní varianty v = 0 a v = 1. Použij AOV vč. služeb, pokud je cíl
   tržeb včetně služeb; jinak AOV bez služeb – bázi cíle uveď.
   Označ měsíce, kde je cíl (např. IV–V +10 %, VII–VIII +8 %) bez růstu objednávek
   nad historický rámec nereálný.

VÝSTUP
A) V chatu (max. 1 obrazovka):
   - Tabulka backtestu „jako v březnu 2026“ pro obě báze: model | MAPE | bias | ex ante?
   - Vybrané modely M1 (GA/BI), M2 (časová řada ERP), M3 (kombinace) a proč; u M3 backtest.
   - Datum zlomu PPC a srovnání před/po (AOV, mix, PNO) – 1 krátká tabulka.
   - Most služeb: σ, služby Kč/objednávku, k_obj, převodní vztah – 1 krátká tabulka.
   - Tabulka forecast 2027: měsíce I–XII + rok, pro M1, M2, M3, YoY vs. 2026E, pro doporučené v,
     ve dvou blocích: AOV VČETNĚ služeb | AOV BEZ služeb.
   - Matice ročního AOV 2027: modely M1/M2/M3 × v = 0 / 0,25 / 0,5 / 0,75 / 1, obě báze.
   - Tabulka implikací: cíl tržeb CZ | růst AOV | potřebný růst objednávek, po měsících + rok.
   - Doporučená plánová hodnota AOV 2027 = M3 při doporučeném v: jedno číslo vč. služeb
     a jedno bez služeb, s pásmem.
   - 3–5 bodů: hlavní předpoklady, rizika, co data nevysvětlí (promo, produktový mix, služby).
B) Excel „AOV_2027_CZ_final.xlsx“ – listy: Návod, Souhrn, Data_BI, Data_ERP, BI_vs_ERP,
   Data_GA_denní, Zlom_PPC, Most_služby, Backtest, M1_GA_BI, M2_ERP_TS, M3_Kombinace,
   Váha_VIII-X, Forecast_2027 (obě báze vedle sebe), Cíl_2027.
   Konvence: modrá = vstupní data, černá = vzorce, zelená = odkaz na jiný list,
   žlutá = měnitelné parametry (α, γ, w, v, u, váhy, σ_2027, k_obj_2027, cíle růstu) a klíčové výsledky. Výstupy
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
| Služby z GA (GP incl services − GP products) | 2025: 2,2 % tržeb, 22,9 Kč/obj.; 2026 I–X: 2,7 %, 27,1 Kč/obj. |
| k_obj = AOV GA bez služeb / AOV ERP | ≈ 0,955, stabilní (měsíčně 0,92–0,97; leden nejnižší) |

Hlavní poznatky: modely s trendem mají záporný bias (−3 až −7 %); měsíční AOV má šum ±3–6 %,
roční hodnota je plánovatelná s přesností ±1,5–2 %; zlomy v létě a na podzim 2026 nejsou
z časové řady vysvětlitelné (vnitrokanálový pokles košíku při vyšších mediálních výdajích).
