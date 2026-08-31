#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator stron case studies dla webstudio47.pl.

Chrome strony (nagłówek, stopka, dane strukturalne) jest wspólny, żeby nie
rozjechał się przy zmianach. Treść każdej realizacji jest pisana osobno —
opisujemy wyłącznie to, co da się sprawdzić na żywej stronie klienta.
Żadnych wymyślonych wyników ani opinii.

Uruchomienie:  python tools/generuj-realizacje.py
"""

import html
import json
import pathlib
import re

KATALOG = pathlib.Path(__file__).resolve().parent.parent
BAZA = "https://webstudio47.pl"
FB = "https://www.facebook.com/profile.php?id=61578430357755"

# ——— Treść realizacji ————————————————————————————————————————————————

REALIZACJE = [
    dict(
        slug="strona-dla-salonu-groomerskiego",
        klient="hOla Perros",
        branza="Salon groomerski",
        miasto="Racibórz",
        domena="holaperros.pl",
        miniatura="holaperros-thumb.webp",
        tytul="Strona dla salonu groomerskiego — hOla Perros",
        opisMeta="Strona dla salonu pielęgnacji psów w Raciborzu: rezerwacja terminu, cennik usług, galeria metamorfoz i sklepik. Zobacz, jak powstała.",
        h1="Strona dla salonu groomerskiego",
        lead="Salon pielęgnacji i strzyżenia psów w Raciborzu. Marka premium, która musiała wyglądać premium także w internecie — i jednocześnie odbierać rezerwacje bez telefonu.",
        wyzwanie=[
            "Groomer sprzedaje coś, czego nie widać na cenniku: <strong>spokój psa podczas wizyty</strong>. Suchy wykaz usług i cen tego nie odda — trzeba było pokazać atmosferę salonu i efekt pracy.",
            "Drugi problem był praktyczny. Umawianie przez telefon w trakcie strzyżenia oznacza przerwanie pracy albo nieodebrane połączenie. Strona musiała przejąć część tego ruchu.",
        ],
        zbudowane=[
            ("Rezerwacja terminu online", "Klient wybiera usługę i termin bez dzwonienia. Zgłoszenie trafia na skrzynkę salonu, a właścicielka nie przerywa pracy z psem."),
            ("Galeria metamorfoz", "Zdjęcia przed i po są tu głównym argumentem sprzedażowym — pokazują poziom wykonania lepiej niż jakikolwiek opis."),
            ("Przejrzysty cennik według rozmiaru psa", "Najczęstsze pytanie w tej branży brzmi „ile to będzie kosztować u mojego psa”. Odpowiedź jest na stronie, nie w rozmowie telefonicznej."),
            ("Sklepik z kosmetykami", "Dodatkowy kanał sprzedaży dla produktów używanych w salonie."),
            ("Blog poradnikowy", "Treści o pielęgnacji, które ściągają ruch z wyszukiwarki na długo po publikacji."),
        ],
        design="Jasna, elegancka typografia z krojem szeryfowym w nagłówkach — celowo bliżej estetyki salonu kosmetycznego niż sklepu zoologicznego. Marka jest premium i wygląd strony miał to potwierdzać, zanim klient przeczyta pierwsze zdanie.",
        tagi=["Groomer", "Rezerwacje online", "Sklep", "Blog", "SEO lokalne"],
    ),
    dict(
        slug="strona-dla-zlotej-raczki",
        klient="Super Irek",
        branza="Usługi remontowe",
        miasto="Racibórz",
        domena="superirek.pl",
        miniatura="superirek-thumb.webp",
        tytul="Strona dla złotej rączki — Super Irek",
        opisMeta="Strona dla usług remontowych i montażowych w Raciborzu, zbudowana wokół jednego celu: telefonu od klienta. Zobacz, jak powstała.",
        h1="Strona dla złotej rączki",
        lead="Montaż mebli, drobna hydraulika, lampy i gniazdka, poprawki po fachowcach. Usługa, w której klient dzwoni od razu albo nie dzwoni wcale.",
        wyzwanie=[
            "Ta branża ma jeden problem z wiarygodnością: <strong>każdy może napisać, że „montuje meble”</strong>. Klient wpuszcza obcą osobę do mieszkania, więc decyduje na podstawie zaufania, nie ceny.",
            "Do tego ścieżka jest krótka. Ktoś ma popsuty kran teraz i albo zadzwoni w ciągu minuty, albo pójdzie do następnego wyniku w Google.",
        ],
        zbudowane=[
            ("Numer telefonu jako główny element", "Widoczny w nagłówku, w sekcji otwierającej i jako przyklejony przycisk na telefonie. Cała strona prowadzi do jednego działania."),
            ("Autorska ilustracja maskotki", "Zamiast zdjęć stockowych — rozpoznawalna postać, która nadaje marce twarz i odróżnia ją od konkurencji z tego samego miasta."),
            ("Rozbicie na konkretne usługi", "Osobne sekcje dla montażu mebli, hydrauliki, elektryki i poprawek. Każda odpowiada na inne zapytanie w wyszukiwarce."),
            ("Galeria realizacji", "Zdjęcia z prawdziwych zleceń — dowód, że firma istnieje i pracuje."),
            ("Opinie sąsiadów", "Społeczny dowód słuszności w formie, która pasuje do usługi lokalnej: rekomendacja od kogoś z okolicy."),
        ],
        design="Zieleń i biel, dużo powietrza, duże przyciski. Strona ma być czytelna dla osoby po pięćdziesiątce przeglądającej ją na telefonie — bo to jest realny klient tej usługi.",
        tagi=["Usługi lokalne", "Konwersja", "Ilustracja", "SEO lokalne"],
    ),
    dict(
        slug="strona-dla-firmy-sprzatajacej",
        klient="Czysto-Po",
        branza="Firma sprzątająca",
        miasto="Racibórz",
        domena="czysto-po.pl",
        miniatura="czysto-po-thumb.webp",
        tytul="Strona dla firmy sprzątającej — Czysto-Po",
        opisMeta="Strona dla firmy sprzątającej z Raciborza: ozonowanie, dezynfekcja, sprzątanie po zgonach i po remontach. Zobacz, jak powstała.",
        h1="Strona dla firmy sprzątającej",
        lead="Sprzątanie mieszkań, ozonowanie, dezynfekcja, sprzątanie po zgonach i po zbieractwie. Usługi, których szuka się w bardzo różnych stanach emocjonalnych.",
        wyzwanie=[
            "Ta firma świadczy usługi z dwóch zupełnie różnych światów. Sprzątanie po remoncie zamawia się na spokojnie, z wyprzedzeniem. <strong>Sprzątanie po zgonie zamawia się w najgorszym tygodniu swojego życia.</strong>",
            "Jeden ton komunikacji nie mógł obsłużyć obu sytuacji. Strona musiała być rzeczowa tam, gdzie klient porównuje oferty, i powściągliwa tam, gdzie potrzebuje po prostu pomocy.",
        ],
        zbudowane=[
            ("Rozdzielenie usług na osobne sekcje", "Każda usługa specjalistyczna ma własny opis i własny język. Klient trafia od razu do swojej sytuacji, nie do ogólnego cennika."),
            ("Wyciszony ton przy usługach trudnych", "Bez wykrzykników i sprzedażowego entuzjazmu tam, gdzie byłby nie na miejscu. Konkret, dyskrecja, telefon."),
            ("Treść pod zapytania długiego ogona", "„Sprzątanie po zbieractwie”, „ozonowanie mieszkania” — to są frazy o małym wolumenie, ale bardzo wysokiej intencji zakupowej."),
            ("Szybkie ładowanie", "Bez zbędnych bibliotek. Ktoś w sytuacji kryzysowej nie czeka na animacje."),
        ],
        design="Czysta struktura, wyraźna hierarchia, duży kontrast. Estetyka jest tu drugorzędna — pierwszorzędne jest to, żeby w piętnaście sekund dało się znaleźć właściwą usługę i numer telefonu.",
        tagi=["Usługi", "Marketing", "Konwersja", "SEO"],
    ),
    dict(
        slug="strona-dla-firmy-klimatyzacyjnej",
        klient="Alaska",
        branza="Klimatyzacja i chłodnictwo",
        miasto="Racibórz",
        domena="alaskarp.pl",
        miniatura="alaska-thumb.webp",
        tytul="Strona dla firmy klimatyzacyjnej — Alaska",
        opisMeta="Strona dla firmy klimatyzacyjnej i chłodniczej z Raciborza działającej od 1997 roku. Animowane wejście, blog, panel realizacji. Zobacz, jak powstała.",
        h1="Strona dla firmy klimatyzacyjnej",
        lead="Montaż i serwis klimatyzacji oraz chłodnictwo przemysłowe. Firma z Raciborza działająca od 1997 roku — z dorobkiem, którego wcześniej nie było widać w internecie.",
        wyzwanie=[
            "Firma z takim stażem ma coś, czego nowe podmioty nie kupią za żadne pieniądze: <strong>ćwierć wieku realizacji</strong>. Problem w tym, że w internecie wyglądała jak każda inna.",
            "Druga rzecz: klimatyzacja to dwa różne rynki naraz. Osoba montująca split w salonie i zakład potrzebujący chłodni to inni klienci z innymi pytaniami.",
        ],
        zbudowane=[
            ("Animowane wejście", "Krótka sekwencja otwierająca, która buduje wrażenie firmy technologicznej, a nie zakładu usługowego z lat dziewięćdziesiątych."),
            ("Rozdzielenie oferty", "Klimatyzacja dla domu i chłodnictwo przemysłowe jako osobne ścieżki, każda z własnym językiem i własnymi frazami."),
            ("Panel do dodawania realizacji", "Właściciel sam wrzuca zdjęcia z montaży, bez dzwonienia do wykonawcy strony. Portfolio rośnie samo."),
            ("Blog techniczny", "Odpowiedzi na pytania, które klienci i tak zadają przy wycenie — a przy okazji materiał dla wyszukiwarki."),
            ("Optymalizacja wydajności", "WebP, leniwe ładowanie obrazów i dzielenie kodu. Strona z animacjami nie musi być ciężka."),
        ],
        design="Chłodna paleta błękitów, mocne zdjęcia urządzeń, duże liczby przy stażu firmy. Wszystko podporządkowane jednemu przekazowi: to nie jest firma założona w zeszłym roku.",
        tagi=["Klimatyzacja", "Animacje", "Panel klienta", "Blog"],
    ),
    dict(
        slug="strona-dla-przychodni",
        klient="Life-Centrum",
        branza="Placówka medyczna",
        miasto="Racibórz",
        domena="life-centrum.pl",
        miniatura="life-centrum-thumb.webp",
        tytul="Strona dla przychodni — Life-Centrum",
        opisMeta="Strona dla centrum zdrowia w Raciborzu: usługi medyczne, punkt pobrań, lekarze specjaliści. Zobacz, jak powstała.",
        h1="Strona dla placówki medycznej",
        lead="Centrum zdrowia w Raciborzu: lekarze specjaliści, punkt pobrań krwi, usługi pielęgniarskie. Placówka, do której trafia się w konkretnej sprawie i chce się szybko wiedzieć, czy to właściwe miejsce.",
        wyzwanie=[
            "Pacjent nie przegląda strony przychodni dla przyjemności. Ma pytanie — <strong>czy przyjmuje tu ortopeda, o której otwierają punkt pobrań, czy trzeba być na czczo</strong> — i chce odpowiedzi w kilkanaście sekund.",
            "Strona medyczna ma też inny ciężar niż zwykła firmowa: musi budzić zaufanie, nie sprzedawać. Każdy element sprzedażowy działa tu przeciwko sobie.",
        ],
        zbudowane=[
            ("Architektura informacji wokół pytań pacjenta", "Nie wokół struktury organizacyjnej placówki. Punkt wejścia to potrzeba, nie dział."),
            ("Sekcja punktu pobrań z zasadami przygotowania", "Najczęściej zadawane pytanie w każdej placówce z laboratorium — odpowiedź jest na stronie, nie w słuchawce."),
            ("Prezentacja specjalistów", "Twarz i specjalizacja. W medycynie zaufanie buduje konkretna osoba, nie logo."),
            ("Spokojna, czytelna typografia", "Duży stopień pisma, wysoki kontrast, dużo światła. Część pacjentów to osoby starsze."),
            ("Dane strukturalne placówki medycznej", "Godziny, adres i zakres usług podane w formie, którą Google rozumie i pokazuje w wynikach."),
        ],
        design="Biel, błękit i dużo przestrzeni. Świadomie bez efektów — w tej branży „wow” jest podejrzane, a spokój wiarygodny.",
        tagi=["Medycyna", "UX", "Dostępność", "SEO"],
    ),
    dict(
        slug="strona-dla-transportu-medycznego",
        klient="Life-Ratownictwo",
        branza="Transport medyczny",
        miasto="Racibórz",
        domena="life-ratownictwo.pl",
        miniatura="life-ratownictwo-thumb.webp",
        tytul="Strona dla transportu medycznego",
        opisMeta="Strona dla firmy transportu medycznego i zabezpieczeń imprez: prywatna karetka, transport międzynarodowy, obsługa wydarzeń. Zobacz, jak powstała.",
        h1="Strona dla firmy transportu medycznego",
        lead="Prywatna karetka, transport międzynarodowy pacjentów i zabezpieczenie medyczne imprez masowych. Trzy usługi, trzech zupełnie różnych odbiorców.",
        wyzwanie=[
            "Na tę stronę trafiają ludzie w skrajnie różnych sytuacjach. <strong>Rodzina szukająca transportu dla chorego krewnego</strong> i <strong>organizator festynu, który musi mieć zabezpieczenie medyczne</strong> nie potrzebują tych samych informacji.",
            "Pierwszy dzwoni pod wpływem stresu i chce wiedzieć, czy da się dziś. Drugi porównuje oferty i potrzebuje zakresu, uprawnień i konkretów do przetargu.",
        ],
        zbudowane=[
            ("Rozdzielenie ścieżek od pierwszego ekranu", "Transport pacjenta i zabezpieczenie wydarzeń jako dwie osobne drogi. Nikt nie musi czytać nie swojej sekcji."),
            ("Konkret zamiast ogólników przy zabezpieczeniach", "Rodzaje zespołów, wyposażenie, zakres — to, czego szuka organizator wypełniający dokumentację."),
            ("Prosty, spokojny język przy transporcie", "Bez żargonu medycznego. Osoba w stresie ma zrozumieć od pierwszego czytania."),
            ("Telefon dostępny z każdego miejsca", "W tej branży kontakt telefoniczny wygrywa z formularzem i strona to odzwierciedla."),
            ("Galeria z prawdziwych zabezpieczeń", "Zdjęcia z realnych wydarzeń zamiast zdjęć stockowych karetek."),
        ],
        design="Czerwień i granat, mocne zdjęcia, wyraźna hierarchia. Powaga bez straszenia — to usługa, przy której estetyka ma schodzić na drugi plan wobec czytelności.",
        tagi=["Ratownictwo", "Architektura informacji", "SEO"],
    ),
    dict(
        slug="aplikacja-do-wystawiania-faktur",
        klient="WystawFakture.eu",
        branza="Aplikacja SaaS",
        miasto=None,
        domena="wystawfakture.eu",
        miniatura="wystawfakture-thumb.webp",
        tytul="Aplikacja do faktur — WystawFakture.eu",
        opisMeta="Darmowy generator faktur online bez rejestracji: faktury VAT, proforma i korekty, gotowość na KSeF. Zobacz, jak powstała aplikacja.",
        h1="Aplikacja do wystawiania faktur",
        lead="Generator faktur działający w przeglądarce, bez zakładania konta. Faktury VAT, proformy i korekty, zgodne z polskimi przepisami i przygotowane na KSeF.",
        wyzwanie=[
            "Rynek programów do faktur jest zatłoczony, ale prawie każdy zaczyna od tego samego: <strong>załóż konto, potwierdź e-mail, wybierz plan</strong>. Dla kogoś, kto musi wystawić jedną fakturę, to bariera nie do przejścia.",
            "Druga trudność jest merytoryczna. Faktura to dokument regulowany — układ pól, sposób liczenia VAT i wymagane oznaczenia wynikają z przepisów, nie z upodobań projektanta.",
        ],
        zbudowane=[
            ("Wystawienie faktury bez rejestracji", "Wchodzisz, wypełniasz, pobierasz PDF. Konto jest opcją dla wracających, nie warunkiem wstępu."),
            ("Trzy typy dokumentów", "Faktura VAT, proforma i korekta — każda z własnymi regułami i własnym układem pól."),
            ("Liczenie zgodne z przepisami", "Stawki, kwoty i zaokrąglenia liczone po stronie aplikacji, żeby użytkownik nie musiał tego sprawdzać kalkulatorem."),
            ("Przygotowanie pod KSeF", "Struktura danych ułożona tak, żeby wejście obowiązkowego e-fakturowania nie wymagało przepisywania aplikacji od zera."),
            ("Panel klienta dla wracających", "Zapisani kontrahenci i historia dokumentów dla tych, którzy fakturują regularnie."),
        ],
        design="Interfejs narzędziowy, nie marketingowy. Formularz zajmuje środek ekranu, wszystko inne schodzi z drogi. Przy aplikacji użytkowej najlepszy design to ten, którego się nie zauważa.",
        tagi=["SaaS", "Aplikacja webowa", "Panel klienta", "PDF"],
    ),
    dict(
        slug="aplikacja-z-kalkulatorami",
        klient="9 Dom",
        branza="Aplikacja webowa",
        miasto=None,
        domena="9dom.pl",
        miniatura="9dom-thumb.webp",
        tytul="Aplikacja z kalkulatorami — 9 Dom",
        opisMeta="Aplikacja z kalkulatorami astrologii wedyjskiej i numerologii: kosmogram, astrokartografia, cykle czasu, panel użytkownika. Zobacz, jak powstała.",
        h1="Aplikacja webowa z kalkulatorami",
        lead="Kalkulatory astrologii wedyjskiej i numerologii: kosmogram, astrokartografia, cykle czasu, mapa życia. Obliczenia astronomiczne podane językiem, który da się zrozumieć bez przygotowania.",
        wyzwanie=[
            "To nie jest strona informacyjna, tylko <strong>zestaw narzędzi liczących</strong>. Każdy kalkulator wymaga własnej logiki, a wyniki muszą się zgadzać — błąd w obliczeniach kompromituje cały serwis.",
            "Druga trudność to próg wejścia. Dziedzina ma własne słownictwo, którego użytkownik z zewnątrz nie zna. Wynik obliczeń bez wyjaśnienia jest bezużyteczny.",
        ],
        zbudowane=[
            ("Zestaw powiązanych kalkulatorów", "Kosmogram, numerologia, astrokartografia i cykle czasu jako osobne narzędzia korzystające ze wspólnej podstawy obliczeniowej."),
            ("Wyjaśnienia w miejscu użycia", "Pojęcia tłumaczone tam, gdzie się pojawiają, a nie na osobnej stronie ze słownikiem. Użytkownik uczy się przy okazji korzystania."),
            ("Panel użytkownika", "Zapisane profile i wyniki, żeby nie wpisywać daty urodzenia przy każdej wizycie."),
            ("Rozbudowana część treściowa", "Horoskop roczny i materiały wyjaśniające — to one przyprowadzają ruch z wyszukiwarki do narzędzi."),
        ],
        design="Ciemna, nocna paleta ze złotem i szeryfowym krojem w nagłówkach. Temat jest poważny i wyraźnie zaznaczony w komunikacie: „nie przepowiadamy przyszłości”.",
        tagi=["Aplikacja", "Kalkulatory", "Panel", "Treści"],
    ),
    dict(
        slug="serwis-tresciowy-z-narzedziem",
        klient="Karta Dnia",
        branza="Serwis treściowy",
        miasto=None,
        domena="karta-dnia.pl",
        miniatura="karta-dnia-thumb.webp",
        tytul="Serwis treściowy z narzędziem — Karta Dnia",
        opisMeta="Tarot online po polsku: karta dnia, rozkłady z interpretacją i znaczenia wszystkich 78 kart. Zobacz, jak powstał serwis.",
        h1="Serwis treściowy z narzędziem",
        lead="Rozkłady tarota z interpretacją i znaczenia wszystkich 78 kart, bez rejestracji. Serwis, w którym treść i narzędzie napędzają się nawzajem.",
        wyzwanie=[
            "Sam generator rozkładów nie wystarczy — <strong>nikt go nie znajdzie</strong>. Ruch w tej niszy przychodzi z zapytań o znaczenia poszczególnych kart, a nie z zapytania o narzędzie.",
            "Odwrotnie też nie zadziała: serwis z samymi opisami kart to jeden z tysiąca. Potrzebny był powód, żeby zostać dłużej niż na jedno przeczytanie.",
        ],
        zbudowane=[
            ("Deterministyczny silnik rozkładów", "Losowanie i interpretacja liczone po stronie aplikacji, spójnie i powtarzalnie — bez podpinania zewnętrznych usług."),
            ("Osobna strona dla każdej z 78 kart", "Każda odpowiada na własne zapytanie w wyszukiwarce. To jest właściwy fundament ruchu w tej niszy."),
            ("Brak rejestracji", "Rozkład w minutę, bez konta i bez podawania adresu e-mail. Bariera wejścia zredukowana do zera."),
            ("Wyraźne postawienie sprawy", "„Tarot, który nie wróży — pomaga myśleć”. Deklaracja, która ustawia oczekiwania i odróżnia serwis od konkurencji."),
        ],
        design="Głęboka zieleń butelkowa, złote akcenty, ilustracje kart jako główny element wizualny. Estetyka rytuału, nie jarmarku.",
        tagi=["Serwis treściowy", "Narzędzie", "SEO", "Bez rejestracji"],
    ),
]

# ——— Kontrola długości ————————————————————————————————————————————————
# Google ucina tytuł ok. 60 znaków, opis ok. 155. Generator MUSI to
# wymuszać, bo inaczej limit istnieje wyłącznie w czyjejś pamięci —
# a tak właśnie powstało 20 stron ze ściętymi tytułami.

LIMIT_TYTUL = 60
LIMIT_OPIS = 155


def sprawdz_dlugosc(tytul, opis, gdzie):
    if len(tytul) > LIMIT_TYTUL:
        raise ValueError(f'{gdzie}: tytul ma {len(tytul)} znakow, limit {LIMIT_TYTUL} -> {tytul}')
    if len(opis) > LIMIT_OPIS:
        raise ValueError(f'{gdzie}: opis ma {len(opis)} znakow, limit {LIMIT_OPIS}')


# ——— Szablon ————————————————————————————————————————————————————————

def naglowek_strony(r, stempel):
    url = f"{BAZA}/realizacje/{r['slug']}/"
    sprawdz_dlugosc(f'{r["tytul"]} | WebStudio47', r["opisMeta"], r["slug"])
    schema_dzielo = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": f"{r['klient']} — {r['branza'].lower()}",
        "headline": r["tytul"],
        "description": r["opisMeta"],
        "url": url,
        "image": f"{BAZA}/{r['miniatura']}",
        "genre": r["branza"],
        "inLanguage": "pl",
        "creator": {
            "@type": "ProfessionalService",
            "name": "WebStudio47",
            "@id": f"{BAZA}/#organizacja",
            "url": BAZA,
            "telephone": "+48602622840",
            "email": "kontakt@webstudio47.pl",
            "sameAs": [FB],
        },
        "about": {"@type": "Organization", "name": r["klient"], "url": f"https://{r['domena']}"},
        "keywords": ", ".join(r["tagi"]),
    }
    if r["miasto"]:
        schema_dzielo["locationCreated"] = {"@type": "Place", "name": r["miasto"]}

    schema_okruszki = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": f"{BAZA}/"},
            {"@type": "ListItem", "position": 2, "name": "Realizacje", "item": f"{BAZA}/portfolio.html"},
            {"@type": "ListItem", "position": 3, "name": r["klient"], "item": url},
        ],
    }

    return f'''<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(r["tytul"])} | WebStudio47</title>
    <meta name="description" content="{html.escape(r["opisMeta"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/png" href="/favicon.png">
    <meta name="theme-color" content="#0a0a0f">

    <link rel="stylesheet" href="/style.css?v={stempel}">
    <link rel="stylesheet" href="/page-style.css?v={stempel}">

    <!-- Fonts: preconnect + non-blocking load -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style"
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap"
        rel="stylesheet" media="print" onload="this.media='all'">
    <noscript>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap"
            rel="stylesheet">
    </noscript>

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:site_name" content="WebStudio47">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{html.escape(r["tytul"])}">
    <meta property="og:description" content="{html.escape(r["opisMeta"])}">
    <meta property="og:image" content="{BAZA}/{r["miniatura"]}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(r["tytul"])}">
    <meta name="twitter:description" content="{html.escape(r["opisMeta"])}">
    <meta name="twitter:image" content="{BAZA}/{r["miniatura"]}">

    <!-- Zgoda na cookies (Google Consent Mode v2).
         MUSI byc przed gtag.js: inaczej GA4 zapisze dane, zanim ktokolwiek
         wyrazi zgode. Obsluge modala ma consent.js. -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}

        gtag('consent', 'default', {{
            ad_storage: 'denied',
            ad_user_data: 'denied',
            ad_personalization: 'denied',
            analytics_storage: 'denied',
            functionality_storage: 'denied',
            personalization_storage: 'denied',
            security_storage: 'granted',
            wait_for_update: 500
        }});

        try {{
            var wybor = JSON.parse(localStorage.getItem('cookieConsent') || 'null');
            if (wybor) {{
                gtag('consent', 'update', {{
                    analytics_storage: wybor.analytics ? 'granted' : 'denied',
                    functionality_storage: wybor.functional ? 'granted' : 'denied',
                    personalization_storage: wybor.functional ? 'granted' : 'denied'
                }});
            }}
        }} catch (e) {{ }}
    </script>

    <!-- Google Analytics (GA4) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NV6W571RJB"></script>
    <script>
        gtag('js', new Date());
        gtag('config', 'G-NV6W571RJB', {{ anonymize_ip: true }});
    </script>

    <!-- Dane strukturalne: realizacja -->
    <script type="application/ld+json">
{json.dumps(schema_dzielo, ensure_ascii=False, indent=2)}
    </script>

    <!-- Dane strukturalne: okruszki -->
    <script type="application/ld+json">
{json.dumps(schema_okruszki, ensure_ascii=False, indent=2)}
    </script>
</head>
'''


NAWIGACJA = '''
<body>

    <!-- Header / Nav -->
    <header id="main-header">
        <div class="container nav-container">
            <a href="/" class="logo font-special">&lt;WebStudio<span>47</span>&gt;</a>
            <div class="nav-spacer"></div>
            <nav>
                <ul class="nav-links">
                    <li><a href="/tworzenie-stron-internetowych-raciborz/">Strony&nbsp;WWW</a></li>
                    <li><a href="/pozycjonowanie-stron-raciborz/">Pozycjonowanie</a></li>
                    <li><a href="/portfolio.html" class="active" aria-current="page">Realizacje</a></li>
                    <li><a href="/cennik/">Cennik</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/kontakt/">Kontakt</a></li>
                    <li><a href="tel:+48602622840" class="btn btn-primary btn-sm">602 622 840</a></li>
                </ul>
                <button class="menu-toggle" id="mobile-menu" aria-label="Menu nawigacyjne" aria-expanded="false">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </nav>
        </div>
    </header>
'''


def stopka(stempel):
    return f'''
    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div class="footer-logo font-special">&lt;WebStudio<span>47</span>&gt;</div>
                    <p class="footer-tagline">Strony internetowe dla firm, które traktują swój biznes poważnie. Nie
                        robię stron dla każdego — i właśnie dlatego te, które robię, wyglądają tak, jak wyglądają.</p>
                </div>
                <div class="footer-nav">
                    <p class="footer-heading">Oferta</p>
                    <ul>
                        <li><a href="/tworzenie-stron-internetowych-raciborz/">Strony internetowe</a></li>
                        <li><a href="/pozycjonowanie-stron-raciborz/">Pozycjonowanie</a></li>
                        <li><a href="/cennik/">Cennik</a></li>
                        <li><a href="/portfolio.html">Realizacje</a></li>
                        <li><a href="/blog/">Blog</a></li>
                        <li><a href="/kontakt/">Kontakt</a></li>
                    </ul>
                </div>
                <div class="footer-contact-info">
                    <p class="footer-heading">Kontakt</p>
                    <p><a href="tel:+48602622840">602 622 840</a></p>
                    <p><a href="mailto:kontakt@webstudio47.pl">kontakt@webstudio47.pl</a></p>
                    <p>Racibórz, Woj. Śląskie</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 WebStudio47. Projektowanie stron internetowych — Racibórz.</p>
                <p class="footer-note">Ograniczona liczba zleceń miesięcznie. Jakość ponad ilość.</p>
            </div>
        </div>
    </footer>

    <aside class="akcje-plywajace" aria-label="Szybkie akcje">
        <a href="tel:+48602622840" class="floating-phone-btn" id="floating-phone-btn" aria-label="Zadzwoń">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="phone-float-grad" x1="0%" y1="100%" x2="0%" y2="0%">
                        <stop offset="0%" stop-color="#7c3aed" />
                        <stop offset="100%" stop-color="#06b6d4" />
                    </linearGradient>
                </defs>
                <path
                    d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"
                    stroke="url(#phone-float-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                </path>
            </svg>
        </a>
        <button class="scroll-top-btn" id="scroll-top-btn" aria-label="Przewiń do góry">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="arrow-grad" x1="0%" y1="100%" x2="0%" y2="0%">
                        <stop offset="0%" stop-color="#7c3aed" />
                        <stop offset="100%" stop-color="#06b6d4" />
                    </linearGradient>
                </defs>
                <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
        </button>
    </aside>

    <script src="/script.js?v={stempel}" defer></script>
    <script src="/consent.js?v={stempel}" defer></script>
</body>

</html>
'''


def tresc(r, poprzednia, nastepna):
    wyzwanie = '\n'.join(f'                    <p>{x}</p>' for x in r["wyzwanie"])
    zbudowane = '\n'.join(
        f'''                    <div class="info-card glass reveal">
                        <h3>{html.escape(t)}</h3>
                        <p>{o}</p>
                    </div>''' for t, o in r["zbudowane"])
    tagi = '\n'.join(f'                    <li>{html.escape(t)}</li>' for t in r["tagi"])
    lokalizacja = f' · {r["miasto"]}' if r["miasto"] else ''

    nawigacja_realizacji = ''
    if poprzednia or nastepna:
        czesci = []
        if poprzednia:
            czesci.append(f'<a href="/realizacje/{poprzednia["slug"]}/">&larr; {html.escape(poprzednia["klient"])}</a>')
        czesci.append('<a href="/portfolio.html">Wszystkie realizacje</a>')
        if nastepna:
            czesci.append(f'<a href="/realizacje/{nastepna["slug"]}/">{html.escape(nastepna["klient"])} &rarr;</a>')
        nawigacja_realizacji = f'''
        <section class="section-alt">
            <div class="container">
                <nav class="realizacje-nawigacja" aria-label="Inne realizacje">
                    {' '.join(czesci)}
                </nav>
            </div>
        </section>
'''

    return f'''
    <main>

        <!-- Hero -->
        <section class="page-hero">
            <div class="container">
                <nav class="breadcrumbs" aria-label="Okruszki">
                    <a href="/">Strona główna</a>
                    <span aria-hidden="true">›</span>
                    <a href="/portfolio.html">Realizacje</a>
                    <span aria-hidden="true">›</span>
                    <span>{html.escape(r["klient"])}</span>
                </nav>
                <p class="realizacja-branza">{html.escape(r["branza"])}{lokalizacja}</p>
                <h1 class="reveal"><span class="text-white">{html.escape(r["h1"])}</span><br>
                    <span class="text-gradient">{html.escape(r["klient"])}</span></h1>
                <p class="page-hero-lead reveal delay-1">{r["lead"]}</p>
                <div class="page-hero-btns reveal delay-2">
                    <a href="https://{r["domena"]}" target="_blank" rel="noopener" class="btn btn-primary">Zobacz stronę na żywo</a>
                    <a href="/kontakt/" class="btn btn-outline">Chcę podobną</a>
                </div>
            </div>
        </section>

        <!-- Zrzut -->
        <section style="padding-top:0">
            <div class="container">
                <figure class="realizacja-zrzut reveal">
                    <img src="/{r["miniatura"]}" width="800" height="450" loading="lazy" decoding="async"
                        alt="Strona internetowa {html.escape(r["klient"])} — {html.escape(r["branza"].lower())}{html.escape(lokalizacja)}">
                    <figcaption>{html.escape(r["klient"])} — <a href="https://{r["domena"]}" target="_blank" rel="noopener">{r["domena"]}</a></figcaption>
                </figure>
            </div>
        </section>

        <!-- Wyzwanie -->
        <section class="section-alt">
            <div class="container">
                <div class="prose reveal">
                    <h2>Wyzwanie</h2>
{wyzwanie}
                </div>
            </div>
        </section>

        <!-- Co zbudowałem -->
        <section>
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Co zbudowałem</h2>
                </div>
                <div class="card-grid">
{zbudowane}
                </div>
            </div>
        </section>

        <!-- Design -->
        <section class="section-alt">
            <div class="container">
                <div class="prose reveal">
                    <h2>Kierunek wizualny</h2>
                    <p>{r["design"]}</p>
                    <h3>Zakres prac</h3>
                    <ul class="check-list">
{tagi}
                    </ul>
                </div>
            </div>
        </section>
{nawigacja_realizacji}
        <!-- CTA -->
        <section>
            <div class="container">
                <div class="cta-band glass reveal">
                    <h2 class="text-gradient">Chcesz taką stronę dla siebie?</h2>
                    <p>Piętnaście minut rozmowy i wiesz, ile to kosztuje w Twoim przypadku i ile potrwa.
                        Widełki cenowe znajdziesz w <a href="/cennik/">cenniku</a>.</p>
                    <div class="cta-band-btns">
                        <a href="tel:+48602622840" class="btn btn-primary">Zadzwoń: 602 622 840</a>
                        <a href="/kontakt/" class="btn btn-outline">Opisz swój projekt</a>
                    </div>
                </div>
            </div>
        </section>

    </main>
'''


def main():
    import time
    stempel = int(time.time())
    kat = KATALOG / 'realizacje'
    kat.mkdir(exist_ok=True)

    for i, r in enumerate(REALIZACJE):
        poprzednia = REALIZACJE[i - 1] if i > 0 else None
        nastepna = REALIZACJE[i + 1] if i < len(REALIZACJE) - 1 else None
        strona = (naglowek_strony(r, stempel) + NAWIGACJA
                  + tresc(r, poprzednia, nastepna) + stopka(stempel))
        cel = kat / r['slug']
        cel.mkdir(exist_ok=True)
        (cel / 'index.html').write_text(strona, encoding='utf-8')
        print(f"  realizacje/{r['slug']}/  ({len(strona) // 1024} KB)")

    print(f"\nWygenerowano {len(REALIZACJE)} stron, stempel ?v={stempel}")


if __name__ == '__main__':
    main()
