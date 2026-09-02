#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator poziomej galerii usług na stronie głównej.

Wzorzec przeniesiony z projektu „Mapa dłoni”: scena wysoka na kilka ekranów,
wewnątrz `position: sticky` i tor przesuwany przez `animation-timeline`
związany z osią przewijania. Panele jadą z prawa na lewo, gdy użytkownik
przewija w dół. Zero JavaScriptu — cały ruch robi CSS.

Zapasy, bez których to by się rozpadło:
  - `@supports (animation-timeline: view())` — Safari i starsze Firefoksy
    nie znają tej własności i dostają zwykły pionowy ciąg kart,
  - `prefers-reduced-motion` — kto wyłączył ruch, dostaje to samo,
  - poniżej 1000 px pion, bo panel na cały ekran nie mieści się na telefonie.

Uruchomienie:  python tools/generuj-uslugi.py
"""

import html
import pathlib
import re

KATALOG = pathlib.Path(__file__).resolve().parent.parent

def bezp(tekst):
    """html.escape, ale nie psuje twardych spacji wpisanych w tresci.

    Bez tego „&nbsp;" wstawione przez tools/sierotki.py wychodzi z escape'a
    jako widoczne „&amp;nbsp;" — czytelnik widzi wtedy w zdaniu doslowny
    ciag znakow zamiast spacji. Zdarzylo sie to 2026-09-01 w opisach meta
    i pytaniach FAQ.
    """
    return html.escape(tekst).replace('&amp;nbsp;', '&nbsp;')


USLUGI = [
    dict(
        klucz="strona-firmowa",
        etykieta="01 / 04 · Najczęstszy wybór",
        tytul="Strona firmowa",
        lead="Wizytówka Twojego biznesu w&nbsp;sieci. Szybka, czytelna i&nbsp;przygotowana pod wyszukiwarkę — żeby klienci znajdowali Cię sami, a&nbsp;nie z&nbsp;polecenia.",
        akapity=[
            "Dla firmy usługowej to zwykle najrozsądniejszy wybór. Pokazuje, że istniejesz naprawdę, odpowiada na pytania, które klient i&nbsp;tak zadałby przez telefon, i&nbsp;daje Google coś, co można pozycjonować.",
            "W&nbsp;cenie dostajesz indywidualny projekt graficzny, wersję mobilną, formularz z&nbsp;zabezpieczeniem przed spamem, certyfikat SSL, zgodność z&nbsp;RODO oraz podpięte Analytics i&nbsp;Search Console — żeby od pierwszego dnia było widać, kto wchodzi i&nbsp;skąd.",
        ],
        punkty=["Do kilkunastu podstron", "Blog albo galeria realizacji",
                "2 000 – 5 000 zł netto", "Realizacja 3–5 tygodni"],
        obraz="life-centrum-thumb.webp",
        obrazAlt="Strona internetowa Life-Centrum — placówka medyczna w Raciborzu",
        obrazPodpis="Life-Centrum — placówka medyczna",
        obrazLink="/realizacje/strona-dla-przychodni/",
        cel="/tworzenie-stron-internetowych-raciborz/",
        celTekst="Zobacz, jak to robię",
    ),
    dict(
        klucz="pozycjonowanie",
        etykieta="02 / 04 · Praca ciągła",
        tytul="Pozycjonowanie (SEO)",
        lead="Strona bez odwiedzin to wizytówka schowana w&nbsp;szufladzie. Zajmuję się tym, żeby Google pokazywał Cię wtedy, gdy klient szuka dokładnie Twojej usługi.",
        akapity=[
            "Pozycjonowanie to trzy rzeczy robione porządnie: <strong>technika</strong>, <strong>treść</strong> i <strong>wiarygodność</strong>. Dla lokalnej firmy najkrótszą drogą do telefonów jest zwykle <strong>Profil Firmy w&nbsp;Google</strong> — to on decyduje, czy pojawiasz się w&nbsp;mapce nad wynikami, i&nbsp;od niego zaczynam.",
            "Bez obiecywania pierwszego miejsca i&nbsp;bez umowy na dwanaście miesięcy. Co miesiąc dostajesz raport z&nbsp;Search Console: na jakie frazy się wyświetlasz i&nbsp;co zostało zrobione. Realne efekty: po 4–6 miesiącach.",
        ],
        punkty=["Audyt od 900 zł", "Opieka od 800 zł miesięcznie",
                "Wypowiedzenie w&nbsp;miesiąc", "Raport co miesiąc"],
        obraz="czysto-po-thumb.webp",
        obrazAlt="Strona internetowa Czysto-Po — firma sprzątająca z Raciborza",
        obrazPodpis="Czysto-Po — treść pod długi ogon zapytań",
        obrazLink="/realizacje/strona-dla-firmy-sprzatajacej/",
        cel="/pozycjonowanie-stron-raciborz/",
        celTekst="Zobacz zakres i&nbsp;ceny",
    ),
    dict(
        klucz="efekt-wow",
        etykieta="03 / 04 · Gdy marka ma się wyróżniać",
        tytul="Strona z efektem „wow”",
        lead="Animacje, interaktywne elementy i&nbsp;design premium. Strona, po której klient mówi: „chcę tak samo”.",
        akapity=[
            "Ma sens tam, gdzie sam produkt jest wizualny albo marka celuje w&nbsp;górną półkę — salon, detailing, wnętrza, gastronomia. Tam pierwsze wrażenie robi za połowę argumentów sprzedażowych.",
            "Nie ma sensu tam, gdzie klient przychodzi z&nbsp;pilną potrzebą i&nbsp;chce numeru telefonu w&nbsp;piętnaście sekund. Powiem to na pierwszej rozmowie, jeśli tak wygląda Twoja sytuacja — również wtedy, gdy oznacza to tańsze zlecenie.",
        ],
        punkty=["Animowane wejście", "Efekty na przewijaniu",
                "Bez ciężkich bibliotek", "Wycena indywidualna"],
        obraz="alaska-thumb.webp",
        obrazAlt="Strona internetowa Alaska — klimatyzacja i chłodnictwo, Racibórz",
        obrazPodpis="Alaska — animowane wejście",
        obrazLink="/realizacje/strona-dla-firmy-klimatyzacyjnej/",
        cel="/portfolio.html",
        celTekst="Zobacz realizacje",
    ),
    dict(
        klucz="aplikacja",
        etykieta="04 / 04 · Gdy gotowe nie pasuje",
        tytul="Aplikacja webowa",
        lead="Narzędzie, a&nbsp;nie strona: panel klienta, system rezerwacji, wewnętrzna ewidencja, generator dokumentów.",
        akapity=[
            "Robię je wtedy, gdy gotowe programy nie pasują do sposobu, w&nbsp;jaki pracujesz — albo gdy abonament za nie zaczyna kosztować więcej niż napisanie własnego rozwiązania.",
            "Przykład z&nbsp;portfolio: generator faktur działający w&nbsp;przeglądarce bez zakładania konta, z&nbsp;trzema typami dokumentów i&nbsp;liczeniem zgodnym z&nbsp;przepisami. Albo panel, w&nbsp;którym właściciel firmy sam dodaje realizacje, bez dzwonienia do wykonawcy strony.",
        ],
        punkty=["Logowanie i&nbsp;role", "Baza danych i&nbsp;raporty",
                "Od 8 000 zł netto", "Realizacja od 8 tygodni"],
        obraz="wystawfakture-thumb.webp",
        obrazAlt="WystawFakture.eu — aplikacja do wystawiania faktur online",
        obrazPodpis="WystawFakture.eu — faktury bez rejestracji",
        obrazLink="/realizacje/aplikacja-do-wystawiania-faktur/",
        cel="/cennik/",
        celTekst="Sprawdź widełki cenowe",
    ),
]


def panel(u):
    akapity = '\n'.join(
        f'                                <p class="usluga-akapit">{a}</p>' for a in u["akapity"])
    punkty = '\n'.join(
        f'                                    <li>{bezp(p)}</li>' for p in u["punkty"])

    return f'''                    <article class="usluga-panel" id="usluga-{u["klucz"]}">
                        <div class="usluga-siatka">
                            <div class="usluga-tekst">
                                <p class="usluga-etykieta">{bezp(u["etykieta"])}</p>
                                <h3>{u["tytul"]}</h3>
                                <p class="usluga-lead">{u["lead"]}</p>
{akapity}
                                <ul class="usluga-punkty">
{punkty}
                                </ul>
                                <a href="{u["cel"]}" class="btn btn-primary usluga-cel">{bezp(u["celTekst"])} →</a>
                            </div>
                            <figure class="usluga-obraz">
                                <a href="{u["obrazLink"]}" aria-label="Zobacz, jak powstała strona {bezp(u["obrazPodpis"].split(" — ")[0])}">
                                    <img src="/{u["obraz"]}" width="800" height="450" loading="lazy" decoding="async"
                                        alt="{bezp(u["obrazAlt"])}">
                                </a>
                                <figcaption>{bezp(u["obrazPodpis"])}</figcaption>
                            </figure>
                        </div>
                    </article>'''


def sekcja():
    panele = '\n'.join(panel(u) for u in USLUGI)
    return f'''            <div class="uslugi-scena" id="uslugi-scena">
                <div class="uslugi-klej">
                    <div class="uslugi-tor">
{panele}
                    </div>
                </div>
            </div>
'''


def main():
    p = KATALOG / 'index.html'
    s = p.read_text(encoding='utf-8')

    wzor = re.compile(r'[ \t]*<div class="services-grid">.*?\n[ \t]*</div>\n(?=[ \t]*</div>\n[ \t]*</section>)', re.S)
    if not wzor.search(s):
        # Druga próba: sekcja już przebudowana. Kotwicą końcową jest zamknięcie
        # samej sceny — rozpoznawane po DOKŁADNYM wcięciu 12 spacji, bo takie ma
        # tylko ona (zagnieżdżone <div> siedzą głębiej). Wcześniej kotwicą była
        # podpowiedź „Przewijaj w dół”, ale zniknęła ze strony.
        #
        # Nie używać tu „.*?</div>” z lookaheadem na </section>: przy pierwszym
        # uruchomieniu po usunięciu podpowiedzi wzorzec przeskoczył zamknięcie
        # sekcji usług i zjadł całą sekcję portfolio (2026-09-01).
        #
        # Człon opcjonalny sprząta podpowiedź, jeśli jeszcze została w pliku.
        if 'uslugi-scena' in s:
            wzor = re.compile(
                r'[ \t]*<div class="uslugi-scena".*?\n {12}</div>\n'
                r'(?:[ \t]*<p class="uslugi-podpowiedz">.*?</p>\n)?',
                re.S)
        else:
            raise SystemExit('nie znaleziono siatki usług w&nbsp;index.html')

    s = wzor.sub(sekcja(), s, count=1)
    p.write_text(s, encoding='utf-8')
    print(f'index.html: galeria usług wstawiona ({len(USLUGI)} panele)')
    for u in USLUGI:
        # Encje zamieniamy na spacje PRZED liczeniem — inaczej „i&nbsp;treść”
        # liczy sie jako jeden wyraz i licznik zanizal wynik.
        slow = sum(len(re.sub(r'&[a-z]+;', ' ', re.sub(r'<[^>]+>', '', a)).split())
                   for a in u["akapity"])
        print(f'  {u["tytul"]:24} {slow:3} słów w akapitach')


if __name__ == '__main__':
    main()
