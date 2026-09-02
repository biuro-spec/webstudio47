#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wydziela CSS potrzebny nad zagięciem i wbudowuje go w <head> stron.

PO CO: arkusz waży 101 KB i blokuje renderowanie. Zmierzone trzykrotnie
2026-09-01/02: tuż po wdrożeniu, gdy brzeg CDN nie ma jeszcze pliku,
FCP na komórce rośnie z 0,9 s do 3,5 s, a wynik spada z 95 do 76.
To nie jest wyłącznie artefakt pomiaru — odwiedzający trafiający na zimny
węzeł naprawdę tyle czeka na pierwsze malowanie.

JAK: reguły pasujące do elementów widocznych nad zagięciem lądują wprost
w <head>, a pełny arkusz dociąga się bez blokowania renderowania.

CZEGO NIE WOLNO POMINĄĆ, choć nie wynika z samych selektorów:
  * @font-face — fonty są preloadowane, ale bez tych reguł przeglądarka
    nie wie, do czego preloadowany plik przypisać, i czeka na arkusz;
  * :root ze zmiennymi — bez nich krytyczne reguły nie mają skąd wziąć kolorów;
  * @keyframes używane przez animacje wejścia hero;
  * reset (*, html, body).

    python tools/krytyczny-css.py            # pokazuje rozmiar, nic nie zapisuje
    python tools/krytyczny-css.py --zapisz
