#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Urealnia daty <lastmod> w sitemap.xml — po dacie ostatniego commita pliku.

DLACZEGO TO NIE JEST KOSMETYKA: Google traktuje <lastmod> jako podpowiedź,
czy warto stronę odwiedzić ponownie. Data sprzed zmian mówi robotowi
„nic tu się nie dzieje" akurat wtedy, gdy treść realnie się zmieniła —
i świeże poprawki czekają na przeindeksowanie dłużej, niż musiały.

Data brana z gita, nie z czasu pliku na dysku: czas pliku zmienia każdy
przebieg generatora albo podbicie stempla ?v=, więc kłamałby w drugą
stronę i podawał wszystkie strony jako świeże przy każdym wdrożeniu.

    python tools/odswiez-mape.py           # pokazuje, co by zmienil
    python tools/odswiez-mape.py --zapisz
"""
import pathlib
import re
import subprocess
import sys

KATALOG = pathlib.Path(__file__).resolve().parent.parent
MAPA = KATALOG / 'sitemap.xml'
BAZA = 'https://webstudio47.pl'


def plik_dla_adresu(url):
    """Adres w mapie -> plik w repozytorium."""
    sciezka = url.replace(BAZA, '').lstrip('/')
    if sciezka == '':
        return KATALOG / 'index.html'
    if sciezka.endswith('/'):
        return KATALOG / sciezka / 'index.html'
    return KATALOG / sciezka


def data_z_gita(plik):
    try:
        wynik = subprocess.run(
            ['git', 'log', '-1', '--format=%cd', '--date=short', '--', str(plik)],
            cwd=KATALOG, capture_output=True, text=True, timeout=30)
        return (wynik.stdout or '').strip() or None
    except Exception:
        return None


def main():
    zapisz = '--zapisz' in sys.argv
    tekst = MAPA.read_text(encoding='utf-8')
    zmian = 0
    brakujace = []

    def podmien(m):
        nonlocal zmian
        url, stara = m.group(1), m.group(2)
        plik = plik_dla_adresu(url)
        if not plik.exists():
            brakujace.append(url)
            return m.group(0)
        nowa = data_z_gita(plik)
        if not nowa or nowa == stara:
            return m.group(0)
        zmian += 1
        print(f'  {stara} -> {nowa}   {url.replace(BAZA, "") or "/"}')
        return m.group(0).replace(f'<lastmod>{stara}</lastmod>',
                                  f'<lastmod>{nowa}</lastmod>')

    wz = re.compile(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', re.S)
    nowy = wz.sub(podmien, tekst)

    for url in brakujace:
        print(f'  UWAGA: brak pliku dla {url}')
    if zapisz and zmian:
        MAPA.write_text(nowy, encoding='utf-8')
    print(f'\nzaktualizowanych dat: {zmian}'
          + ('  — ZAPISANE' if zapisz and zmian else
             '  (podgląd; --zapisz zapisuje)' if zmian else ''))


if __name__ == '__main__':
    main()
