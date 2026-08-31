#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator poziomej galerii usług na stronie głównej.

Wzorzec przeniesiony z projektu „Mapa dłoni": scena wysoka na kilka ekranów,
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

USLUGI = [
    dict(
        klucz="strona-firmowa",
        etykieta="01 / 04 · Najczęstszy wybór",
        tytul="Strona firmowa",
        lead="Wizytówka Twojego biznesu w sieci. Szybka, czytelna i przygotowana pod wyszukiwarkę — żeby klienci znajdowali Cię sami, a nie z polecenia.",
        akapity=[
            "Dla firmy usługowej to zwykle najrozsądniejszy wybór. Pokazuje, że istniejesz naprawdę, odpowiada na pytania, które klient i tak zadałby przez telefon, i daje Google coś, co można pozycjonować.",
            "W cenie dostajesz indywidualny projekt graficzny, wersję mobilną, formularz z zabezpieczeniem przed spamem, certyfikat SSL, zgodność z RODO oraz podpięte Analytics i Search Console — żebyś od pierwszego dnia widział, kto wchodzi i skąd.",
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
        lead="Strona bez odwiedzin to wizytówka schowana w szufladzie. Zajmuję się tym, żeby Google pokazywał Cię wtedy, gdy klient szuka dokładnie Twojej usługi.",
        akapity=[
            "Pozycjonowanie to nie sztuczka ani „ustawianie się” z Google. To trzy rzeczy robione porządnie: <strong>technika</strong> — żeby strona ładowała się szybko i dała się poprawnie odczytać; <strong>treść</strong> — żeby odpowiadała na realne pytania klientów; oraz <strong>wiarygodność</strong> — czyli spójne dane firmy, opinie i Profil Firmy w Google.",
            "Dla firmy działającej lokalnie najkrótszą drogą do telefonów jest zwykle nie sama strona, lecz <strong>Profil Firmy w Google</strong>. To on decyduje o tym, czy pojawiasz się w mapce nad zwykłymi wynikami — a tam trafia lwia część kliknięć. Dlatego zwykle od niego zaczynam, mimo że mniej się na tym zarabia.",
            "Mówię wprost, czego nie robię: nie gwarantuję pierwszego miejsca, bo decyduje o nim Google, a nie wykonawca. Nie kupuję linków w systemach wymiany, bo to kończy się filtrem. Nie zamykam nikogo w umowie na dwanaście miesięcy. Co miesiąc dostajesz raport z Search Console: na jakie frazy się wyświetlasz, na której pozycji i co zostało zrobione.",
            "Realny termin: pierwsze zmiany po 2–3 miesiącach, efekty po 4–6. W Rybniku dłużej, w Głubczycach szybciej — konkurencja decyduje bardziej niż budżet.",
        ],
        punkty=["Audyt od 900 zł", "Opieka od 800 zł miesięcznie",
                "Wypowiedzenie w miesiąc", "Raport co miesiąc"],
        obraz="czysto-po-thumb.webp",
        obrazAlt="Strona internetowa Czysto-Po — firma sprzątająca z Raciborza",
        obrazPodpis="Czysto-Po — treść pod długi ogon zapytań",
        obrazLink="/realizacje/strona-dla-firmy-sprzatajacej/",
        cel="/pozycjonowanie-stron-raciborz/",
        celTekst="Zobacz zakres i ceny",
    ),
    dict(
        klucz="efekt-wow",
        etykieta="03 / 04 · Gdy marka ma wyróżniać",
        tytul="Strona z efektem „wow”",
        lead="Animacje, interaktywne elementy i design premium. Strona, po której klient mówi: „chcę tak samo”.",
        akapity=[
            "Ma sens tam, gdzie sam produkt jest wizualny albo marka celuje w górną półkę — salon, detailing, wnętrza, gastronomia. Tam pierwsze wrażenie robi za połowę argumentów sprzedażowych.",
            "Nie ma sensu tam, gdzie klient przychodzi z pilną potrzebą i chce numeru telefonu w piętnaście sekund. Powiem to na pierwszej rozmowie, jeśli tak wygląda Twoja sytuacja — również wtedy, gdy oznacza to tańsze zlecenie.",
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
        lead="Narzędzie, a nie strona: panel klienta, system rezerwacji, wewnętrzna ewidencja, generator dokumentów.",
        akapity=[
            "Robię je wtedy, gdy gotowe programy nie pasują do sposobu, w jaki pracujesz — albo gdy abonament za nie zaczyna kosztować więcej niż napisanie własnego rozwiązania.",
            "Przykład z portfolio: generator faktur działający w przeglądarce bez zakładania konta, z trzema typami dokumentów i liczeniem zgodnym z przepisami. Albo panel, w którym właściciel firmy sam dodaje realizacje, bez dzwonienia do wykonawcy strony.",
        ],
        punkty=["Logowanie i role", "Baza danych i raporty",
                "od 8 000 zł netto", "Realizacja od 8 tygodni"],
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
        f'                                    <li>{html.escape(p)}</li>' for p in u["punkty"])

    return f'''                    <article class="usluga-panel" id="usluga-{u["klucz"]}">
                        <div class="usluga-siatka">
                            <div class="usluga-tekst">
                                <p class="usluga-etykieta">{html.escape(u["etykieta"])}</p>
                                <h3>{u["tytul"]}</h3>
                                <p class="usluga-lead">{u["lead"]}</p>
{akapity}
                                <ul class="usluga-punkty">
{punkty}
                                </ul>
                                <a href="{u["cel"]}" class="btn btn-primary usluga-cel">{html.escape(u["celTekst"])} →</a>
                            </div>
                            <figure class="usluga-obraz">
                                <a href="{u["obrazLink"]}" aria-label="Zobacz, jak powstała strona {html.escape(u["obrazPodpis"].split(" — ")[0])}">
                                    <img src="/{u["obraz"]}" width="800" height="450" loading="lazy" decoding="async"
                                        alt="{html.escape(u["obrazAlt"])}">
                                </a>
                                <figcaption>{html.escape(u["obrazPodpis"])}</figcaption>
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
            <p class="uslugi-podpowiedz">Przewijaj w dół — panele przesuwają się w bok.</p>
'''


def main():
    p = KATALOG / 'index.html'
    s = p.read_text(encoding='utf-8')

    wzor = re.compile(r'[ \t]*<div class="services-grid">.*?\n[ \t]*</div>\n(?=[ \t]*</div>\n[ \t]*</section>)', re.S)
    if not wzor.search(s):
        # druga próba: sekcja już przebudowana
        if 'uslugi-scena' in s:
            wzor = re.compile(r'[ \t]*<div class="uslugi-scena".*?<p class="uslugi-podpowiedz">.*?</p>\n', re.S)
        else:
            raise SystemExit('nie znaleziono siatki usług w index.html')

    s = wzor.sub(sekcja(), s, count=1)
    p.write_text(s, encoding='utf-8')
    print(f'index.html: galeria usług wstawiona ({len(USLUGI)} panele)')
    for u in USLUGI:
        slow = sum(len(re.sub(r'<[^>]+>', '', a).split()) for a in u["akapity"])
        print(f'  {u["tytul"]:24} {slow:3} słów w akapitach')


if __name__ == '__main__':
    main()
