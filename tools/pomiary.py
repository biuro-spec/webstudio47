# -*- coding: utf-8 -*-
"""
Wyniki Lighthouse dla realizacji — dane i renderowanie sekcji.

Prawdziwe pomiary, wykonane lokalnie Lighthouse 12.8.2 w profilu mobilnym.
Pokazujemy WSZYSTKIE cztery kategorie, także słabsze: strona jest zbudowana
na mówieniu wprost, a klient i tak sprawdzi sam w PageSpeed Insights.

Dwie realizacje nie mają pomiaru i to jest celowe:
  - Alaska — home.pl blokuje ruch z tego środowiska,
  - Life-Centrum — pod adresem stoi jeszcze WordPress klienta, a nasza
    wersja nie jest wdrożona. Pokazywanie jej wyniku jako własnego
    byłoby przypisywaniem sobie cudzej pracy.
Zamiast zgadywać albo mierzyć nie to co trzeba, sekcja się nie pojawia.

Aktualizacja: uruchom pomiar ponownie i podmień słownik POMIARY.
"""

DATA_POMIARU = "31 sierpnia 2026"

POMIARY = {
    "hOla Perros":      {"performance": 90, "accessibility": 100, "best-practices": 100, "seo": 100},
    "Super Irek":       {"performance": 72, "accessibility": 100, "best-practices": 100, "seo": 100},
    "Czysto-Po":        {"performance": 64, "accessibility": 94, "best-practices": 100, "seo": 100},
    "Alaska":           {"performance": None, "accessibility": None, "best-practices": None, "seo": None},
    "Life-Centrum":     {"performance": None, "accessibility": None, "best-practices": None, "seo": None},
    "Life-Ratownictwo": {"performance": 91, "accessibility": 100, "best-practices": 100, "seo": 100},
    "WystawFakture.eu": {"performance": 64, "accessibility": 98, "best-practices": 96, "seo": 100},
    "9 Dom":            {"performance": 81, "accessibility": 96, "best-practices": 100, "seo": 100},
    "Karta Dnia":       {"performance": 84, "accessibility": 100, "best-practices": 100, "seo": 100},
}

KATEGORIE = [
    ("performance", "Wydajność"),
    ("accessibility", "Dostępność"),
    ("best-practices", "Sprawdzone metody"),
    ("seo", "SEO"),
]


def poziom(wynik):
    """Progi Lighthouse: zielony od 90, pomarańczowy od 50."""
    if wynik >= 90:
        return "dobry"
    if wynik >= 50:
        return "sredni"
    return "slaby"


def sekcja(klient, domena):
    """Blok z wynikami. Pusty, gdy pomiaru nie ma — nie zgadujemy liczb."""
    w = POMIARY.get(klient)
    if not w or w.get("performance") is None:
        return ""

    karty = []
    for klucz, etykieta in KATEGORIE:
        wynik = w[klucz]
        karty.append(
            '                    <div class="wynik" data-poziom="' + poziom(wynik) + '">\n'
            '                        <span class="wynik-liczba">' + str(wynik) + '</span>\n'
            '                        <span class="wynik-nazwa">' + etykieta + '</span>\n'
            '                    </div>'
        )

    sprawdz = 'https://pagespeed.web.dev/analysis?url=https%3A%2F%2F' + domena + '%2F'

    return (
        '\n        <!-- Pomiary Lighthouse -->\n'
        '        <section>\n'
        '            <div class="container">\n'
        '                <div class="section-header reveal">\n'
        '                    <h2 class="text-gradient">Zmierzone, nie deklarowane</h2>\n'
        '                    <p>Lighthouse, profil mobilny — pomiar z ' + DATA_POMIARU + '</p>\n'
        '                </div>\n'
        '                <div class="wyniki reveal">\n'
        + '\n'.join(karty) + '\n'
        '                </div>\n'
        '                <p class="wyniki-nota">Skala 0–100, im wyżej tym lepiej. Nie musisz mi wierzyć —\n'
        '                    sprawdź sam w <a href="' + sprawdz + '" target="_blank" rel="noopener">PageSpeed\n'
        '                    Insights</a>. Wynik wydajności waha się między pomiarami i zależy od łącza,\n'
        '                    dlatego podaję datę.</p>\n'
        '            </div>\n'
        '        </section>\n'
    )


def podsumowanie():
    """Zakresy i średnie po wszystkich zmierzonych realizacjach."""
    zmierzone = [w for w in POMIARY.values() if w["performance"] is not None]
    wynik = {}
    for klucz, etykieta in KATEGORIE:
        v = sorted(w[klucz] for w in zmierzone)
        wynik[klucz] = {
            "etykieta": etykieta,
            "min": v[0],
            "max": v[-1],
            "srednia": round(sum(v) / len(v)),
            "setek": sum(1 for x in v if x == 100),
            "ile": len(v),
        }
    return wynik
