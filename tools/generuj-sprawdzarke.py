#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator strony /sprawdz-swoja-strone/.

Darmowe narzędzie: odwiedzający wpisuje adres własnej strony i trafia
do PageSpeed Insights z gotowym wynikiem. Świadomie NIE liczymy nic sami —
wynik od Google jest wiarygodniejszy niż liczba podana przez wykonawcę,
który chce sprzedać poprawki.

Formularz działa BEZ JavaScriptu: `action` prowadzi wprost do PSI, a metoda
GET buduje `?url=`. JS tylko dokleja `https://`, gdy ktoś go pominie.

Uruchomienie:  python tools/generuj-sprawdzarke.py
"""

import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pomiary

KATALOG = pathlib.Path(__file__).resolve().parent.parent
BAZA = "https://webstudio47.pl"
FB = "https://www.facebook.com/profile.php?id=61578430357755"
URL = f"{BAZA}/sprawdz-swoja-strone/"

TYTUL = "Sprawdź swoją stronę — darmowy test | WebStudio47"
OPIS = ("Sprawdź swoją stronę w Google PageSpeed Insights i dowiedz się, co "
        "znaczą wyniki. Darmowo, bez rejestracji, bez zostawiania e-maila.")

# Co znaczy każda kategoria — językiem właściciela firmy, nie programisty
KATEGORIE = [
    ("Wydajność",
     "Jak szybko strona się otwiera na telefonie.",
     "Poniżej 50 znaczy, że część odwiedzających wychodzi, zanim cokolwiek "
     "zobaczy. To najczęściej wina nieskompresowanych zdjęć — i zwykle "
     "najtańsza rzecz do naprawienia."),
    ("Dostępność",
     "Czy stronę da się obsłużyć bez myszki i czy przeczyta ją czytnik ekranu.",
     "Dotyczy osób słabowidzących i starszych, ale nie tylko: Google używa "
     "tych samych sygnałów do oceny, czy strona jest zrobiona porządnie."),
    ("Sprawdzone metody",
     "Czy strona jest zbudowana zgodnie ze standardami sieci.",
     "Niski wynik zwykle oznacza błędy w konsoli, brak HTTPS albo obrazy "
     "podane w złych rozmiarach. Rzeczy niewidoczne dla Ciebie, widoczne "
     "dla wyszukiwarki."),
    ("SEO",
     "Czy Google w ogóle jest w stanie zrozumieć, o czym jest ta strona.",
     "To absolutne minimum, nie pozycjonowanie. Sto punktów tutaj nie znaczy, "
     "że jesteś wysoko w wynikach — znaczy, że nic nie stoi na przeszkodzie."),
]

PYTANIA = [
    ("Czy ten test coś kosztuje?",
     "Nie. To narzędzie Google, całkowicie darmowe i bez rejestracji. "
     "Nie zbieram Twojego adresu ani wyniku — po kliknięciu trafiasz wprost "
     "na stronę Google, a ja nie dowiaduję się, że w ogóle tu byłeś."),
    ("Mam niski wynik wydajności. To źle?",
     "Zależy jak niski i jaka to strona. Poniżej 50 na telefonie to realny "
     "problem: część odwiedzających wychodzi, zanim strona się pokaże. "
     "Między 50 a 90 jest do poprawienia, ale nie pali się. Powyżej 90 nie ma "
     "o czym mówić. Najczęstsza przyczyna niskiego wyniku to nieskompresowane "
     "zdjęcia — i to zwykle najtańsza rzecz do naprawienia."),
    ("Wynik zmienia się przy każdym sprawdzeniu. Dlaczego?",
     "Bo Google mierzy rzeczywiste ładowanie, a to zależy od obciążenia "
     "serwera i łącza w danej chwili. Wahania o kilka punktów są normalne. "
     "Jeśli chcesz mieć pewność, zmierz trzy razy i weź wynik środkowy."),
    ("Czy 100 punktów w SEO znaczy, że będę wysoko w Google?",
     "Nie. Ta kategoria sprawdza wyłącznie, czy nic nie blokuje wyszukiwarce "
     "zrozumienia strony: czy jest tytuł, opis, czy treść nie jest ukryta. "
     "To warunek konieczny, nie wystarczający. O pozycji decyduje treść, "
     "konkurencja i wiarygodność strony."),
    ("Naprawiacie takie rzeczy?",
     "Tak, ale najpierw powiem, czy warto. Czasem wystarczy skompresować "
     "zdjęcia i wynik skacze o trzydzieści punktów. Czasem strona jest "
     "zbudowana tak, że taniej napisać ją od nowa niż łatać. Na 15-minutowej "
     "rozmowie mówię, w której z tych sytuacji jesteś — również wtedy, gdy "
     "odpowiedź brzmi: nic nie rób."),
]


def podsumowanie_html():
    p = pomiary.podsumowanie()
    karty = []
    for klucz, _ in pomiary.KATEGORIE:
        d = p[klucz]
        zakres = f'{d["min"]}–{d["max"]}' if d["min"] != d["max"] else str(d["min"])
        szczegol = (f'średnia {d["srednia"]}, w tym {d["setek"]} '
                    f'{"wynik" if d["setek"] == 1 else "wyników"} po 100')
        karty.append(
            '                    <div class="wynik-zbiorczy glass reveal">\n'
            f'                        <h3>{d["etykieta"]}</h3>\n'
            f'                        <span class="zakres">{zakres}</span>\n'
            f'                        <span class="szczegol">{szczegol}</span>\n'
            '                    </div>')
    return '\n'.join(karty)


def kategorie_html():
    return '\n'.join(
        '                    <div class="info-card glass reveal">\n'
        f'                        <h3>{nazwa}</h3>\n'
        f'                        <p><strong>{co}</strong></p>\n'
        f'                        <p style="margin-top:10px">{kiedy}</p>\n'
        '                    </div>'
        for nazwa, co, kiedy in KATEGORIE)


def faq_html():
    return '\n'.join(
        '                    <details class="faq-item glass">\n'
        f'                        <summary>{p}</summary>\n'
        '                        <div class="faq-answer">\n'
        f'                            <p>{o}</p>\n'
        '                        </div>\n'
        '                    </details>'
        for p, o in PYTANIA)


def schematy(stempel):
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p,
             "acceptedAnswer": {"@type": "Answer", "text": o}}
            for p, o in PYTANIA
        ],
    }
    okruszki = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": f"{BAZA}/"},
            {"@type": "ListItem", "position": 2, "name": "Sprawdź swoją stronę", "item": URL},
        ],
    }
    narzedzie = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Sprawdź swoją stronę",
        "url": URL,
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Dowolna przeglądarka",
        "description": OPIS,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "PLN"},
        "provider": {
            "@type": "ProfessionalService",
            "name": "WebStudio47",
            "@id": f"{BAZA}/#organizacja",
            "url": BAZA,
            "telephone": "+48602622840",
            "sameAs": [FB],
        },
    }
    return '\n'.join(
        '    <script type="application/ld+json">\n'
        + json.dumps(s, ensure_ascii=False, indent=2)
        + '\n    </script>\n' for s in (narzedzie, okruszki, faq))


def buduj(stempel):
    return f'''<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TYTUL}</title>
    <meta name="description" content="{OPIS}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{URL}">
    <link rel="icon" type="image/png" href="/favicon.png">
    <meta name="theme-color" content="#0a0a0f">

    <link rel="preload" as="font" type="font/woff2" href="/fonty/spacegrotesk-700-latin.woff2" crossorigin>
    <link rel="preload" as="font" type="font/woff2" href="/fonty/spacegrotesk-700-latin-ext.woff2" crossorigin>
    <link rel="stylesheet" href="/style.css?v={stempel}">
    <link rel="stylesheet" href="/page-style.css?v={stempel}">

    <meta property="og:type" content="website">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:site_name" content="WebStudio47">
    <meta property="og:url" content="{URL}">
    <meta property="og:title" content="{TYTUL}">
    <meta property="og:description" content="{OPIS}">
    <meta property="og:image" content="{BAZA}/og-image.png">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{TYTUL}">
    <meta name="twitter:description" content="{OPIS}">
    <meta name="twitter:image" content="{BAZA}/og-image.png">

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

{schematy(stempel)}</head>

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
                    <span>Sprawdź swoją stronę</span>
                </nav>
                <h1 class="reveal-hero"><span class="text-white">Sprawdź</span> <span class="text-gradient">swoją stronę</span></h1>
                <p class="page-hero-lead reveal-hero delay-1">Wpisz adres i zobacz, co Google sądzi o Twojej stronie.
                    Za darmo, bez rejestracji i bez zostawiania mi e-maila. Wynik dostajesz wprost od Google,
                    nie ode mnie.</p>

                <form class="sprawdzarka reveal delay-2" id="sprawdzarka"
                    action="https://pagespeed.web.dev/analysis" method="get" target="_blank" rel="noopener">
                    <label for="adres" class="sr-only">Adres Twojej strony internetowej</label>
                    <input type="text" id="adres" name="url" inputmode="url" autocomplete="url"
                        placeholder="twojafirma.pl" required>
                    <button type="submit" class="btn btn-primary">Sprawdź</button>
                </form>
                <p class="sprawdzarka-nota reveal delay-3">Otworzy się PageSpeed Insights — narzędzie Google.
                    Analiza trwa kilkanaście sekund.</p>
            </div>
        </section>

        <section class="section-alt">
            <div class="container">
                <div class="prose reveal">
                    <h2>Co znaczą te cztery liczby</h2>
                    <p>Google ocenia stronę w czterech kategoriach, każdą w skali <strong>od 0 do 100</strong>.
                        Wynik <strong>90 lub więcej jest dobry</strong>, między 50 a 89 wymaga poprawy,
                        poniżej 50 to realny problem. Poniżej tłumaczę, co każda z nich naprawdę mierzy —
                        bo nazwy niewiele mówią, a nie każda liczy się tak samo.</p>
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <div class="card-grid">
{kategorie_html()}
                </div>
            </div>
        </section>

        <section class="section-alt">
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Dla porównania — moje realizacje</h2>
                    <p>Osiem stron zmierzonych {pomiary.DATA_POMIARU}, profil mobilny</p>
                </div>
                <div class="wyniki-zbiorcze">
{podsumowanie_html()}
                </div>
                <p class="wyniki-nota">Podaję też słabsze wyniki, bo i tak możesz je sprawdzić.
                    <strong>Wydajność 57–93</strong> to uczciwy obraz: przy stronach z dużą liczbą zdjęć
                    schodzi niżej i jest to obszar, nad którym pracuję. Każdą realizację i jej wynik
                    zobaczysz w <a href="/portfolio.html">portfolio</a>.</p>
            </div>
        </section>

        <section>
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Częste pytania</h2>
                </div>
                <div class="faq-list reveal">
{faq_html()}
                </div>
            </div>
        </section>

        <section class="section-alt">
            <div class="container">
                <div class="cta-band glass reveal">
                    <h2 class="text-gradient">Wynik Cię zaniepokoił?</h2>
                    <p>Zadzwoń i przeczytaj mi liczby. W piętnaście minut powiem, co je psuje, ile kosztuje
                        naprawa i czy w Twoim przypadku w ogóle warto. Bywa, że odpowiedź brzmi: nic nie rób.</p>
                    <div class="cta-band-btns">
                        <a href="tel:+48602622840" class="btn btn-primary">Zadzwoń: 602 622 840</a>
                        <a href="/kontakt/" class="btn btn-outline">Napisz wiadomość</a>
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
                        robię stron dla każdego — i właśnie dlatego te, które robię, wyglądają tak, jak wyglądają.</p>
                </div>
                <div class="footer-nav">
                    <p class="footer-heading">Oferta</p>
                    <ul>
                        <li><a href="/tworzenie-stron-internetowych-raciborz/">Strony internetowe</a></li>
                        <li><a href="/pozycjonowanie-stron-raciborz/">Pozycjonowanie</a></li>
                        <li><a href="/cennik/">Cennik</a></li>
                        <li><a href="/portfolio.html">Realizacje</a></li>
                        <li><a href="/sprawdz-swoja-strone/">Sprawdź swoją stronę</a></li>
                        <li><a href="/kontakt/">Kontakt</a></li>
                    </ul>
                </div>
                <div class="footer-nav footer-miasta">
                    <p class="footer-heading">Obsługuję</p>
                    <ul>
                        <li><a href="/tworzenie-stron-internetowych-raciborz/">Racibórz</a></li>
                        <li><a href="/strony-internetowe-wodzislaw-slaski/">Wodzisław Śląski</a></li>
                        <li><a href="/strony-internetowe-rybnik/">Rybnik</a></li>
                        <li><a href="/strony-internetowe-kedzierzyn-kozle/">Kędzierzyn-Koźle</a></li>
                        <li><a href="/strony-internetowe-glubczyce/">Głubczyce</a></li>
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

    <script>
        // Formularz dziala BEZ tego skryptu — `action` prowadzi wprost do PSI,
        // a metoda GET buduje ?url=. To tylko dokleja https:// gdy ktos pominie
        // schemat, bo PageSpeed bez niego nie ruszy.
        (function () {{
            var f = document.getElementById('sprawdzarka');
            if (!f) return;
            f.addEventListener('submit', function () {{
                var pole = f.elements.url;
                var v = pole.value.trim();
                if (v && !/^https?:\\/\\//i.test(v)) pole.value = 'https://' + v;
                if (typeof gtag === 'function') {{
                    gtag('event', 'sprawdzenie_strony', {{ event_category: 'narzedzie' }});
                }}
            }});
        }})();
    </script>

    <script src="/script.js?v={stempel}" defer></script>
    <script src="/consent.js?v={stempel}" defer></script>
</body>

</html>
'''


def main():
    stempel = int(time.time())
    cel = KATALOG / 'sprawdz-swoja-strone'
    cel.mkdir(exist_ok=True)
    tresc = buduj(stempel)
    (cel / 'index.html').write_text(tresc, encoding='utf-8')
    print(f'  sprawdz-swoja-strone/  ({len(tresc) // 1024} KB)')
    print(f'  tytul: {len(TYTUL)} znakow, opis: {len(OPIS)} znakow')


if __name__ == '__main__':
    main()
