#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomiar realizacji przez API PageSpeed Insights — serwery Google.

DLACZEGO NIE LOKALNY LIGHTHOUSE: 2026-09-01 lokalny pomiar desktop dal 97
dla strony, ktorej PSI dawal 58 (szybki procesor tej maszyny maskuje TBT).
Publikowanie liczb, ktorych klient nie zobaczy po kliknieciu „sprawdz sam",
podwaza cala sekcje „Zmierzone, nie deklarowane". Stad pomiar z tego samego
zrodla, ktore otworzy klient.

API bez klucza ma bardzo maly limit (429 po kilku zadaniach z IP).
Z kluczem (darmowy, console.cloud.google.com -> PageSpeed Insights API):

    set PSI_KLUCZ=AIza...            # PowerShell: $env:PSI_KLUCZ='AIza...'
    python tools/zmierz-psi.py           # wszystkie strony, obie strategie
    python tools/zmierz-psi.py holaperros.pl   # jedna strona

Wynik wypisuje gotowy slownik do wklejenia w tools/pomiary.py.
"""
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

STRONY = {
    'hOla Perros':      'holaperros.pl',
    'Super Irek':       'superirek.pl',
    'Czysto-Po':        'czysto-po.pl',
    'Life-Ratownictwo': 'www.life-ratownictwo.pl',
    'WystawFakture.eu': 'wystawfakture.eu',
    '9 Dom':            '9dom.pl',
    'Karta Dnia':       'karta-dnia.pl',
    # Alaska: home.pl blokuje czesc ruchu, ale serwery Google zwykle wpuszcza
    'Alaska':           'alaskarp.pl',
}

KATEGORIE = ['performance', 'accessibility', 'best-practices', 'seo']
KONTEKST = ssl.create_default_context()


def zmierz(domena, strategia, klucz):
    q = {'url': f'https://{domena}/', 'strategy': strategia}
    zapytanie = urllib.parse.urlencode(q) + ''.join(f'&category={k}' for k in KATEGORIE)
    if klucz:
        zapytanie += f'&key={klucz}'
    u = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?{zapytanie}'
    d = json.loads(urllib.request.urlopen(u, timeout=240, context=KONTEKST).read())
    kat = d['lighthouseResult']['categories']
    return {k: round(kat[k]['score'] * 100) for k in KATEGORIE}


def main():
    klucz = os.environ.get('PSI_KLUCZ', '')
    tylko = sys.argv[1] if len(sys.argv) > 1 else None
    if not klucz:
        print('UWAGA: brak PSI_KLUCZ — limit bez klucza to kilka zadan,'
              ' potem 429.\n')

    wyniki = {}
    for klient, domena in STRONY.items():
        if tylko and tylko not in domena:
            continue
        wyniki[klient] = {}
        for strategia in ('mobile', 'desktop'):
            for proba in range(3):
                try:
                    w = zmierz(domena, strategia, klucz)
                    wyniki[klient][strategia] = w
                    print(f'  {klient:18} {strategia:8} '
                          + '  '.join(f'{k[:4]}:{v}' for k, v in w.items()))
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 429 and proba < 2:
                        czekaj = 70 * (proba + 1)
                        print(f'  {klient:18} {strategia:8} 429 — czekam {czekaj}s', flush=True)
                        time.sleep(czekaj)
                        continue
                    print(f'  {klient:18} {strategia:8} BLAD: {e}', flush=True)
                    wyniki[klient][strategia] = None
                    break
                except Exception as e:
                    print(f'  {klient:18} {strategia:8} BLAD: {e}', flush=True)
                    wyniki[klient][strategia] = None
                    break
            # odstep miedzy zadaniami — grzecznosc wobec limitu
            time.sleep(3)

    print('\n# --- do wklejenia w tools/pomiary.py (POMIARY) ---')
    for klient, w in wyniki.items():
        print(f'    "{klient}": {json.dumps(w, ensure_ascii=False)},')


if __name__ == '__main__':
    main()
