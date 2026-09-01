#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kontrola serwisu statycznego przed wdrożeniem.

Każda z tych kontroli powstała po tym, jak dany błąd realnie wszedł
na produkcję albo o włos tego uniknął. To nie jest lista życzeń —
to lista rzeczy, które już raz poszły źle.

Uruchomienie:
    python tools/sprawdz.py            # wszystko
    python tools/sprawdz.py --szybko   # bez kontroli podobieństwa treści

Kod wyjścia: 0 = czysto, 1 = są błędy.
"""

import argparse
import itertools
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

KATALOG = pathlib.Path(__file__).resolve().parent.parent

# Pola, których brak Google zgłasza jako błąd rich results
WYMAGANE_POLA = {
    'Article':             ['headline', 'author', 'datePublished'],
    'FAQPage':             ['mainEntity'],
    'HowTo':               ['name', 'step'],
    'Service':             ['name', 'provider'],
    'BreadcrumbList':      ['itemListElement'],
    'CreativeWork':        ['name'],
    'ProfessionalService': ['name', 'address', 'telephone'],
    'OfferCatalog':        ['name'],
    'ContactPage':         ['url'],
}

# Zasoby cache'owane długo — po zmianie MUSZĄ dostać nowy ?v=
ZASOBY_CACHE = ['style.css', 'page-style.css', 'script.js', 'consent.js',
                'page-script.js', 'arc.css', 'arc.js', 'blog/blog-style.css']

PUSTE_TAGI = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'path',
              'circle', 'rect', 'polyline', 'line', 'stop', 'use', 'area',
              'col', 'embed', 'track', 'wbr'}


class Struktura(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stos = []
        self.bledy = []

    def handle_starttag(self, tag, attrs):
        if tag not in PUSTE_TAGI:
            self.stos.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in PUSTE_TAGI:
            return
        if not self.stos:
            self.bledy.append(f'linia {self.getpos()[0]}: </{tag}> bez otwarcia')
        elif self.stos[-1][0] != tag:
            self.bledy.append(
                f'linia {self.getpos()[0]}: </{tag}> zamyka <{self.stos[-1][0]}> '
                f'z linii {self.stos[-1][1]}')
        else:
            self.stos.pop()

    def niezamkniete(self):
        return [t for t in self.stos if t[0] not in ('html', 'body', 'head')]


def strony():
    return sorted(p for p in KATALOG.rglob('*.html')
                  if '.git' not in p.parts and 'node_modules' not in p.parts)


def bez_tagow(src):
    src = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', src, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', src)


# ——— Kontrole ————————————————————————————————————————————————————————

def sprawdz_json_ld():
    """Dane strukturalne: poprawny JSON i wymagane pola."""
    bledy = []
    for p in strony():
        src = p.read_text(encoding='utf-8')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',
                             src, re.S):
            try:
                d = json.loads(m.group(1))
            except Exception as e:
                bledy.append(f'{p.relative_to(KATALOG)}: niepoprawny JSON-LD — {e}')
                continue

            typ = d.get('@type')
            for pole in WYMAGANE_POLA.get(typ, []):
                if pole not in d:
                    bledy.append(f'{p.relative_to(KATALOG)}: {typ} bez pola "{pole}"')

            if typ == 'FAQPage':
                for q in d.get('mainEntity', []):
                    if not q.get('acceptedAnswer', {}).get('text'):
                        bledy.append(f'{p.relative_to(KATALOG)}: FAQPage — pytanie '
                                     f'bez odpowiedzi: {q.get("name", "?")[:50]}')
            if typ == 'HowTo':
                for s in d.get('step', []):
                    if not (s.get('name') and s.get('text')):
                        bledy.append(f'{p.relative_to(KATALOG)}: HowTo — krok bez nazwy lub treści')
    return bledy


def sprawdz_faq_zgodnosc():
    """Pytania w FAQPage muszą być identyczne z widocznym <summary>.

    Google odrzuca rich result, gdy dane strukturalne mówią co innego
    niż treść strony."""
    bledy = []
    for p in strony():
        src = p.read_text(encoding='utf-8')
        faq = None
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
            try:
                d = json.loads(m.group(1))
            except Exception:
                continue
            if d.get('@type') == 'FAQPage':
                faq = [q['name'] for q in d.get('mainEntity', [])]
        if faq is None:
            continue

        import html as _h

        def porownywalne(t):
            """Tekst sprowadzony do postaci, w jakiej CZYTA go człowiek.

            Pytanie FAQ jest jednocześnie treścią do wyświetlenia i kluczem
            zestawianym z danymi strukturalnymi. Widoczny <summary> ma
            twarde spacje (typografia), a JSON-LD ma zwykłe — i słusznie,
            bo to dane dla Google, nie tekst do łamania. Bez zrównania obu
            stron kontrola zgłaszała rozjazd przy identycznej treści
            (2026-09-01, po przebiegu tools/sierotki.py).

            `\\s` w Pythonie obejmuje twardą spację, więc jedna zamiana
            załatwia też inne drobne różnice zapisu.
            """
            return re.sub(r'\s+', ' ', _h.unescape(t)).strip()

        faq = [porownywalne(q) for q in faq]
        widoczne = [porownywalne(re.sub(r'<[^>]+>', '', x))
                    for x in re.findall(r'<summary>(.*?)</summary>', src, re.S)]
        if faq != widoczne:
            bledy.append(f'{p.relative_to(KATALOG)}: FAQPage rozjeżdża się z widocznym '
                         f'tekstem ({len(faq)} w schemacie, {len(widoczne)} na stronie)')
    return bledy


def sprawdz_strukture():
    """Niezamknięte i źle zagnieżdżone znaczniki."""
    bledy = []
    for p in strony():
        k = Struktura()
        k.feed(p.read_text(encoding='utf-8'))
        for b in k.bledy:
            bledy.append(f'{p.relative_to(KATALOG)}: {b}')
        for t, linia in k.niezamkniete():
            bledy.append(f'{p.relative_to(KATALOG)}: niezamknięty <{t}> z linii {linia}')
    return bledy


def sprawdz_linki():
    """Odnośniki wewnętrzne prowadzące donikąd."""
    bledy = []
    for p in strony():
        src = p.read_text(encoding='utf-8')
        for m in re.finditer(r'(?:href|src)="([^"]+)"', src):
            u = m.group(1)
            if u.startswith(('http', 'mailto:', 'tel:', '#', 'data:', 'javascript:')):
                continue
            czysty = u.split('?')[0].split('#')[0]
            if not czysty:
                continue
            cel = (KATALOG / czysty.lstrip('/')) if czysty.startswith('/') \
                else (p.parent / czysty)
            cel = cel.resolve()
            if cel.is_dir():
                cel = cel / 'index.html'
            if not cel.exists():
                bledy.append(f'{p.relative_to(KATALOG)} → {u}')
    return bledy


def sprawdz_stemple():
    """Zasób zmieniony po ostatnim podbiciu ?v= = powracający dostaną
    starą wersję z rocznego cache."""
    bledy = []
    wzorce = {}
    for p in strony():
        src = p.read_text(encoding='utf-8')
        for zasob in ZASOBY_CACHE:
            nazwa = zasob.split('/')[-1]
            m = re.search(r'(?<![-\w])' + re.escape(nazwa) + r'\?v=(\d+)', src)
            if m:
                wzorce.setdefault(zasob, set()).add(int(m.group(1)))

    for zasob, stemple in wzorce.items():
        plik = KATALOG / zasob
        if not plik.exists():
            bledy.append(f'{zasob}: linkowany, ale nie istnieje')
            continue
        if len(stemple) > 1:
            bledy.append(f'{zasob}: rozjechane stemple w różnych plikach: '
                         f'{sorted(stemple)}')
        najnowszy = max(stemple)
        if plik.stat().st_mtime > najnowszy + 300:
            bledy.append(f'{zasob}: zmieniony po podbiciu ?v={najnowszy} — '
                         f'podbij stempel we wszystkich plikach HTML')
    return bledy


def sprawdz_podobienstwo(prog=70):
    """Strony lokalne różniące się wyłącznie nazwą miasta to dla Google
    strony-wycieraczki (doorway pages) — czyli spam."""
    bledy = []
    grupy = {}
    for p in strony():
        nazwa = p.parent.name if p.name == 'index.html' else p.stem
        klucz = re.sub(r'-[a-ząćęłńóśźż-]+$', '', nazwa)
        if klucz and klucz != nazwa:
            grupy.setdefault(klucz, []).append(p)

    for klucz, lista in grupy.items():
        if len(lista) < 2:
            continue
        slowa = {p: set(re.findall(r'\w{4,}', bez_tagow(
            p.read_text(encoding='utf-8')).lower())) for p in lista}
        for a, b in itertools.combinations(lista, 2):
            A, B = slowa[a], slowa[b]
            if not (A | B):
                continue
            proc = len(A & B) / len(A | B) * 100
            if proc >= prog:
                bledy.append(f'{a.parent.name} vs {b.parent.name}: {proc:.0f}% '
                             f'wspólnych słów (próg {prog}%) — ryzyko doorway page')
    return bledy


def sprawdz_meta():
    """Tytuł i opis: obecność oraz długość mieszcząca się w wynikach Google."""
    bledy = []
    tytuly = {}
    for p in strony():
        src = p.read_text(encoding='utf-8')
        rel = p.relative_to(KATALOG)

        t = re.search(r'<title>(.*?)</title>', src, re.S)
        if not t:
            bledy.append(f'{rel}: brak <title>')
        else:
            tekst = t.group(1).strip()
            tytuly.setdefault(tekst, []).append(str(rel))
            if len(tekst) > 65:
                bledy.append(f'{rel}: <title> ma {len(tekst)} znaków (Google ucina ok. 60)')

        # re.S i \s* — atrybuty bywają łamane na dwie linie przez formatery.
        # Bez tego kontrola zgłaszała „brak opisu” na stronach, które go mają.
        d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', src, re.S)
        if not d:
            bledy.append(f'{rel}: brak meta description')
        elif len(d.group(1)) > 165:
            bledy.append(f'{rel}: opis ma {len(d.group(1))} znaków (Google ucina ok. 155)')

        if not re.search(r'rel="canonical"', src):
            bledy.append(f'{rel}: brak canonical')

    for tekst, gdzie in tytuly.items():
        if len(gdzie) > 1:
            bledy.append(f'zduplikowany <title> "{tekst[:45]}…" w: {", ".join(gdzie)}')
    return bledy


KONTROLE = [
    ('dane strukturalne',       sprawdz_json_ld,      False),
    ('zgodność FAQ ze stroną',  sprawdz_faq_zgodnosc, False),
    ('struktura HTML',          sprawdz_strukture,    False),
    ('linki wewnętrzne',        sprawdz_linki,        False),
    ('stemple cache ?v=',       sprawdz_stemple,      False),
    ('meta i canonical',        sprawdz_meta,         False),
    ('podobieństwo treści',     sprawdz_podobienstwo, True),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--szybko', action='store_true',
                    help='pomiń kontrolę podobieństwa treści (najwolniejsza)')
    args = ap.parse_args()

    print(f'Sprawdzam {len(strony())} plików HTML w {KATALOG.name}/\n')
    razem = 0

    for nazwa, funkcja, wolna in KONTROLE:
        if wolna and args.szybko:
            print(f'  {nazwa:26} pominięte (--szybko)')
            continue
        bledy = funkcja()
        razem += len(bledy)
        znak = 'OK' if not bledy else f'{len(bledy)} do poprawy'
        print(f'  {nazwa:26} {znak}')
        for b in bledy[:12]:
            print(f'      {b}')
        if len(bledy) > 12:
            print(f'      … i {len(bledy) - 12} więcej')

    print()
    if razem:
        print(f'RAZEM {razem} rzeczy do poprawy — NIE wdrażaj, zanim ich nie naprawisz.')
        return 1
    print('Czysto. Można wdrażać.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
