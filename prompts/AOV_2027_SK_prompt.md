# Prompt: AOV 2027 – SK e-shop (GA model, model časové řady, kombinace + forecast 2027)

> Verze pro SK e-shop, odvozená z CZ promptu (AOV_2027_CZ_prompt.md). Vložte celý blok níže
> do nového chatu a přiložte uvedené soubory. Cíle růstu a názvy souborů upravte, pokud se změní.

---

```text
ROLE
Jsi senior analytik pro forecasting e-commerce KPI. Pracuješ samostatně, výpočty děláš v Pythonu
(pandas, statsmodels) a výstup dodáš jako jeden Excel se živými vzorci + stručné shrnutí v chatu.
Odpovídej česky, čísla s mezerou jako oddělovačem tisíců.

CÍL
Forecast průměrné hodnoty objednávky (AOV) SK e-shopu na rok 2027 (měsíčně I–XII/2027 + roční
hodnota + pásmo). Výstupem jsou tři modely:
  M1 = nejlepší model podle GA dat (kanálový mix, AOV VČETNĚ služeb),
  M2 = nejlepší model časové řady BI ERP (produktové AOV BEZ služeb),
  M3 = kombinace M1 a M2 (doporučený finální model).
Každý model musí mít variantu s vahou vývoje VIII–X/2026 (parametr v, krok 5) a každý výsledek
musí být uveden v OBOU bázích: AOV včetně služeb i AOV bez služeb (produktové).
Výběr M1 a M2 musí být podložen backtestem, ne intuicí.
Modeluješ pouze SK eshop. Jiné existující forecasty/plány nepoužívej a nesrovnávej se s nimi.

MĚNA
Hodnoty v exportech jsou řádově ~900–1 100 na objednávku, tj. zřejmě přepočtené do Kč (ne EUR).
Měnu ověř (popis exportu / porovnání s EUR) a uveď ji ve všech tabulkách; při přepočtu z EUR
upozorni, že část meziročních změn může být kurzová.

VSTUPNÍ DATA (přiložena)
1) GA data – SK e-shop po kanálech a dnech, VČETNĚ služeb (1. 1. 2025 – 31. 10. 2026):
   - SK_1_6_2025_GA.xlsx    (1. 1. – 30. 6. 2025)
   - SK_7_12_2025_GA.xlsx   (1. 7. – 31. 12. 2025)
   - SK_1_102026_GA.xlsx    (1. 1. – 31. 10. 2026)
   Struktura: list Sheet1, řádek 1 = popis filtrů (E-shop = SK eshop, DivisionSubType = eshop,
   Cookie measurement type = standard, Web sessions není prázdné, Is in history = True),
   řádek 2 prázdný, hlavička na řádku 3 (načítat header=2). 1 řádek = kanál × den,
   řádky nejsou seřazené, bez duplicit.
   Sloupce: E-shops hierarchy – E-shop, E-shops hierarchy – E-shop (detail), Channel, Date,
   Sessions est, GA conversion rate, CR invoice est, Orders est, Sales est, AOV est, GM1 est,
   GP est incl services, GP est products, Ads costs, Ads clicks, PNO est,
   MP1 est incl services, MP1 est products.
   Kanály (Channel) s objednávkami: Google ads brand, Google organic, Google ads sea, Direct,
   Google ads pmax, Google brand organic, Newsletter, Affil, Other, Heureka, SMS, Referral,
   Facebook, Organic other, Google ads pla. Kanály Google ads other, Seznam brand organic
   a Seznam organic mají nulové objednávky; Seznam Sklik, Zbozi a Srovname na SK nejsou.
   Sales est = tržby VČETNĚ služeb (poštovné, balné). AOV vč. služeb = Σ Sales est / Σ Orders est
   (nikdy neprůměruj sloupec AOV est).
   Služby nemají GM1 (nemají náklady), takže GP est incl services − GP est products
   = přímo TRŽBY ZE SLUŽEB. Z GA tedy jde spočítat i AOV bez služeb, měsíčně i po kanálech:
   AOV_GA bez služeb = (Σ Sales est − Σ služby) / Σ Orders est.

2) BI ERP – SK_BI_ERP_AOV_2025-2026_bez_služeb.xlsx – měsíční prodeje SK e-shopu
   BEZ služeb (jen produkty), I/2025–X/2026 (celé měsíce, říjen do 31. 10.).
   Struktura: list Export, řádek 1 = hlavička, pak za každý rok řádek „Total“ a 12 (resp. 10)
   měsíců (název měsíce česky: leden … prosinec; rok jen u prvního řádku roku → doplnit ffill),
   na konci celkový Total a řádek s popisem filtrů.
   Filtry exportu: Is employee sales = customer sales; Products and gifts (Product card category)
   + typy gift a karta; ABC classification není „neurčeno“; DivisionL1 = Slovensko,
   DivisionL2 = E-shop SK.
   Sloupce: Calendar – Year, Calendar – Month, # Sales documents (= objednávky), # Documents,
   Ʃ Sales (tržby bez služeb), Ʃ Buy, Ø Sales (= AOV bez služeb = Ʃ Sales / # Sales
   documents – ověř), GM1, GM3, Ʃ Qty, Ʃ Qty PY.
   Objednávky = # Sales documents (ne # Documents). Jako váhy pro roční AOV používej
   # Sales documents.

3) [DOPORUČENO] „Vývoj AOV 2023-2026 CZ SK HU.xlsx“ – list/řada SK: měsíční AOV bez služeb
   I/2023–X/2026 (ověř shodu s BI ERP za 2025–2026 a měnu). Slouží k prodloužení časové řady
   o 2023–2024 (4 sezónní cykly místo necelých 2). Pokud přiložen není, upozorni, že sezónní
   modely (Holt-Winters, SARIMA) mají jen 22 měsíců dat, a omez výběr modelů na ty, které
   to snesou (sezónní naivní, ETS s pevnými indexy, regrese s dummy).

DŮLEŽITÉ VLASTNOSTI DAT (ošetři)
- DVĚ BÁZE AOV – klíčové pro celý výstup:
    • GA data = AOV VČETNĚ služeb (produkty + poštovné, balné, další služby),
    • BI ERP data = AOV BEZ služeb (jen produkty).
  Báze se liší i počtem objednávek: GA (Orders est, odhad) má o ~5–6 % více objednávek než
  ERP (# Sales documents). Porovnávej růsty a podíly, ne absolutní hodnoty.
- PŘEVOD MEZI BÁZEMI (most služeb) – rozlož rozdíl na dvě složky:
  (a) SLUŽBY: z GA přímo, služby = GP est incl services − GP est products;
      podíl služeb σ = služby / Sales est, na objednávku, po měsících i po skupinách kanálů
      (malé košíky ze Shopping/Pmax platí poštovné častěji – ověř).
  (b) DEFINICE OBJEDNÁVEK A TRŽEB: r_obj = Orders est / # Sales documents,
      r_tržby = (Sales est − služby) / Ʃ Sales, k_obj = AOV_GA bez služeb / Ø Sales
      (= r_tržby / r_obj).
  Celkový převod: AOV bez služeb (ERP) = AOV vč. služeb (GA) × (1 − σ) / k_obj.
  σ_2027 a k_obj_2027 jako žluté vstupy (default průměr LTM se sezónností; σ volitelně
  scénářově podle mixu kanálů). Ověř stabilitu obou složek a omezení metody uveď.
- STRUKTURÁLNÍ POKLES AOV NA SK: AOV bez služeb kleslo z 1 008 (2025) na 892 (2026 I–X),
  tj. −11,6 %. Současně se výrazně změnil mix: podíl Shopping/Pmax na objednávkách
  ~12 % → ~19 % (a jeho AOV ~667 → ~503), Paid search non-brand ~9 % → ~17 %, Brand ~31 % → ~20 %.
  Rozhodni a doložit: je pokles jednorázový posun úrovně (mix / PPC / cenotvorba – pak
  neextrapolovat), nebo trvalý trend? Pravidlo z CZ („trend jen jako dolní okraj“) na SK
  automaticky nepřebírej – rozhodni podle backtestu a dekompozice mix vs. vnitrokanálový efekt.
- Roční AOV počítej vážené objednávkami (GA: Orders est, ERP: # Sales documents).
- Listopad–prosinec 2026 nejsou skutečnost → nejdřív je dopočítej (viz krok 4).
- Kanály z GA agreguj do 7 skupin a mapování ukaž:
  Brand = Google ads brand + Google brand organic (+ Seznam brand organic, nulový)
    (paid a organic brand sloučeně – atribuce mezi nimi skáče);
  Organic non-brand = Google organic + Organic other (+ Seznam organic, nulový);
  Direct;
  Paid search non-brand = Google ads sea (+ Google ads other, nulový);
  Shopping/Pmax/srovnávače = Google ads pmax + Google ads pla + Heureka;
  CRM = Newsletter + SMS;
  Social/Affil/Referral/Other = Facebook + Affil + Referral + Other.
- Ověř podezřelé měsíce: leden 2026 (AOV nejnižší v řadě), XI/2025 (nízké AOV, start vyšších
  nákladů PPC), propad IX–X 2026. Duben 2026 = výpadek Google Ads (ban) – známá příčina, krok 5.

CÍL RŮSTU TRŽEB 2027 (YoY, pro výpočet implikací)
Měsíc:     1    2    3    4    5    6    7    8    9   10   11   12  CELKEM
SK eshop: 15%  15%  15%  15%  15%  15%  15%  15%  15%  15%  15%  15%  15%
CZ eshop:  5%   5%   5%  10%  10%   5%   8%   8%   5%   5%   5%   5%   6%
(CZ jen pro kontext – modeluje se pouze SK.)

POSTUP
1) Načti a sjednoť data (GA denně → měsíčně a týdně; ERP měsíčně), zkontroluj
   AOV = Sales/Orders v obou zdrojích, spočti most služeb (σ, r_obj, r_tržby, k_obj),
   sezónní indexy, YoY, LTM, klouzavý 12M průměr. Pro GA rozlož meziroční změnu AOV
   na mixový a vnitrokanálový efekt (7 skupin).
2) Kandidátní modely:
   GA báze (AOV vč. služeb, kanálová data):
   - A0 sezónní naivní (= stejný měsíc loni)
   - A1 sezónní naivní × YoY posledních známých měsíců
   - A  top-down: sezónní profil × trend z log-lineární regrese s měsíčními dummy
   - A4 sezónní profil × úroveň posledních 6–12 měsíců (posun úrovně bez trendu)
   - B1 bottom-up mix: Σ (podíl objednávek skupiny × AOV skupiny), mix LTM
   - B3 bottom-up mix s mixem posledních 4 měsíců
   - ensemble A1+B1
   ERP báze (AOV bez služeb, časová řada; s přílohou 3 od 2023):
   - TS1 Holt-Winters / ETS(A,N,A) bez trendu, α=γ=0,1 (+ varianta s optimalizovanými parametry
     – na SK kvůli posunu úrovně otestuj i vyšší α)
   - TS2 SARIMA(0,1,1)(0,1,1)12 „airline“ (+ auto-ARIMA dle AIC)
   - TS3 sezónní naivní (drift 0 a drift = YoY 12M)
   - Holt-Winters s tlumeným trendem (aditivní i multiplikativní)
   - log-lineární regrese s trendem a sezónou (+ varianta s dummy pro posun úrovně)
   - ensemble TS1+TS3
3) BACKTEST (rolling origin, jen ex ante informace – žádná znalost budoucího mixu ani trendu):
   - Hlavní řez: data do 31. 3. 2026 → predikce IV–XII/2026, vyhodnoť na IV–X/2026.
   - Kontrolní řezy: do X/2025 (h=12), do IV/2026, do VI/2026, do VIII/2026 (→ IX–X).
   - Metriky: MAPE, bias (+ = přestřelení), chyba průměrného AOV za testované období.
   - Ex post varianty (např. B2 se skutečným mixem) uváděj jen jako diagnostiku, ne pro výběr.
   Pravidla výběru: nejnižší MAPE na hlavním řezu, |bias| < 2 %, stabilita přes řezy.
   Řez X/2025 (h=12) přímo testuje, zda modely zachytí pokles 2026 – komentuj.
4) Dopočet XI–XII/2026 vybranými modely (tři varianty podle toho, kolik z propadu IX–X 2026
   přeteče: w = 0 / 0,5 / 1; spočti autokorelaci odchylek a w zdůvodni). Z toho 2026E.
5) VÁHA REŽIMU VIII–X/2026 (navýšení PPC):
   Orientačně z GA (SK): Ads costs 2025 I–X 52–239 tis./měs. (PNO 3–10 %), od XI/2025
   ~280–360 tis. (PNO 10–12 %), od VII/2026 420–467 tis. (PNO 11–13 %);
   AOV (GA vč. služeb) VII 893, VIII 926, IX 855, X 873. Na SK tedy byly dvě vlny navýšení PPC
   (XI/2025 a VII/2026) – z týdenních dat urči obě data zlomu a ověř.
   IV/2026 = výpadek Google Ads (ban účtu): Ads costs jen ~34 tis. (PNO 1,8 %), objednávky
   z placených kanálů minimální. Data jsou správná, nejde o chybu. Duben 2026 (a náběh v V/2026)
   proto: (1) označ jako mimořádný měsíc – nepoužívej ho k odhadu běžného mixu ani PNO a ve
   forecastu 2027 s ním počítej jako s měsícem s normálním PPC; (2) využij ho jako přirozený
   experiment „bez PPC“ – porovnej AOV a mix IV/2026 s VIII–X/2026 („max PPC“), s I–III/2026
   a s 2025 (nízké PPC); získáš tak rozpětí vlivu intenzity PPC na AOV (na 1 p. b. podílu
   placených kanálů); (3) v backtestech uveď, jak výpadek ovlivnil chyby modelů v dubnu.
   a) Z denních GA dat urči data zlomů (změna nákladů PPC / podílu paid search a Shopping
      na objednávkách) a porovnej období před a po: AOV celkem i bez služeb, AOV po skupinách,
      podíl objednávek po skupinách, podíl služeb σ, PNO. Rozlož změnu AOV na mixový
      a vnitrokanálový efekt.
   b) Zaveď parametr v = váha vývoje VIII–X/2026 (žlutá buňka, 0–1):
      - v = 0 → forecast 2027 jen z dlouhodobé historie (vybrané modely bez úpravy),
      - v = 1 → režim VIII–X/2026 trvá celý rok 2027 (mix kanálů a vnitrokanálová AOV
        z období po zlomu, YoY dynamika VIII–X aplikovaná na sezónní profil),
      - mezi tím lineární kombinace: AOV_2027_m = (1 − v) · AOV_base_m + v · AOV_PPC_m.
      Spočti varianty v = 0 / 0,25 / 0,5 / 0,75 / 1 pro M1, M2 i M3 (M2 jako časová řada
      dostane režim PPC přes úroveň: AOV_PPC_m = AOV_base_m × (AOV VIII–X 2026 / forecast
      VIII–X 2026 z modelu natrénovaného do VII/2026)).
      Výsledek: samostatný „PPC-weighted“ forecast 2027 pro každý model, ne jen poznámka.
   c) Doporuč v a zdůvodni (pokračuje navýšený PPC rozpočet v 2027? cíl +15 % tržeb na SK
      bude PPC pravděpodobně dál tlačit; autokorelace odchylek, backtest řezu VIII/2026 → IX–X).
      Volitelně zvaž v proměnné po měsících (nastavitelný řádek vah).
   d) Dopočet XI–XII/2026 (krok 4) a pásmo 2027 navaž na stejné v, aby byl výstup konzistentní.
6) KOMBINOVANÝ MODEL M3 (GA + časová řada BI ERP):
   Spoj oba přístupy tak, aby každý přispěl tím, v čem je silný:
   - ERP časová řada (M2): úroveň a sezónní profil AOV bez služeb,
   - GA model (M1): kanálový mix, služby a vliv intenzity PPC → úprava úrovně podle režimu
     VIII–X (parametr v) a scénářů mixu.
   Otestuj aspoň dvě varianty kombinace a vyber podle backtestu (stejné řezy jako v kroku 3):
   (i) vážený ensemble na společné bázi: M3 = u·M1_bez služeb + (1 − u)·M2, kde
       M1_bez služeb = M1 × (1 − σ) / k_obj; váha u z inverzní MAPE backtestu (žlutá buňka);
   (ii) hybrid: M3_m = M2_m × (1 + Δmix_m), kde Δmix_m je relativní efekt změny mixu kanálů
       a PPC režimu z M1 (mixový efekt bez vnitrokanálového trendu).
   M3 počítej pro stejné varianty v jako M1 a M2.
7) Forecast 2027 všemi třemi modely (M1, M2, M3): měsíčně, roční hodnota vážená objednávkami,
   YoY vs. 2026E, pásmo dolní/střed/horní (pásmo z backtest chyb nebo scénářů mixu).
   Každou hodnotu uveď v obou bázích: AOV vč. služeb a AOV bez služeb (převod přes σ a k_obj).
8) Implikace pro cíl tržeb SK (+15 % každý měsíc): pro každý měsíc 2027 a celý rok spočti
   potřebný růst objednávek = (1 + cíl tržeb) / (1 + růst AOV) − 1, pro M1, M2 a M3
   a pro doporučené v i krajní varianty v = 0 a v = 1. Použij AOV vč. služeb, pokud je cíl
   tržeb včetně služeb; jinak AOV bez služeb – bázi cíle uveď.
   Porovnej potřebný růst objednávek s historií (2026 vs. 2025: objednávky ERP +38 % za I–X,
   ve VIII–X +39 až +71 % YoY) a označ, které měsíce jsou bez dalšího růstu PPC nereálné.

VÝSTUP
A) V chatu (max. 1 obrazovka):
   - Tabulka backtestu „jako v březnu 2026“ pro obě báze: model | MAPE | bias | ex ante?
   - Vybrané modely M1 (GA), M2 (časová řada BI ERP), M3 (kombinace) a proč; u M3 backtest.
   - Pokles AOV 2026: rozklad na mix / vnitrokanálový efekt / služby; posun úrovně vs. trend.
   - Data zlomů PPC a srovnání před/po (AOV, mix, σ, PNO) – 1 krátká tabulka.
   - Most služeb: σ, služby na objednávku, r_obj, k_obj, převodní vztah – 1 krátká tabulka.
   - Tabulka forecast 2027: měsíce I–XII + rok, pro M1, M2, M3, YoY vs. 2026E, pro doporučené v,
     ve dvou blocích: AOV VČETNĚ služeb | AOV BEZ služeb.
   - Matice ročního AOV 2027: modely M1/M2/M3 × v = 0 / 0,25 / 0,5 / 0,75 / 1, obě báze.
   - Tabulka implikací: cíl tržeb SK | růst AOV | potřebný růst objednávek, po měsících + rok.
   - Doporučená plánová hodnota AOV 2027 = M3 při doporučeném v: jedno číslo vč. služeb
     a jedno bez služeb, s pásmem.
   - 3–5 bodů: hlavní předpoklady, rizika, co data nevysvětlí (promo, produktový mix, služby, kurz).
B) Excel „AOV_2027_SK_final.xlsx“ – listy: Návod, Souhrn, Data_GA_denní, Data_GA_měsíc,
   Data_ERP, Most_služby, Pokles_2026, Zlom_PPC, Backtest, M1_GA, M2_ERP_TS, M3_Kombinace,
   Váha_VIII-X, Forecast_2027 (obě báze vedle sebe), Cíl_2027.
   Konvence: modrá = vstupní data, černá = vzorce, zelená = odkaz na jiný list,
   žlutá = měnitelné parametry (α, γ, w, v, u, váhy, σ_2027, k_obj_2027, cíle růstu)
   a klíčové výsledky. Výstupy Pythonu, které nejdou vzorcem (SARIMA), vlož jako modré
   hodnoty. Po uzavření měsíce stačí přepsat vstupy a vše se přepočte.

Nepiš mezikroky ani průběžné komentáře – dodej jen finální výsledek podle bodů A a B.
```

