# -*- coding: utf-8 -*-
"""Dwie poprawki tresci pod frazy z Search Console (28 dni do 2026-09-09).

DLACZEGO (odczyt kolumny „Pozycja" w GSC, 2026-09-11):
  tworzenie stron internetowych racibórz      poz. 12,0
  tworzenie sklepów internetowych racibórz    poz. 13,2
  projektowanie stron internetowych racibórz  poz. 13,9   <- o krok od 1. strony
  agencja seo racibórz                         poz. 56,7   (45 wyswietlen)

1. Strona tworzenia: slowo „projektowanie" wystepowalo WYLACZNIE w stopce,
   mimo ze Google juz stawia strone na 14. miejscu pod te fraze. Krok
   procesu „Projekt" nazywa sie teraz „Projektowanie" i jego opis mowi to
   wprost. Ta sama zmiana w danych HowTo, jesli krok tam jest.

2. Strona pozycjonowania: 45 osob szukalo „agencja seo racibórz", a strona
   nie odpowiadala na to wprost. Nowe pytanie w FAQ, zbudowane wylacznie
   z tego, co juz stoi na stronie (jedna osoba, SEO techniczne/lokalne/
   Profil Firmy, ograniczona liczba zlecen) — zero nowych obietnic.
   Pytanie trafia do HTML i do FAQPage w JSON-LD w tym samym miejscu,
   bo tools/sprawdz.py pilnuje zgodnosci obu.

Idempotentny: drugi przebieg nic nie zmienia.
"""
import pathlib

KAT = pathlib.Path(__file__).resolve().parent.parent

# --- 1. projektowanie ---------------------------------------------------------
T = KAT / 'tworzenie-stron-internetowych-raciborz' / 'index.html'

STARY_KROK = '''                        <h3>Projekt</h3>
                        <p>Pokazuję układ i&nbsp;kierunek graficzny, zanim cokolwiek zakoduję. Poprawki na tym etapie
                            są darmowe i&nbsp;natychmiastowe — później kosztują czas.</p>'''
NOWY_KROK = '''                        <h3>Projektowanie</h3>
                        <p>Projektowanie strony zaczynam od układu i&nbsp;kierunku graficznego — pokazuję je, zanim
                            cokolwiek zakoduję. Poprawki na tym etapie są darmowe i&nbsp;natychmiastowe — później
                            kosztują czas.</p>'''

# --- 2. agencja SEO -----------------------------------------------------------
P = KAT / 'pozycjonowanie-stron-raciborz' / 'index.html'

KOTWICA_HTML = '''                    <details class="faq-item glass">
                        <summary>Ile kosztuje pozycjonowanie?</summary>'''
NOWE_HTML = '''                    <details class="faq-item glass">
                        <summary>Czy jesteś agencją SEO?</summary>
                        <div class="faq-answer">
                            <p>Nie. Jestem jedną osobą i&nbsp;pozycjonowaniem zajmuję się sam, więc rozmawiasz
                                bezpośrednio z&nbsp;tym, kto robi audyt i&nbsp;poprawia Twoją stronę. Bez opiekuna
                                klienta i&nbsp;bez „przekażę zespołowi”.</p>
                            <p>Zakres jest ten sam, co w&nbsp;agencji SEO w&nbsp;Raciborzu: SEO techniczne, lokalne
                                i&nbsp;Profil Firmy w&nbsp;Google. Różnica jest w&nbsp;skali — biorę ograniczoną liczbę
                                zleceń, więc każde dostaje pełną uwagę.</p>
                        </div>
                    </details>
'''

KOTWICA_LD = '''        {
          "@type": "Question",
          "name": "Ile kosztuje pozycjonowanie?",'''
NOWE_LD = '''        {
          "@type": "Question",
          "name": "Czy jesteś agencją SEO?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Nie. Jestem jedną osobą i pozycjonowaniem zajmuję się sam, więc rozmawiasz bezpośrednio z tym, kto robi audyt i poprawia Twoją stronę. Bez opiekuna klienta i bez „przekażę zespołowi”. Zakres jest ten sam, co w agencji SEO w Raciborzu: SEO techniczne, lokalne i Profil Firmy w Google. Różnica jest w skali — biorę ograniczoną liczbę zleceń, więc każde dostaje pełną uwagę."
          }
        },
'''


def podmien(sciezka, stare, nowe, opis):
    s = sciezka.read_text(encoding='utf-8')
    if nowe.strip() in s:
        print(f'  {opis:48} juz jest')
        return s, False
    n = s.count(stare)
    if n != 1:
        raise SystemExit(f'  {opis}: kotwica wystepuje {n} razy — przerywam, nic nie zapisano')
    return s.replace(stare, nowe, 1), True


def main():
    # 1. krok procesu
    s, zm1 = podmien(T, STARY_KROK, NOWY_KROK, 'tworzenie: krok Projekt -> Projektowanie')
    # ten sam krok w danych HowTo (jesli jest), zeby dane nie rozjechaly sie z trescia
    if '"name": "Projekt"' in s:
        s = s.replace('"name": "Projekt"', '"name": "Projektowanie"', 1)
        stary_ld = 'Pokazuję układ i kierunek graficzny, zanim cokolwiek zakoduję.'
        if stary_ld in s:
            s = s.replace(stary_ld, 'Projektowanie strony zaczynam od układu i kierunku graficznego — pokazuję je, zanim cokolwiek zakoduję.', 1)
        print('  tworzenie: HowTo krok zaktualizowany')
        zm1 = True
    if zm1:
        T.write_text(s, encoding='utf-8', newline='\n')
        print('  tworzenie: zapisano')

    # 2. FAQ: HTML i JSON-LD razem, albo wcale
    s = P.read_text(encoding='utf-8')
    if 'Czy jesteś agencją SEO?' in s:
        print('  pozycjonowanie: pytanie o agencje juz jest')
        return
    if s.count(KOTWICA_HTML) != 1 or s.count(KOTWICA_LD) != 1:
        raise SystemExit('  pozycjonowanie: kotwica HTML albo JSON-LD niejednoznaczna — nic nie zapisano')
    s = s.replace(KOTWICA_HTML, NOWE_HTML + KOTWICA_HTML, 1)
    s = s.replace(KOTWICA_LD, NOWE_LD + KOTWICA_LD, 1)
    P.write_text(s, encoding='utf-8', newline='\n')
    print('  pozycjonowanie: pytanie o agencje dodane (HTML + FAQPage)')


if __name__ == '__main__':
    main()
