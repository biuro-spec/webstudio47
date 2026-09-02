# -*- coding: utf-8 -*-
"""Dopisuje adres Profilu Firmy w Google do sameAs we WSZYSTKICH danych
strukturalnych serwisu: 3 generatory + 5 stron pisanych recznie.

Uzycie:
    python tools/dodaj-profil-google.py "https://maps.app.goo.gl/XXXX"          # wpisuje
    python tools/dodaj-profil-google.py "https://maps.app.goo.gl/XXXX" --proba  # tylko pokazuje

Idempotentny: drugi przebieg z tym samym adresem nic nie zmienia.
Po wpisaniu trzeba odpalic generatory (skrypt robi to sam) i sprawdz.py.
"""
import pathlib
import re
import subprocess
import sys

KATALOG = pathlib.Path(__file__).resolve().parent.parent
FB = "https://www.facebook.com/profile.php?id=61578430357755"

GENERATORY = ["generuj-sprawdzarke.py", "generuj-realizacje.py", "generuj-miasta.py"]
RECZNE = [
    "index.html",
    "kontakt/index.html",
    "cennik/index.html",
    "tworzenie-stron-internetowych-raciborz/index.html",
    "pozycjonowanie-stron-raciborz/index.html",
]


def popraw_generator(p, url, proba):
    s = p.read_text(encoding="utf-8")
    if "PROFIL_GOOGLE" in s:
        return "juz ma"
    s2 = s.replace(f'FB = "{FB}"\n', f'FB = "{FB}"\nPROFIL_GOOGLE = "{url}"\n', 1)
    s2 = s2.replace('"sameAs": [FB],', '"sameAs": [FB, PROFIL_GOOGLE],', 1)
    if s2.count("PROFIL_GOOGLE") != 2:
        return "BLAD: nie znaleziono obu kotwic"
    if not proba:
        p.write_text(s2, encoding="utf-8", newline="\n")
    return "dopisano"


def popraw_html(p, url, proba):
    s = p.read_text(encoding="utf-8")
    if url in s:
        return "juz ma"
    # wariant jednoliniowy: "sameAs": ["...fb..."],
    jedno = f'"sameAs": ["{FB}"]'
    if jedno in s:
        s2 = s.replace(jedno, f'"sameAs": ["{FB}", "{url}"]', 1)
    else:
        # wariant wieloliniowy (index.html): linia z FB w bloku sameAs
        m = re.search(r'("sameAs": \[\n)([ \t]*)"' + re.escape(FB) + r'"\n', s)
        if not m:
            return "BLAD: nie znaleziono bloku sameAs"
        wciecie = m.group(2)
        s2 = s[:m.end()].rstrip("\n") + f',\n{wciecie}"{url}"\n' + s[m.end():]
    if not proba:
        p.write_text(s2, encoding="utf-8", newline="\n")
    return "dopisano"


def main():
    if len(sys.argv) < 2 or not sys.argv[1].startswith("https://"):
        print(__doc__)
        sys.exit(1)
    url = sys.argv[1].strip()
    proba = "--proba" in sys.argv
    print("PROBA — nic nie zapisuje" if proba else "ZAPIS")
    for g in GENERATORY:
        print(f"  {g:45} {popraw_generator(KATALOG / 'tools' / g, url, proba)}")
    for h in RECZNE:
        print(f"  {h:45} {popraw_html(KATALOG / h, url, proba)}")
    if proba:
        return
    print("-- generatory --")
    for g in GENERATORY:
        r = subprocess.run([sys.executable, str(KATALOG / "tools" / g)], cwd=KATALOG,
                           capture_output=True, text=True, encoding="utf-8")
        print(f"  {g}: kod {r.returncode}" + ("" if r.returncode == 0 else "\n" + r.stderr[-800:]))
    print("-- kontrola: wszystkie sameAs z profilem? --")
    brak = [str(f.relative_to(KATALOG)) for f in KATALOG.rglob("*.html")
            if "sameAs" in f.read_text(encoding="utf-8") and url not in f.read_text(encoding="utf-8")
            and "node_modules" not in str(f)]
    print("  brakuje w:", brak if brak else "nigdzie — komplet")


if __name__ == "__main__":
    main()
