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
    <link rel="stylesheet" href="/style.css?v={stempel}">

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
