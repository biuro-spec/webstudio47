#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leczenie sierotek — jednoliterowych wyrazów na końcu wiersza.

Polska typografia nie pozwala kończyć wiersza na „a i o u w z". Angielski
nie ma jednoliterowych przyimków, więc ŻADEN domyślny mechanizm łamania
tekstu tego nie pilnuje — `text-wrap: pretty` dba o ostatnią linię akapitu,
nie o pojedyncze litery w środku. Lekarstwo: twarda spacja w treści.

DLACZEGO NIE ZWYKŁY REGEX PO PLIKU: trafiłby w atrybuty (`class="w-full"`),
w adresy, w JSON-LD i — w generatorach — w kod (`.map((k, i) => ...)`
zamieniłoby się w `i => ...` i skrypt przestałby działać). Dlatego:

  * HTML — podmieniamy WYŁĄCZNIE tekst między znacznikami, z pominięciem
    <script>, <style> i <title> (tytuł trafia do wyników Google i nie ma
    tam czego łamać),
  * Python — chodzimy po drzewie składniowym i ruszamy wyłącznie literały
    tekstowe, po ich dokładnych pozycjach w źródle.

Generatory poprawiamy RAZEM ze stronami: inaczej najbliższe uruchomienie
`generuj-*.py` cofnęłoby pracę na 16 z 27 stron.

    python tools/sierotki.py            # pokazuje, co by zmienił
    python tools/sierotki.py --napraw   # zapisuje
"""
import ast
import glob
import pathlib
import re
import sys

# Litera osamotniona na końcu wiersza. Dopuszczamy znak przestankowy przed
# nią, bo „— a potem" też jest sierotką. Po literze musi stać zwykła spacja
# i początek następnego wyrazu.
SIEROTKA = re.compile(
    r'(^|[\s(„”"—–\-])([aiouwzAIOUWZ])[ \t]+(?=[\w„ąćęłńóśżźĄĆĘŁŃÓŚŻŹ])'
)

BLOKI_HTML = re.compile(r'<(script|style|title)\b[^>]*>.*?</\1>', re.S | re.I)
TEKST_HTML = re.compile(r'(>)([^<>]+)(<)')


def wylecz(tekst, znacznik='&nbsp;'):
    """Wstawia twardą spację po każdej osamotnionej literze."""
    return SIEROTKA.sub(lambda m: m.group(1) + m.group(2) + znacznik, tekst)


def przerob_html(zrodlo):
    """Podmienia tylko tekst widoczny; zwraca (nowe_zrodlo, ile_zmian)."""
    # Bloki, których nie wolno ruszać, chowamy na czas przebiegu pod
    # znacznikami zastępczymi — prościej i pewniej niż omijanie ich regexem.
    schowek = []

    def schowaj(m):
        schowek.append(m.group(0))
        return f'\x00{len(schowek) - 1}\x00'

    tekst = BLOKI_HTML.sub(schowaj, zrodlo)

    licznik = [0]

    def podmien(m):
        przed = m.group(2)
        po = wylecz(przed)
        if po != przed:
            licznik[0] += przed.count(' ') - po.count(' ')
        return m.group(1) + po + m.group(3)

    tekst = TEKST_HTML.sub(podmien, tekst)
    tekst = re.sub(r'\x00(\d+)\x00', lambda m: schowek[int(m.group(1))], tekst)
    return tekst, licznik[0]


def przerob_python(zrodlo):
    """Podmienia tylko literały tekstowe, po pozycjach z drzewa składni."""
    drzewo = ast.parse(zrodlo)
    linie = zrodlo.split('\n')
    zmiany = []          # (linia, kol_od, kol_do, nowy_tekst)
    licznik = 0

    for wezel in ast.walk(drzewo):
        if not (isinstance(wezel, ast.Constant) and isinstance(wezel.value, str)):
            continue
        # Literały wielolinijkowe i f-stringi zostawiamy: przy f-stringu
        # pozycje obejmują też wyrażenia w klamrach, a przy wielolinijkowym
        # nie da się bezpiecznie podmienić fragmentu jednej linii.
        if wezel.lineno != wezel.end_lineno:
            continue
        linia = linie[wezel.lineno - 1]
        fragment = linia[wezel.col_offset:wezel.end_col_offset]
        # Pomijamy f-stringi (pozycje bywają mylące) i wszystko, co wygląda
        # na ścieżkę, adres, klasę CSS albo nazwę pliku — tam spacja twarda
        # nie ma czego szukać.
        if re.match(r'^[rbf]', fragment) or '{' in fragment:
            continue
        nowy = wylecz(fragment, znacznik='&nbsp;')
        if nowy != fragment:
            zmiany.append((wezel.lineno - 1, wezel.col_offset,
                           wezel.end_col_offset, nowy))
            licznik += 1

    # Od końca, żeby wcześniejsze podmiany nie przesuwały kolejnych pozycji.
    for nr, od, do, nowy in sorted(zmiany, reverse=True):
        linie[nr] = linie[nr][:od] + nowy + linie[nr][do:]
    return '\n'.join(linie), licznik


def main():
    napraw = '--napraw' in sys.argv
    pliki = [f for f in sorted(glob.glob('**/*.html', recursive=True))
             if '.git' not in f]
    pliki += sorted(glob.glob('tools/generuj-*.py')) + ['tools/pomiary.py']

    razem = 0
    for f in pliki:
        p = pathlib.Path(f)
        if not p.exists():
            continue
        zrodlo = p.read_text(encoding='utf-8')
        if f.endswith('.py'):
            nowe, ile = przerob_python(zrodlo)
            # Bezpiecznik: skrypt, który po zabiegu przestaje się parsować,
            # nie ma prawa trafić na dysk.
            if ile:
                ast.parse(nowe)
        else:
            nowe, ile = przerob_html(zrodlo)
        if ile:
            razem += ile
            print(f'  {ile:4}  {f}')
            if napraw:
                p.write_text(nowe, encoding='utf-8')

    print(f'\nsierotek: {razem}' + ('  — ZAPISANE' if napraw
                                    else '  (podgląd; --napraw zapisuje)'))


if __name__ == '__main__':
    main()
