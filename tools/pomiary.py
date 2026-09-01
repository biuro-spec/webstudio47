# -*- coding: utf-8 -*-
"""
Wyniki Lighthouse dla realizacji — dane i renderowanie sekcji.

Od 2026-09-01 dwie strategie: komórka i komputer, bo pokazywanie tylko
korzystniejszej byłoby deklarowaniem, nie mierzeniem. Klient po kliknięciu
„sprawdź sam" widzi w PSI obie zakładki — my też pokazujemy obie.

Źródło liczb: docelowo API PageSpeed Insights (tools/zmierz-psi.py) —
te same serwery Google, które otworzy klient. Pomiar lokalny potrafił
się mylić o 40 punktów przy TBT (97 vs 58 na tej samej stronie).

Brak pomiaru (None) = sekcja lub wiersz się nie pojawia. Nie zgadujemy:
  - Life-Centrum — projekt w realizacji, pod domeną stoi cudzy WordPress.
  Alaska od 2026-09-01 MA pomiar: serwery Google przebijają blokadę
  home.pl, o którą rozbijał się pomiar lokalny.

Aktualizacja: python tools/zmierz-psi.py i wklej wynik do POMIARY.
"""

DATA_POMIARU = "1 września 2026"

# Obie strategie z JEDNEGO źródła: PSI API (serwery Google), 2026-09-01.
# Odświeżenie: python tools/zmierz-psi.py (klucz w env PSI_KLUCZ) i wklej.
POMIARY = {
    "hOla Perros":      {"mobile": {"performance": 92, "accessibility": 100, "best-practices": 100, "seo": 100}, "desktop": {"performance": 100, "accessibility": 100, "best-practices": 100, "seo": 100}},
    "Super Irek":       {"mobile": {"performance": 89, "accessibility": 100, "best-practices": 100, "seo": 100}, "desktop": {"performance": 97, "accessibility": 100, "best-practices": 100, "seo": 100}},
    "Czysto-Po":        {"mobile": {"performance": 77, "accessibility": 94, "best-practices": 100, "seo": 100}, "desktop": {"performance": 99, "accessibility": 94, "best-practices": 100, "seo": 100}},
    "Alaska":           {"mobile": {"performance": 67, "accessibility": 100, "best-practices": 100, "seo": 100}, "desktop": {"performance": 96, "accessibility": 100, "best-practices": 100, "seo": 100}},
    "Life-Centrum":     {"mobile": None, "desktop": None},
    "Life-Ratownictwo": {"mobile": {"performance": 90, "accessibility": 100, "best-practices": 100, "seo": 100}, "desktop": {"performance": 99, "accessibility": 100, "best-practices": 100, "seo": 100}},
    "WystawFakture.eu": {"mobile": {"performance": 88, "accessibility": 98, "best-practices": 96, "seo": 100}, "desktop": {"performance": 99, "accessibility": 98, "best-practices": 96, "seo": 100}},
    "9 Dom":            {"mobile": {"performance": 73, "accessibility": 96, "best-practices": 100, "seo": 100}, "desktop": {"performance": 94, "accessibility": 96, "best-practices": 100, "seo": 100}},
    "Karta Dnia":       {"mobile": {"performance": 97, "accessibility": 100, "best-practices": 100, "seo": 100}, "desktop": {"performance": 100, "accessibility": 100, "best-practices": 100, "seo": 100}},
}

KATEGORIE = [
    ("performance", "Wydajność"),
    ("accessibility", "Dostępność"),
    ("best-practices", "Sprawdzone metody"),
    ("seo", "SEO"),
]

ETYKIETY_STRATEGII = [("mobile", "Komórka"), ("desktop", "Komputer")]


def poziom(wynik):
    """Progi Lighthouse: zielony od 90, pomarańczowy od 50."""
    if wynik >= 90:
        return "dobry"
    if wynik >= 50:
        return "sredni"
    return "slaby"


def wiersz(w, etykieta):
    karty = []
    for klucz, nazwa in KATEGORIE:
        wynik = w[klucz]
        karty.append(
            '                    <div class="wynik" data-poziom="' + poziom(wynik) + '">\n'
            '                        <span class="wynik-liczba">' + str(wynik) + '</span>\n'
            '                        <span class="wynik-nazwa">' + nazwa + '</span>\n'
            '                    </div>'
        )
    return ('                <p class="wyniki-tryb">' + etykieta + '</p>\n'
            '                <div class="wyniki reveal">\n'
            + '\n'.join(karty) + '\n'
            '                </div>\n')


def sekcja(klient, domena):
    """Blok z wynikami. Pusty, gdy nie ma ŻADNEGO pomiaru — nie zgadujemy."""
    dane = POMIARY.get(klient) or {}
    wiersze = [wiersz(dane[s], etyk) for s, etyk in ETYKIETY_STRATEGII if dane.get(s)]
    if not wiersze:
        return ""

    sprawdz = 'https://pagespeed.web.dev/analysis?url=https%3A%2F%2F' + domena + '%2F'
    return (
        '\n        <!-- Pomiary Lighthouse -->\n'
        '        <section>\n'
        '            <div class="container">\n'
        '                <div class="section-header reveal">\n'
        '                    <h2 class="text-gradient">Zmierzone, nie deklarowane</h2>\n'
        '                    <p>Lighthouse — pomiar z ' + DATA_POMIARU + '</p>\n'
        '                </div>\n'
        + ''.join(wiersze) +
        '                <p class="wyniki-nota">Skala 0–100, im wyżej tym lepiej. Nie musisz mi wierzyć —\n'
        '                    sprawdź sam w <a href="' + sprawdz + '" target="_blank" rel="noopener">PageSpeed\n'
        '                    Insights</a>. Wynik wydajności waha się między pomiarami i zależy od łącza,\n'
        '                    dlatego podaję datę.</p>\n'
        '            </div>\n'
        '        </section>\n'
    )


def podsumowanie(strategia="mobile"):
    """Zakresy i średnie po zmierzonych realizacjach (jedna strategia)."""
    zmierzone = [d[strategia] for d in POMIARY.values() if d.get(strategia)]
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
