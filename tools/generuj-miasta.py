#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator stron lokalnych dla webstudio47.pl.

UWAGA na pułapkę: cztery strony różniące się wyłącznie nazwą miasta to
klasyczna „strona-wycieraczka” (doorway page), którą Google traktuje jako
spam. Dlatego każde miasto ma własny, realnie odmienny tekst: inny rynek,
inna konkurencja, inne konsekwencje dla ceny i terminu.

Wspólny jest tylko chrome (nagłówek, stopka, dane strukturalne).

Uruchomienie:  python tools/generuj-miasta.py
"""

import html
import json
import pathlib
import time

KATALOG = pathlib.Path(__file__).resolve().parent.parent
BAZA = "https://webstudio47.pl"

def bezp(tekst):
    """html.escape, ale nie psuje twardych spacji wpisanych w tresci.

    Bez tego „&nbsp;" wstawione przez tools/sierotki.py wychodzi z escape'a
    jako widoczne „&amp;nbsp;" — czytelnik widzi wtedy w zdaniu doslowny
    ciag znakow zamiast spacji. Zdarzylo sie to 2026-09-01 w opisach meta
    i pytaniach FAQ.
    """
    return html.escape(tekst).replace('&amp;nbsp;', '&nbsp;')

FB = "https://www.facebook.com/profile.php?id=61578430357755"

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


MIASTA = [
    dict(
        slug="strony-internetowe-wodzislaw-slaski",
        miasto="Wodzisław Śląski",
        miastoD="Wodzisławia Śląskiego",   # dopełniacz
        miastoMs="Wodzisławiu Śląskim",    # miejscownik
        wojewodztwo="śląskie",
        dojazd="niecałe pół godziny",
        opisMeta="Tworzenie stron internetowych w Wodzisławiu Śląskim. Strony pisane od zera, wycena po 15-minutowej rozmowie. Racibórz obok, spotkanie bez problemu.",
        lead="Wodzisław jest najbliższym sąsiadem Raciborza — dojazd zajmuje niecałe pół godziny. To jedyne miasto z&nbsp;tej listy, w&nbsp;którym spotkanie na kawie przy pierwszej rozmowie jest naprawdę bez znaczenia logistycznego.",
        rynek=[
            "Wodzisław i&nbsp;Racibórz to praktycznie jeden rynek pracy i&nbsp;usług. Klienci jeżdżą w&nbsp;obie strony, firmy budowlane obsługują oba miasta, a&nbsp;wiele zapytań w&nbsp;wyszukiwarce pada bez nazwy miasta w&nbsp;ogóle — po prostu „hydraulik” z&nbsp;lokalizacją ustaloną przez telefon.",
            "Dla Ciebie oznacza to konkretną rzecz: <strong>walka o&nbsp;widoczność toczy się tu nie tylko z&nbsp;firmami z&nbsp;Wodzisławia, ale i&nbsp;z raciborskimi</strong>. Profil Firmy w&nbsp;Google trzeba ustawić tak, żeby obsługiwał oba obszary, a&nbsp;nie tylko adres siedziby.",
        ],
        specyfika=[
            ("Jeden obszar, dwa miasta", "Ustawiam obsługiwany obszar w&nbsp;Profilu Firmy tak, żeby obejmował Wodzisław i&nbsp;Racibórz. Wiele firm traci tu połowę zasięgu, zostawiając domyślny promień wokół adresu."),
            ("Spotkanie na żywo w&nbsp;cenie", "Przy projektach ze zdjęciami i&nbsp;materiałami do zebrania osobiste spotkanie oszczędza tygodnie wymiany maili. Z&nbsp;Raciborza to rzut beretem."),
            ("Konkurencja średnia", "Mniejsza niż w&nbsp;Rybniku, większa niż w&nbsp;Głubczycach. Realny termin na pierwsze efekty pozycjonowania: od czterech do sześciu miesięcy."),
        ],
        pytania=[
            ("Czy pracujesz zdalnie, czy trzeba się spotkać?",
             "Cały projekt da się poprowadzić zdalnie — tak robię większość zleceń. Ale przy Wodzisławiu spotkanie nie jest problemem i&nbsp;przy niektórych projektach po prostu przyspiesza sprawę, zwłaszcza gdy trzeba obejrzeć zakład albo zebrać zdjęcia."),
            ("Czy strona z&nbsp;Raciborza będzie widoczna w&nbsp;Wodzisławiu?",
             "To zależy nie od tego, gdzie mieszka wykonawca, tylko gdzie działa Twoja firma. Google ustala widoczność lokalną na podstawie Profilu Firmy, adresu i&nbsp;obsługiwanego obszaru — a&nbsp;nie na podstawie tego, kto zrobił stronę."),
            ("Mam klientów i&nbsp;w&nbsp;Wodzisławiu, i&nbsp;w&nbsp;Raciborzu. Pod które miasto pozycjonować?",
             "Pod oba, ale nie tą samą treścią. Jedna strona może celować w&nbsp;dwa sąsiednie miasta, jeśli ma osobną podstronę dla każdego i&nbsp;realnie różną treść. Inaczej Google potraktuje je jak duplikat i&nbsp;sam wybierze jedną — zwykle nie tę, na której Ci zależy."),
            ("Wolę rozmawiać twarzą w&nbsp;twarz. Dojedziesz?",
             "Dojadę, to niecałe pół godziny. Zwykle wystarczy jedno spotkanie na starcie, żeby zobaczyć firmę i&nbsp;zebrać zdjęcia, a&nbsp;resztę prowadzę zdalnie. Dojazdu nie doliczam do wyceny."),
        ],
    ),
    dict(
        slug="strony-internetowe-rybnik",
        miasto="Rybnik",
        miastoD="Rybnika",
        miastoMs="Rybniku",
        wojewodztwo="śląskie",
        dojazd="około pół godziny",
        opisMeta="Tworzenie stron internetowych w Rybniku. Strony pisane od zera dla firm z Rybnika i okolic. Uczciwie o tym, ile kosztuje tu widoczność w Google.",
        lead="Rybnik jest kilkakrotnie większy od Raciborza i&nbsp;to zmienia wszystko — nie w&nbsp;wykonaniu strony, tylko w&nbsp;tym, ile trzeba włożyć, żeby ktoś ją znalazł.",
        rynek=[
            "To najbardziej konkurencyjne miasto z&nbsp;całej okolicy. W&nbsp;większości branż usługowych w&nbsp;Rybniku walczysz nie z&nbsp;dwiema firmami, tylko z&nbsp;kilkunastoma — a&nbsp;część z&nbsp;nich ma już wyrobioną pozycję i&nbsp;kilkadziesiąt opinii w&nbsp;Google.",
            "<strong>Powiem to wprost, bo lepiej wiedzieć na starcie: sama ładna strona w&nbsp;Rybniku nie wystarczy.</strong> Tu potrzeba albo cierpliwości i&nbsp;konsekwentnej pracy nad widocznością, albo wąskiej specjalizacji, w&nbsp;której konkurencja jest cieńsza.",
        ],
        specyfika=[
            ("Nisza zamiast ogólnika", "W&nbsp;Rybniku nie warto celować we frazę „elektryk”. Warto w&nbsp;„instalacje fotowoltaiczne Rybnik” albo inną wąską specjalizację, w&nbsp;której da się wygrać."),
            ("Opinie ważą więcej niż gdzie indziej", "Przy kilkunastu konkurentach w&nbsp;mapce Google o&nbsp;kolejności decydują opinie. Bez planu ich zbierania sama strona niewiele zmieni."),
            ("Dłuższy horyzont", "Realny termin na efekty pozycjonowania w&nbsp;Rybniku to sześć do dziewięciu miesięcy, nie trzy. Kto obiecuje szybciej, sprzedaje nadzieję."),
        ],
        pytania=[
            ("Czy warto w&nbsp;ogóle walczyć o&nbsp;Rybnik?",
             "Warto, jeśli masz wyraźną specjalizację albo cierpliwość. Nie warto, jeśli liczysz, że sama strona załatwi sprawę w&nbsp;kwartał. Na pierwszej rozmowie mówię, w&nbsp;której z&nbsp;tych sytuacji jesteś — również wtedy, gdy odpowiedź brzmi „nie zaczynajmy”."),
            ("Robisz strony tylko dla firm z&nbsp;Raciborza?",
             "Nie. Cały proces prowadzę zdalnie, więc lokalizacja nie jest przeszkodą. Znajomość rynku ma znaczenie przy pozycjonowaniu lokalnym, ale Rybnik to obszar, który znam — jest po sąsiedzku."),
            ("Konkurencja w&nbsp;Rybniku ma już dobre strony. Co mi da nowa?",
             "Sama nowa strona nie przeskoczy kogoś, kto siedzi wysoko od lat. Daje natomiast dwie rzeczy: przestajesz odpadać w&nbsp;momencie, w&nbsp;którym klient porównuje Cię z&nbsp;konkurencją, i&nbsp;masz fundament, na którym pozycjonowanie ma się na czym oprzeć. Bez tego drugiego pierwsze i&nbsp;tak nie ruszy."),
            ("Czy w&nbsp;Rybniku wystarczy sama strona, czy trzeba dokładać reklamy?",
             "Przy tak nasyconym rynku reklama bywa jedynym sposobem, żeby pojawić się szybko — ale to koszt stały, który znika razem z&nbsp;budżetem. Pozycjonowanie działa odwrotnie: wolniej i&nbsp;trwalej. Zwykle sensowne jest jedno i&nbsp;drugie, tylko w&nbsp;innych momentach."),
        ],
    ),
    dict(
        slug="strony-internetowe-kedzierzyn-kozle",
        miasto="Kędzierzyn-Koźle",
        miastoD="Kędzierzyna-Koźla",
        miastoMs="Kędzierzynie-Koźlu",
        wojewodztwo="opolskie",
        dojazd="około pół godziny",
        opisMeta="Tworzenie stron internetowych w Kędzierzynie-Koźlu. Strony od zera dla firm usługowych i podwykonawców przemysłowych. Wycena po rozmowie.",
        lead="Kędzierzyn-Koźle leży już w&nbsp;województwie opolskim, ale z&nbsp;Raciborza to wciąż pół godziny drogi. Miasto o&nbsp;wyraźnie przemysłowym charakterze — i&nbsp;to widać w&nbsp;tym, jakich stron się tu potrzebuje.",
        rynek=[
            "Struktura firm jest tu inna niż w&nbsp;Raciborzu. Obok typowych usług dla mieszkańców jest dużo <strong>podwykonawców obsługujących zakłady przemysłowe</strong> — a&nbsp;to zupełnie inny rodzaj klienta i&nbsp;inny rodzaj strony.",
            "Firma sprzedająca usługi do zakładu nie potrzebuje efektownej animacji. Potrzebuje konkretu: zakresu prac, uprawnień, certyfikatów i&nbsp;referencji w&nbsp;formie, którą da się wkleić do dokumentacji przetargowej.",
        ],
        specyfika=[
            ("Strona jako dokument, nie folder reklamowy", "Przy sprzedaży B2B do przemysłu liczy się sprawdzalność: pełna nazwa, NIP, zakres uprawnień, realizacje z&nbsp;nazwy. To buduje wiarygodność szybciej niż jakikolwiek slogan."),
            ("Inne województwo, ten sam zasięg", "Granica administracyjna nie ma znaczenia dla Google. Znaczenie ma poprawnie ustawiony obszar działania w Profilu Firmy."),
            ("Mniejsza konkurencja niż w&nbsp;Rybniku", "W&nbsp;wielu niszach przemysłowych wciąż da się tu zbudować widoczność szybciej i&nbsp;taniej niż w&nbsp;większych miastach regionu."),
        ],
        pytania=[
            ("Czy robisz strony dla firm spoza województwa śląskiego?",
             "Tak. Cały projekt prowadzę zdalnie, a&nbsp;przy pozycjonowaniu lokalnym liczy się adres i&nbsp;obszar działania Twojej firmy, nie mój. Kędzierzyn to zresztą pół godziny drogi."),
            ("Czym różni się strona B2B od zwykłej firmowej?",
             "Innym punktem ciężkości. Zamiast budowania emocji — sprawdzalne fakty: zakres, uprawnienia, referencje, dane rejestrowe. Kupujący w&nbsp;firmie musi móc uzasadnić wybór przełożonemu, a&nbsp;nie tylko sam się przekonać."),
            ("Nie sprzedaję konsumentom, tylko firmom. Co powinno być na takiej stronie?",
             "Co innego niż na stronie dla klienta z&nbsp;ulicy. Liczą się konkretne dane: zakres i&nbsp;skala usług, zasoby albo park maszynowy, uprawnienia i&nbsp;certyfikaty, referencje wymienione z&nbsp;nazwy oraz szybka ścieżka do zapytania ofertowego. Ładne zdjęcia są tu dodatkiem, nie argumentem."),
            ("Klientów mam z&nbsp;polecenia. Czy strona jest mi w&nbsp;ogóle potrzebna?",
             "Polecenie i&nbsp;tak kończy się sprawdzeniem w&nbsp;Google — ktoś wpisuje nazwę firmy, zanim zadzwoni. Strona nie musi wtedy zdobywać klienta, tylko potwierdzić, że firma istnieje naprawdę i&nbsp;wygląda poważnie. To inna rola i&nbsp;zwykle tańsza strona."),
        ],
    ),
    dict(
        slug="strony-internetowe-glubczyce",
        miasto="Głubczyce",
        miastoD="Głubczyc",
        miastoMs="Głubczycach",
        wojewodztwo="opolskie",
        dojazd="około czterdziestu minut",
        opisMeta="Tworzenie stron internetowych w Głubczycach. Mała konkurencja w Google to realna szansa na pierwsze miejsce. Wycena po rozmowie.",
        lead="Głubczyce to najmniejsze miasto z&nbsp;tej listy — i&nbsp;właśnie dlatego najciekawsze pod względem widoczności w&nbsp;Google. Tam, gdzie konkurencja jest cienka, dobrze zrobiona strona wychodzi na pierwsze miejsce zaskakująco szybko.",
        rynek=[
            "W&nbsp;większości branż usługowych w&nbsp;Głubczycach konkurujesz z&nbsp;kilkoma firmami, a&nbsp;nierzadko <strong>żadna z&nbsp;nich nie ma porządnej strony</strong>. Zdarza się, że pierwsze miejsce w&nbsp;Google zajmuje wpis w&nbsp;katalogu sprzed lat albo profil na portalu ogłoszeniowym.",
            "To najtańszy rynek do zdobycia z&nbsp;całej okolicy. Ta sama praca, która w&nbsp;Rybniku daje efekt po dziewięciu miesiącach, tutaj bywa widoczna po dwóch — po prostu dlatego, że nie ma z&nbsp;kim przegrać.",
        ],
        specyfika=[
            ("Niska konkurencja to realna przewaga", "Sam poprawnie skonfigurowany Profil Firmy plus strona z&nbsp;sensowną treścią potrafią w&nbsp;Głubczycach wystarczyć do wejścia na pierwszą stronę wyników."),
            ("Zasięg szerszy niż miasto", "Przy tej wielkości warto celować w cały powiat, nie tylko w samo miasto — to wielokrotnie większy zbiór potencjalnych klientów."),
            ("Prostszy projekt bywa lepszy", "Skoro widoczność jest tania, budżet lepiej przesunąć z&nbsp;efektów wizualnych na treść i&nbsp;Profil Firmy. Mówię o&nbsp;tym wprost przy wycenie."),
        ],
        pytania=[
            ("Czy w&nbsp;tak małym mieście strona ma sens?",
             "Ma, i&nbsp;to większy niż w&nbsp;dużym — właśnie dlatego, że mało kto ją tu ma. Przy niskiej konkurencji koszt wejścia na pierwsze miejsce jest ułamkiem tego, co trzeba wydać w&nbsp;Rybniku."),
            ("Ile trwa wyjście na pierwszą stronę w&nbsp;Google?",
             "W&nbsp;Głubczycach zwykle szybciej niż gdzie indziej w&nbsp;regionie — bywa, że dwa, trzy miesiące. Nie obiecuję konkretnej pozycji, bo decyduje o&nbsp;niej Google, ale realnie startujesz tu z&nbsp;lepszej sytuacji niż w&nbsp;większym mieście."),
            ("Głubczyce są małe. Czy warto celować też w&nbsp;okoliczne miejscowości?",
             "Zwykle tak — przy mniejszym mieście sam rynek bywa za wąski, żeby utrzymać firmę z&nbsp;samego Google. Wtedy ma sens osobna podstrona dla każdego obsługiwanego kierunku, ale tylko wtedy, gdy naprawdę tam jeździsz. Strona obiecująca dojazd, którego nie ma, kosztuje więcej, niż daje."),
            ("Ile kosztuje najtańsza sensowna strona?",
             "Najtańszy sensowny wariant to landing page: jedna strona z&nbsp;jednym celem, od&nbsp;1&nbsp;500&nbsp;zł netto. Pełna strona firmowa zaczyna się od&nbsp;2&nbsp;000&nbsp;zł. Widełki są jawne, bez formularza — stoją w&nbsp;cenniku."),
        ],
    ),
]

# Realizacje pokazywane jako dowód — te same dla każdego miasta, bo są
# prawdziwe. Nie udajemy, że mamy klienta w każdym z tych miast.
DOWODY = [
    ("hOla Perros", "salon groomerski", "strona-dla-salonu-groomerskiego", "holaperros-thumb.webp"),
    ("Super Irek", "usługi remontowe", "strona-dla-zlotej-raczki", "superirek-thumb.webp"),
    ("Czysto-Po", "firma sprzątająca", "strona-dla-firmy-sprzatajacej", "czysto-po-thumb.webp"),
]


def strona(m, stempel):
    url = f"{BAZA}/{m['slug']}/"
    TYTUL = f'Strony internetowe {m["miasto"]} | WebStudio47'
    sprawdz_dlugosc(TYTUL, m["opisMeta"], m["slug"])

    schema_uslugi = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Tworzenie stron internetowych — {m['miasto']}",
        "serviceType": "Projektowanie i&nbsp;tworzenie stron internetowych",
        "url": url,
        "description": m["opisMeta"],
        "provider": {
            "@type": "ProfessionalService",
            "name": "WebStudio47",
            "@id": f"{BAZA}/#organizacja",
            "url": BAZA,
            "telephone": "+48602622840",
            "email": "kontakt@webstudio47.pl",
            "priceRange": "600-15000 PLN",
            "sameAs": [FB],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Skłodowskiej 2",
                "addressLocality": "Racibórz",
                "postalCode": "47-400",
                "addressRegion": "śląskie",
                "addressCountry": "PL",
            },
        },
        "areaServed": {"@type": "City", "name": m["miasto"],
                       "containedInPlace": {"@type": "AdministrativeArea", "name": f"województwo {m['wojewodztwo']}"}},
    }

    schema_okruszki = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": f"{BAZA}/"},
            {"@type": "ListItem", "position": 2, "name": f"Strony internetowe — {m['miasto']}", "item": url},
        ],
    }

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p,
             "acceptedAnswer": {"@type": "Answer", "text": o}}
            for p, o in m["pytania"]
        ],
    }

    rynek = '\n'.join(f'                    <p>{x}</p>' for x in m["rynek"])
    specyfika = '\n'.join(
        f'''                    <div class="info-card glass reveal">
                        <h3>{bezp(t)}</h3>
                        <p>{o}</p>
                    </div>''' for t, o in m["specyfika"])
    faq = '\n'.join(
        f'''                    <details class="faq-item glass">
                        <summary>{bezp(p)}</summary>
                        <div class="faq-answer">
                            <p>{o}</p>
                        </div>
                    </details>''' for p, o in m["pytania"])
    dowody = '\n'.join(
        f'''                    <a class="miasto-dowod glass reveal" href="/realizacje/{slug}/">
                        <img src="/{obraz}" width="800" height="450" loading="lazy" decoding="async"
                            alt="Strona internetowa {bezp(nazwa)} — {bezp(branza)}">
                        <span class="miasto-dowod-tresc">
                            <strong>{bezp(nazwa)}</strong>
                            <span>{bezp(branza)}</span>
                        </span>
                    </a>''' for nazwa, branza, slug, obraz in DOWODY)

    return f'''<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bezp(TYTUL)}</title>
    <meta name="description" content="{bezp(m["opisMeta"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/png" href="/favicon.png">
    <meta name="theme-color" content="#0a0a0f">

    <!-- Font naglowkow rownolegle z arkuszem: bez tego H1 przemalowuje
         sie po podmianie fontu i LCP przesuwa sie o ~2 s (2026-09-01). -->
    <link rel="preload" href="/fonty/spacegrotesk-700-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonty/spacegrotesk-700-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
        <!-- CSS krytyczny wbudowany: usuwa jeden lot do serwera
         ze sciezki pierwszego malowania. Reszta arkusza dociaga sie
         bez blokowania renderowania. Sklada to tools/krytyczny-css.py
         — nie edytuj tego bloku recznie. -->
    <style id="krytyczny">@font-face{font-family:'Inter Fallback';src:local('Arial');size-adjust:107.09%;ascent-override:90.46%;descent-override:22.52%;line-gap-override:0.00%} @font-face {font-family:'Inter'; font-style:normal; font-weight:300; font-display:swap; src:url(/fonty/inter-300-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/inter-400-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/inter-400-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/inter-500-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/inter-500-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/inter-600-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/inter-600-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/inter-700-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/inter-700-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/spacegrotesk-400-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/spacegrotesk-400-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/spacegrotesk-500-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/spacegrotesk-500-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/spacegrotesk-600-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/spacegrotesk-600-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/spacegrotesk-700-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/spacegrotesk-700-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}:root{--bg-primary:#0a0a0f;--bg-secondary:#12121a;--accent-purple:#8b5cf6;--accent-cyan:#06b6d4;--text-primary:#ffffff;--text-secondary:#a1a1aa;--text-muted:#8a8a93;--glass-bg:rgba(255, 255, 255, 0.03);--glass-border:rgba(255, 255, 255, 0.1);--grad-primary:linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));--grad-surface:linear-gradient(180deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 100%);--section-pady:60px;--header-height:80px;--border-radius:16px;--transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1)}*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}html{scroll-behavior:smooth}body{background-color:var(--bg-primary);color:var(--text-primary);font-family:Inter,'Inter Fallback',sans-serif;line-height:1.6;overflow-x:hidden}.font-special,h1,h2,h3,h4{font-family:'Space Grotesk','Space Grotesk Fallback',sans-serif;font-weight:700}.container{max-width:1200px;margin:0 auto;padding:0 24px}section{padding:var(--section-pady) 0;position:relative}.text-gradient{background:linear-gradient(135deg,var(--accent-purple),var(--accent-cyan),var(--accent-purple));background-size:200% 200%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:inline-block;animation:gradientPulse 4s ease-in-out infinite}.glass{background:var(--glass-bg);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--glass-border);border-radius:var(--border-radius)}.btn{display:inline-flex;align-items:center;padding:12px 24px;border-radius:100px;font-weight:600;text-decoration:none;transition:var(--transition);cursor:pointer;border:none}.btn-primary{background:var(--grad-primary);color:#fff;box-shadow:0 4px 15px rgba(124,58,237,.3)}.btn-outline{border:1px solid var(--glass-border);color:var(--text-primary);background:0 0}header{position:fixed;top:24px;left:50%;transform:translateX(-50%);width:min(95%,1100px);z-index:1000;height:auto;padding:16px 0;display:flex;align-items:center;border-radius:50px;transition:all .5s cubic-bezier(.4, 0, .2, 1)}.nav-container{display:flex;justify-content:space-between;align-items:center;width:100%;padding:0 40px;transition:all .5s ease}.nav-spacer{flex-grow:1;transition:flex-grow .5s ease}.logo{font-size:1.6rem;color:var(--text-primary);text-decoration:none;letter-spacing:-1px;transition:all .5s ease}.logo span{color:var(--accent-cyan)}.nav-links{display:flex;list-style:none;gap:32px;align-items:center}.nav-links a{color:var(--text-secondary);text-decoration:none;font-size:1.05rem;font-weight:500;transition:var(--transition);text-shadow:0 0 10px rgba(255,255,255,0)}.hero{min-height:100vh;display:flex;align-items:center;padding-top:calc(var(--header-height) + 40px);overflow:hidden}.hero-bg{position:absolute;top:0;left:0;width:100%;height:100%;z-index:-1;background:radial-gradient(circle at 70% 30%,rgba(124,58,237,.15),transparent 40%),radial-gradient(circle at 30% 70%,rgba(6,182,212,.15),transparent 40%)}.hero-content{max-width:800px}.hero h1{font-size:clamp(2.8rem, 5.5vw, 4rem);line-height:1.15;margin-bottom:20px;letter-spacing:-1px}.text-white{color:#fff}.text-gradient-alt{background:linear-gradient(135deg,var(--accent-cyan),#3b82f6,#8b5cf6);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;transition:background-position .8s ease}.shimmer{position:relative;background:linear-gradient(to right,var(--accent-purple) 0,var(--accent-cyan) 25%,#fff 50%,var(--accent-cyan) 75%,var(--accent-purple) 100%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer-swipe 8s linear infinite}.hero h1{transition:var(--transition)}.hero p{font-size:1.25rem;color:var(--text-secondary);margin-bottom:40px;max-width:600px}.hero-btns{display:flex;gap:16px}.delay-1{transition-delay:0.2s}.delay-2{transition-delay:0.4s}.delay-3{transition-delay:0.6s}.scroll-indicator{position:absolute;bottom:30px;left:50%;transform:translateX(-50%)}.mouse{width:26px;height:42px;border:2px solid var(--text-muted);border-radius:20px;position:relative}.menu-toggle{display:none;flex-direction:column;gap:6px;cursor:pointer;background:0 0;border:none;padding:8px;border-radius:8px;transition:var(--transition)}.menu-toggle span{display:block;width:26px;height:2px;background:var(--text-primary);border-radius:2px;transition:var(--transition)}.reveal{opacity:0;transform:translateY(40px);transition:all .8s cubic-bezier(.4, 0, .2, 1)}.reveal.active{opacity:1;transform:translateY(0)}@media (max-width:768px){.menu-toggle{display:flex}.nav-links{display:flex!important;position:absolute;top:calc(100% + 10px);left:0;width:100%;background:rgba(10,10,15,.95);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--glass-border);border-radius:24px;flex-direction:column;padding:30px;align-items:center;gap:20px;opacity:0;visibility:hidden;transform:translateY(-20px);transition:all .3s ease;z-index:999}.nav-links.active{opacity:1;visibility:visible;transform:translateY(0)}.hero h1{font-size:3rem}.hero-btns{flex-direction:column}.stats-grid{grid-template-columns:1fr}.section-header h2{font-size:2rem}.menu-toggle.open span:first-child{transform:rotate(45deg) translate(5px,6px)}.menu-toggle.open span:nth-child(2){opacity:0}.menu-toggle.open span:last-child{transform:rotate(-45deg) translate(5px,-6px)}}html{scrollbar-width:thin;scrollbar-color:var(--accent-purple) var(--bg-primary)}.floating-phone-btn{display:none;position:fixed;bottom:90px;right:30px;width:50px;height:50px;border-radius:50%;z-index:9999;align-items:center;justify-content:center;background:var(--bg-secondary);text-decoration:none;transition:opacity .4s ease,transform .4s ease}.floating-phone-btn svg{width:22px;height:22px}@media (max-width:768px){.floating-phone-btn{display:flex;bottom:80px;right:20px;width:44px;height:44px}.floating-phone-btn svg{width:20px;height:20px}}.scroll-top-btn{position:fixed;bottom:30px;right:30px;width:50px;height:50px;border-radius:50%;border:none;cursor:pointer;z-index:9999;display:flex;align-items:center;justify-content:center;background:var(--bg-secondary);opacity:0;visibility:hidden;transform:translateY(20px);transition:opacity .4s ease,visibility .4s ease,transform .4s ease}.scroll-top-btn svg{width:22px;height:22px;fill:none;stroke:url(#arrow-grad);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:transform .3s ease}@media (max-width:768px){:root{--section-pady:60px}header{width:95%!important}header.scrolled{width:90%!important}.nav-links{display:none}.nav-links.active{display:flex!important}.menu-toggle{display:flex!important}.nav-container{padding:0 20px}.hero{padding-top:calc(var(--header-height) + 20px)}.hero h1{font-size:clamp(2rem, 6vw, 2.8rem)}.hero p{font-size:.95rem}.hero-btns{flex-direction:column;gap:12px}.hero-btns .btn{width:100%;text-align:center}.section-header h2{font-size:clamp(1.6rem, 5vw, 2.2rem)}.section-header{margin-bottom:40px}.stats-grid{grid-template-columns:1fr;gap:16px}.stat-number{font-size:2.5rem}.services-grid{grid-template-columns:1fr}.service-card{padding:28px}.portfolio-grid{grid-template-columns:1fr;gap:24px}.process-steps{grid-template-columns:1fr 1fr;gap:24px}.needs-grid{grid-template-columns:1fr}.why-grid{grid-template-columns:1fr}.contact-cta{padding:40px 24px}.phone-cta{padding:20px 24px;gap:16px}.phone-digits{font-size:1.4rem}.contact-secondary{flex-direction:column;gap:16px;align-items:center}.footer-grid{grid-template-columns:1fr;gap:32px;text-align:center}.footer-tagline{max-width:none}.footer-bottom{flex-direction:column;gap:8px;text-align:center}.scroll-top-btn{bottom:20px;right:20px;width:44px;height:44px}}@media (max-width:480px){:root{--section-pady:48px}.container{padding:0 16px}.hero h1{font-size:1.8rem;letter-spacing:-.5px}.hero p{font-size:.9rem}.section-header h2{font-size:1.5rem}.stats-grid{grid-template-columns:1fr;gap:16px}.stat-number{font-size:2.2rem}.process-steps{grid-template-columns:1fr}.step-num{font-size:3rem}.project-img{height:200px}.need-item{padding:24px}.phone-cta{flex-direction:column;text-align:center}.phone-number{align-items:center}.phone-digits{font-size:1.6rem}.tech-track span:not(.tech-sep){font-size:1.1rem;padding:4px 8px}}@media (max-width:768px){.hero{align-items:flex-start!important;padding-top:calc(var(--header-height) + 30px)!important;min-height:85vh!important}.hero-content{margin-top:.5rem}.hero h1{font-size:clamp(2rem, 7vw, 2.9rem)!important}}.reveal-hero{animation:hero-wjazd .7s cubic-bezier(.4,0,.2,1) both}.reveal-hero.delay-1{animation-delay:.15s}.reveal-hero.delay-2{animation-delay:.3s}.reveal-hero.delay-3{animation-delay:.45s}@media (prefers-reduced-motion:reduce){.reveal-hero{animation:none}}

@media (prefers-reduced-motion: reduce) {

    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }

    .reveal {
        opacity: 1;
        transform: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    .info-card::before,
    .info-card::after {
        transition: none;
    }
}

@media (min-width: 1281px) {
    .nav-links {
        gap: 26px;
    }

    .nav-links a {
        font-size: 1rem;
    }
}

@media (max-width: 1280px) {
    .menu-toggle {
        display: flex;
    }

    .nav-links {
        display: flex !important;
        position: absolute;
        top: calc(100% + 10px);
        left: 0;
        width: 100%;
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        flex-direction: column;
        padding: 30px;
        align-items: center;
        gap: 20px;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-20px);
        transition: all 0.3s ease;
        z-index: 999;
    }

    .nav-links.active {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }

    /* Hamburger — animacja krzyżyka */
    .menu-toggle.open span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 6px);
    }

    .menu-toggle.open span:nth-child(2) {
        opacity: 0;
    }

    .menu-toggle.open span:nth-last-child(1) {
        transform: rotate(-45deg) translate(5px, -6px);
    }
}

@media (prefers-reduced-motion: reduce) {
    .faq-item::details-content { transition: none; }
    /* lagodniej, nie zero: samo przenikanie, bez ruchu w pionie */
    .form-status { transition: opacity 250ms ease-out; transform: none; }
}

@media (prefers-reduced-motion: reduce) {
    .karuzela-tor { scroll-behavior: auto; }
    .blog-karta:hover .blog-karta-obraz img { transform: none; }
    .karuzela-kropka,
    .karuzela-kropka::before { transition: none; }
}

/* ---- Animacje ozdobne nad zagieciem: skonczona liczba przebiegow -------
   Speed Index mierzy, jak dlugo WIDOCZNY obszar sie zmienia. Nieskonczona
   animacja w hero sprawia, ze strona nigdy nie jest wizualnie gotowa,
   a zaden pozniejszy fragment nie ma juz szans tego odrobic.

   Zmierzone 2026-09-01 na komputerze: FCP 0,2 s i LCP 0,8 s (oceny 1,00
   i 0,97), a mimo to wydajnosc 81 — bo Speed Index wyszedl 6,6 s z ocena
   ZERO. Winne byly puls gradientu i polysk na naglowku hero, chodzace
   w kolko od pierwszej klatki.

   Zostaja jako efekt WEJSCIA: gradient przechodzi dwa razy, polysk raz
   i obraz sie uspokaja. Naglowki sekcji nizej zachowuja puls bez zmian
   — sa pod zagieciem, wiec pomiaru nie dotykaja. */
.hero .text-gradient,
.hero .text-gradient-alt {
    animation-iteration-count: 2;
}

.hero .shimmer {
    animation-iteration-count: 1;
}@keyframes gradientPulse{0%,100%{background-position:0 50%}50%{background-position:100% 50%}}@keyframes shimmer-swipe{0%{background-position:-200% center}100%{background-position:200% center}}@keyframes hero-wjazd{from{transform:translateY(40px)}to{transform:translateY(0)}}</style>
    <link rel="preload" href="/style.css?v={stempel}" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/style.css?v={stempel}"></noscript>

    <meta property="og:type" content="website">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:site_name" content="WebStudio47">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="Strony internetowe {bezp(m["miasto"])} | WebStudio47">
    <meta property="og:description" content="{bezp(m["opisMeta"])}">
    <meta property="og:image" content="{BAZA}/og-image.jpg">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Strony internetowe {bezp(m["miasto"])} | WebStudio47">
    <meta name="twitter:description" content="{bezp(m["opisMeta"])}">
    <meta name="twitter:image" content="{BAZA}/og-image.jpg">

    <!-- Zgoda na cookies (Google Consent Mode v2) — MUSI byc przed gtag.js -->
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

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NV6W571RJB"></script>
    <script>
        gtag('js', new Date());
        gtag('config', 'G-NV6W571RJB', {{ anonymize_ip: true }});
    </script>

    <script type="application/ld+json">
{json.dumps(schema_uslugi, ensure_ascii=False, indent=2)}
    </script>

    <script type="application/ld+json">
{json.dumps(schema_okruszki, ensure_ascii=False, indent=2)}
    </script>

    <script type="application/ld+json">
{json.dumps(schema_faq, ensure_ascii=False, indent=2)}
    </script>
</head>

<body>

    <header id="main-header">
        <div class="container nav-container">
            <a href="/" class="logo font-special">&lt;WebStudio<span>47</span>&gt;</a>
            <div class="nav-spacer"></div>
            <nav>
                <ul class="nav-links">
                    <li><a href="/tworzenie-stron-internetowych-raciborz/">Strony&nbsp;WWW</a></li>
                    <li><a href="/pozycjonowanie-stron-raciborz/">Pozycjonowanie</a></li>
                    <li><a href="/portfolio.html">Realizacje</a></li>
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

    <main>

        <section class="page-hero">
            <div class="container">
                <nav class="breadcrumbs" aria-label="Okruszki">
                    <a href="/">Strona główna</a>
                    <span aria-hidden="true">›</span>
                    <span>Strony internetowe — {bezp(m["miasto"])}</span>
                </nav>
                <h1 class="reveal-hero"><span class="text-white">Strony internetowe</span><br>
                    <span class="text-gradient">{bezp(m["miasto"])}</span></h1>
                <p class="page-hero-lead reveal-hero delay-1">{m["lead"]}</p>
                <div class="page-hero-btns reveal-hero delay-2">
                    <a href="tel:+48602622840" class="btn btn-primary">Zadzwoń: 602 622 840</a>
                    <a href="/cennik/" class="btn btn-outline">Zobacz widełki cenowe</a>
                </div>
                <div class="hero-trust reveal delay-3">
                    <span>Z Raciborza {bezp(m["dojazd"])} drogi</span>
                    <span>Cały projekt można poprowadzić zdalnie</span>
                    <span>Wycena wiążąca po rozmowie</span>
                </div>
            </div>
        </section>

        <section class="section-alt">
            <div class="container">
                <div class="prose reveal">
                    <h2>Jak wygląda rynek w&nbsp;{bezp(m["miastoMs"])}</h2>
{rynek}
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Co to zmienia w praktyce</h2>
                    <p>Konkretne konsekwencje dla Twojego projektu</p>
                </div>
                <div class="card-grid">
{specyfika}
                </div>
            </div>
        </section>

        <section class="section-alt">
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Zobacz, co robię</h2>
                    <p>Realizacje z Raciborza i okolic — każdą możesz otworzyć na żywo</p>
                </div>
                <div class="miasto-dowody">
{dowody}
                </div>
                <div style="text-align:center; margin-top:34px" class="reveal">
                    <a href="/portfolio.html" class="btn btn-outline">Wszystkie realizacje →</a>
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Częste pytania</h2>
                </div>
                <div class="faq-list reveal">
{faq}
                </div>
            </div>
        </section>

        <section class="section-alt">
            <div class="container">
                <div class="cta-band glass reveal">
                    <h2 class="text-gradient">Porozmawiajmy o Twojej stronie</h2>
                    <p>Piętnaście minut przez telefon i&nbsp;wiesz, ile to kosztuje, ile potrwa i&nbsp;czy w&nbsp;Twojej
                        branży w {bezp(m["miastoMs"])} w ogóle warto. Bez zobowiązań.</p>
                    <div class="cta-band-btns">
                        <a href="tel:+48602622840" class="btn btn-primary">Zadzwoń: 602 622 840</a>
                        <a href="/kontakt/" class="btn btn-outline">Opisz swój projekt</a>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div class="footer-logo font-special">&lt;WebStudio<span>47</span>&gt;</div>
                    <p class="footer-tagline">Strony internetowe dla firm, które traktują swój biznes poważnie. Nie
                        robię stron dla każdego — i&nbsp;właśnie dlatego te, które robię, wyglądają tak, jak wyglądają.</p>
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


def main():
    stempel = int(time.time())
    for m in MIASTA:
        cel = KATALOG / m['slug']
        cel.mkdir(exist_ok=True)
        tresc = strona(m, stempel)
        (cel / 'index.html').write_text(tresc, encoding='utf-8')
        print(f"  {m['slug']}/  ({len(tresc) // 1024} KB)")
    print(f"\nWygenerowano {len(MIASTA)} stron lokalnych, stempel ?v={stempel}")


if __name__ == '__main__':
    main()
