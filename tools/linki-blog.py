# -*- coding: utf-8 -*-
"""Dopisuje na koncu kazdego wpisu blogowego blok „Przeczytaj tez" z dwoma
linkami do pokrewnych wpisow.

PO CO: 2026-09-05 Google zglosil trzy strony jako „wykryta, obecnie
niezindeksowana", w tym dwa wpisy blogowe. Technicznie byly bez zarzutu
(200, bez noindex, canonical na siebie), ale kazdy wpis mial tylko DWA linki
wewnetrzne: z listy /blog/ i z karuzeli na stronie glownej. Ten blok podnosi
to do czterech, z czterech roznych stron, i daje czytelnikowi nastepny krok.

Pary sa dobrane tematycznie (nie losowo i nie „wszystkie do wszystkich"),
bo link ma cos znaczyc dla czytajacego, a nie tylko dla robota.

Skrypt jest idempotentny: drugi przebieg nic nie zmienia.
"""
import pathlib
import re

KATALOG = pathlib.Path(__file__).resolve().parent.parent
BLOG = KATALOG / 'blog'

TYTULY = {
    'dlaczego-firma-potrzebuje-strony.html': 'Dlaczego Twoja firma potrzebuje strony internetowej?',
    'ile-kosztuje-strona-internetowa.html': 'Ile kosztuje strona internetowa w 2026?',
    'jak-pozycjonowac-strone-seo.html': 'Jak pozycjonować stronę internetową? Poradnik SEO',
    'responsywna-strona-internetowa.html': 'Responsywna strona internetowa — dlaczego to konieczność?',
    'strona-wizytowkowa-vs-sklep.html': 'Strona wizytówkowa vs. sklep online — co wybrać?',
    'wordpress-vs-strona-na-zamowienie.html': 'WordPress vs. strona na zamówienie — co wybrać?',
}

# wpis -> (dwa pokrewne wpisy, w kolejnosci naturalnego nastepnego kroku)
POKREWNE = {
    'dlaczego-firma-potrzebuje-strony.html': [
        'ile-kosztuje-strona-internetowa.html',
        'strona-wizytowkowa-vs-sklep.html',
    ],
    'ile-kosztuje-strona-internetowa.html': [
        'wordpress-vs-strona-na-zamowienie.html',
        'strona-wizytowkowa-vs-sklep.html',
    ],
    'jak-pozycjonowac-strone-seo.html': [
        'responsywna-strona-internetowa.html',
        'dlaczego-firma-potrzebuje-strony.html',
    ],
    'responsywna-strona-internetowa.html': [
        'jak-pozycjonowac-strone-seo.html',
        'wordpress-vs-strona-na-zamowienie.html',
    ],
    'strona-wizytowkowa-vs-sklep.html': [
        'ile-kosztuje-strona-internetowa.html',
        'dlaczego-firma-potrzebuje-strony.html',
    ],
    'wordpress-vs-strona-na-zamowienie.html': [
        'ile-kosztuje-strona-internetowa.html',
        'jak-pozycjonowac-strone-seo.html',
    ],
}

KOTWICA = '                <div class="blog-cta-box">'


def blok(nazwa):
    linki = '\n'.join(
        f'                        <li><a href="{cel}">{TYTULY[cel]}</a></li>'
        for cel in POKREWNE[nazwa]
    )
    return (
        '                <aside class="blog-pokrewne" aria-labelledby="pokrewne-naglowek">\n'
        '                    <h2 id="pokrewne-naglowek">Przeczytaj też</h2>\n'
        '                    <ul>\n'
        f'{linki}\n'
        '                    </ul>\n'
        '                </aside>\n'
    )


def main():
    zmienione = 0
    for nazwa in sorted(POKREWNE):
        p = BLOG / nazwa
        s = p.read_text(encoding='utf-8')
        if 'blog-pokrewne' in s:
            print(f'  {nazwa:46} juz ma')
            continue
        if s.count(KOTWICA) != 1:
            print(f'  {nazwa:46} BLAD: kotwica wystepuje {s.count(KOTWICA)} razy')
            continue
        p.write_text(s.replace(KOTWICA, blok(nazwa) + KOTWICA, 1), encoding='utf-8', newline='\n')
        zmienione += 1
        print(f'  {nazwa:46} dopisano ({len(POKREWNE[nazwa])} linki)')
    print(f'zmienionych plikow: {zmienione}')


if __name__ == '__main__':
    main()
