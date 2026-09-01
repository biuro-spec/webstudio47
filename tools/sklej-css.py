#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dokleja page-style.css na koniec style.css (po edycji page-style uruchom ponownie).

Od 2026-09-01 strony linkuja JEDEN arkusz: style.css. Powod: dwa blokujace
arkusze to dwa loty do serwera w sciezce krytycznej, a TTFB hostingu potrafi
wynosic 600+ ms na zadanie. page-style.css pozostaje ZRODLEM swojej czesci —
edytuj go normalnie i uruchom ten skrypt, a potem podbij ?v= w HTML-ach.
"""
import pathlib, re
K = pathlib.Path(__file__).resolve().parent.parent
ZNACZNIK = '/* ==== page-style.css, wklejone'
style = (K / 'style.css').read_text(encoding='utf-8')
page = (K / 'page-style.css').read_text(encoding='utf-8')
i = style.find(ZNACZNIK)
rdzen = style[:i].rstrip('\n') if i != -1 else style.rstrip('\n')
naglowek = ('\n/* ==== page-style.css, wklejone przez tools/sklej-css.py. '
            'Edytuj page-style.css i uruchom skrypt ponownie; nie edytuj tej sekcji. ==== */\n')
(K / 'style.css').write_text(rdzen + naglowek + page, encoding='utf-8')
print(f'style.css = rdzen ({len(rdzen)/1024:.0f} KB) + page-style ({len(page)/1024:.0f} KB)')