"""
import glob
import pathlib
import re
import sys

KATALOG = pathlib.Path(__file__).resolve().parent.parent

# Selektory zebrane z realnie widocznych elementów nad zagięciem
# (pomiar w przeglądarce przy 390x844, strona główna).
NAD_ZAGIECIEM = {
    'html', 'body', 'main', 'header', 'nav', 'section', 'div', 'span', 'a',
    'ul', 'li', 'p', 'h1', 'h2', 'h3', 'button', 'svg', 'path', 'polyline',
    '#main-header', '#home', '#hero-canvas', '#mobile-menu',
    '#floating-phone-btn', '#scroll-top-btn',
    '.container', '.nav-container', '.nav-links', '.nav-spacer', '.logo',
    '.menu-toggle', '.font-special', '.active',
    '.hero', '.hero-bg', '.hero-content', '.hero-btns',
    '.btn', '.btn-primary', '.btn-outline', '.btn-sm',
    '.text-gradient', '.text-gradient-alt', '.text-white', '.shimmer',
    '.reveal', '.reveal-hero', '.delay-1', '.delay-2', '.delay-3',
    '.scroll-indicator', '.mouse', '.glass',
    '.floating-phone-btn', '.scroll-top-btn',
}

# Reguły trzymane zawsze, niezależnie od selektorów.
ZAWSZE = re.compile(r'^\s*(@font-face|:root|\*|::selection|@media\s*\(prefers-reduced-motion)')


def rozbij(css):
    """Dzieli arkusz na reguły najwyższego poziomu, zachowując bloki @."""
    reguly, glebokosc, start = [], 0, 0
    i = 0
    while i < len(css):
        z = css[i]
        if z == '{':
            glebokosc += 1
        elif z == '}':
            glebokosc -= 1
            if glebokosc == 0:
                reguly.append(css[start:i + 1])
                start = i + 1
        i += 1
    if start < len(css):
        reszta = css[start:].strip()
        if reszta:
            reguly.append(reszta)
    return reguly


def krytyczna(regula):
    """Czy ta reguła jest potrzebna do pierwszego malowania."""
    if ZAWSZE.match(regula):
        return True
    naglowek = regula.split('{', 1)[0]

    # blok @media / @supports — sprawdzamy jego zawartość rekurencyjnie
    if naglowek.strip().startswith('@'):
        if naglowek.strip().startswith('@keyframes'):
            return None  # rozstrzygane osobno, po nazwach animacji
        wnetrze = regula[regula.find('{') + 1:regula.rfind('}')]
        return any(krytyczna(r) for r in rozbij(wnetrze))

    for sel in naglowek.split(','):
        sel = sel.strip()
        if not sel:
            continue
        # tokeny: znaczniki, klasy, identyfikatory
        tokeny = re.findall(r'[#.]?[a-zA-Z][\w-]*', sel)
        tokeny = [t for t in tokeny
                  if t.startswith(('.', '#')) or t.islower()]
        if tokeny and all(t in NAD_ZAGIECIEM for t in tokeny):
            return True
    return False


def main():
    zapisz = '--zapisz' in sys.argv
    css = (KATALOG / 'style.css').read_text(encoding='utf-8')
    reguly = rozbij(css)

    wybrane = [r for r in reguly if krytyczna(r) is True]

    # klatki animacji uzywanych przez wybrane reguly
    uzywane = set()
    for r in wybrane:
        for m in re.finditer(r'animation(?:-name)?\s*:\s*([^;}]+)', r):
            for slowo in re.findall(r'[a-zA-Z][\w-]*', m.group(1)):
                uzywane.add(slowo)
    for r in reguly:
        m = re.match(r'\s*@keyframes\s+([\w-]+)', r)
        if m and m.group(1) in uzywane:
            wybrane.append(r)

    krytyczny = ''.join(wybrane)
    print(f'  regul w arkuszu:   {len(reguly)}')
    print(f'  wybranych:         {len(wybrane)}')
    print(f'  rozmiar krytyczny: {len(krytyczny) / 1024:.1f} KB'
          f'  (z {len(css) / 1024:.0f} KB, czyli {len(krytyczny) / len(css):.0%})')

    if not zapisz:
        print('\n(podgląd; --zapisz wbudowuje w strony)')
        return

    (KATALOG / 'krytyczny.css').write_text(krytyczny, encoding='utf-8')
    import os
    os.chdir(KATALOG)
    n = wbuduj(krytyczny)
    print()
    print('  krytyczny.css zapisany, wbudowany w ' + str(n) + ' plikow')


# ——— Wbudowanie w strony ————————————————————————————————————————————

# Odwolania do arkusza maja trzy postacie: "style.css" (strona glowna),
# "/style.css" (podstrony) i "../style.css" (blog), a w generatorach zamiast
# numeru stoi {stempel}. Zamiast regexa z gaszczem ucieczek szukamy wprost
# poczatku znacznika i doczytujemy do jego konca.
POCZATEK = '<link rel="stylesheet" href="'


def znajdz_link(tresc):
    """Zwraca (caly_znacznik, wciecie, adres) albo None."""
    i = tresc.find(POCZATEK)
    while i != -1:
        koniec = tresc.find('">', i)
        if koniec == -1:
            return None
        adres = tresc[i + len(POCZATEK):koniec]
        if adres.endswith('.css') or 'style.css?' in adres:
            wiersz = tresc.rfind(chr(10), 0, i) + 1
            wciecie = tresc[wiersz:i]
            if wciecie.strip() == '':
                return tresc[i:koniec + 2], wciecie, adres
        i = tresc.find(POCZATEK, i + 1)
    return None


def wbuduj(krytyczny):
    """Zastepuje blokujacy <link> wbudowanym CSS-em plus arkuszem bez blokowania."""
    zmienione = 0
    cele = ([f for f in glob.glob('**/*.html', recursive=True) if '.git' not in f]
            + glob.glob('tools/generuj-*.py'))
    for sciezka in cele:
        pl = pathlib.Path(sciezka)
        tresc = pl.read_text(encoding='utf-8')
        if 'id="krytyczny"' in tresc:
            continue
        trafienie = znajdz_link(tresc)
        if not trafienie:
            continue
        caly, wciecie, adres = trafienie
        nl = chr(10)
        nowe = (
            wciecie + '<!-- CSS krytyczny wbudowany: usuwa jeden lot do serwera' + nl
            + wciecie + '     ze sciezki pierwszego malowania. Reszta arkusza dociaga sie' + nl
            + wciecie + '     bez blokowania renderowania. Sklada to tools/krytyczny-css.py' + nl
            + wciecie + '     — nie edytuj tego bloku recznie. -->' + nl
            + wciecie + '<style id="krytyczny">' + krytyczny + '</style>' + nl
            + wciecie + '<link rel="preload" href="' + adres + '" as="style"'
            + ' onload="this.onload=null;this.rel=' + chr(39) + 'stylesheet' + chr(39) + '">' + nl
            + wciecie + '<noscript><link rel="stylesheet" href="' + adres + '"></noscript>'
        )
        pl.write_text(tresc.replace(caly, nowe, 1), encoding='utf-8')
        zmienione += 1
    return zmienione


if __name__ == '__main__':
    main()