---

## Referenční hodnoty pro kontrolu nového běhu (spočteno z dodaných SK dat)

| Ukazatel | Hodnota |
|---|---|
| AOV bez služeb (BI ERP, Ø Sales) – rok | 2025: 1 008; 2026 I–X: 892 (−11,6 %) |
| AOV bez služeb IX / X 2026 (BI ERP) | 857 / 867 |
| AOV vč. služeb – rok (GA) | 2025: 990; 2026 I–X: 881 |
| AOV vč. služeb IX / X 2026 (GA) | 855 / 873 |
| Objednávky ERP (# Sales documents) | 2025: 31 421 (I–X 23 509); 2026 I–X: 32 402 (+38 % YoY) |
| Služby z GA (GP incl services − GP products) | 2025: 1,9 % tržeb, 18,7/obj.; 2026 I–X: 2,6 %, 23,0/obj. |
| r_obj = Orders est (GA) / # Sales documents (ERP) | 2025: 1,050; 2026: 1,057 (leden ~1,08–1,09) |
| r_tržby = tržby GA bez služeb / Ʃ Sales ERP | 2025: 1,012; 2026: 1,018 |
| k_obj = AOV GA bez služeb / AOV ERP | ≈ 0,96–0,97 (měsíčně 0,93–0,98; leden nejnižší) |
| Mix objednávek GA 2025 → 2026 | Brand 31 → 20 %, Shopping 12 → 19 %, Paid search 9 → 17 %, Organic 13 → 18 % |
| AOV Shopping/Pmax (GA) | 2025: ~667; 2026: ~503 |
| Ads costs GA | IV/2026 ~34 tis. (ban), VII–X/2026 420–467 tis./měs. |

Měna všech hodnot dle exportu (řádově Kč) – ověřit.
