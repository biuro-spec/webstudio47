# WebStudio47 — notatki dla agenta

Strona firmowa WebStudio47 (Racibórz): pozyskuje klientów na tworzenie stron
i pozycjonowanie. Właściciel: Mariusz. Kontakt na stronie: 602 622 840,
kontakt@webstudio47.pl.

---

## Stack i struktura

**Statyczny HTML/CSS/JS. Nie ma builda, nie ma npm, nie ma frameworka.**
Źródłem jest katalog repo — to, co tu leży, to jest to, co idzie na serwer.

```
index.html          strona główna
portfolio.html      realizacje (5 sztuk)
cennik/             widełki cenowe + FAQ
kontakt/            formularz (Apps Script)
pozycjonowanie-stron-raciborz/     strona ofertowa SEO
tworzenie-stron-internetowych-raciborz/   strona ofertowa WWW
blog/               7 artykułów + blog-style.css
style.css           główne style (ZMINIFIKOWANE, jedna linia)
style.dev.css       nieskompresowane źródło stylów — NIE jest linkowane
page-style.css      style podstron ofertowych (czytelne)
script.js           nawigacja, reveal, słownik pojęć
consent.js          zgoda na cookies + Consent Mode v2 (wstrzykuje modal)
page-script.js      formularz kontaktowy
deploy.ps1          wysyłka na CyberFolks przez FTP
apps-script/        backend formularza — NIE trafia na serwer
```

Konwencje: wcięcia 4 spacje, style pisane ręcznie (żadnego Tailwinda),
teksty po polsku z twardymi spacjami `&nbsp;` przed krótkimi wyrazami.

Tokeny w `:root`: `--bg-primary #0a0a0f`, `--accent-purple #8b5cf6`,
`--accent-cyan #06b6d4`. Fonty: Inter (tekst) + Space Grotesk (nagłówki).

---

## Pułapki — przeczytaj, zanim cokolwiek zmienisz

**1. Cache na ROK.** `.htaccess` ustawia CSS i JS na `access plus 1 year`.
Po zmianie `style.css`, `page-style.css`, `script.js`, `consent.js`,
`page-script.js` albo `blog/blog-style.css` **musisz podbić `?v=`
we wszystkich plikach HTML**, inaczej powracający dostaną starą wersję.
`deploy.ps1` o tym ostrzega, ale nie poprawia za Ciebie.

**2. Wdrożenie wymaga wyraźnego polecenia użytkownika.** Skrypt czyta hasło
z zapisanej sesji FileZilli, więc classifier blokuje go, gdy agent sięga
po niego z własnej inicjatywy — także w trybie `-Lista`. Ale gdy użytkownik
powie wprost „wdróż", blokada znika i agent wykonuje wysyłkę sam.
Nie trzeba żadnej reguły w `settings.json`. Nie proponuj jej dodawania:
agent i tak nie może sam poszerzać swoich uprawnień, a próba edycji
`settings.local.json` łatwo kończy się popsutym JSON-em, który po cichu
wyłącza wszystkie ustawienia z tego pliku.

**3. `style.css` jest zminifikowany.** Edycja regexem działa, ale ostrożnie.
`style.dev.css` to nieużywane źródło — zmiana w nim niczego nie robi.
Przy zmianach w obu trzymaj je zgodne albo świadomie zignoruj `.dev`.

**4. Ceny występują w dwóch miejscach.** `cennik/index.html` i artykuł
`blog/ile-kosztuje-strona-internetowa.html` muszą się zgadzać.
Aktualne: landing 1 500–3 500, strona firmowa 2 000–5 000,
sklep 5 000–15 000, aplikacja od 8 000, audyt SEO od 900,
opieka SEO od 800/mies., Profil Firmy od 600. Wszystko netto.
Stawki SEO są propozycją agenta — nie zostały potwierdzone przez właściciela.

**5. Dane strukturalne FAQ muszą być zgodne co do znaku z widocznym tekstem.**
Google tego wymaga. Przy zmianie pytania w `<summary>` popraw też JSON-LD.

**6. Sprawdzaj linki zewnętrzne przed pisaniem o realizacjach.** Trzy z siedmiu
były martwe (dwie wygasłe domeny, jedna literówka: `alaska-rp.pl` zamiast
`alaskarp.pl`). Strona obiecuje „kliknij i zobacz na żywo" — martwy link
podważa całą jej wiarygodność.

---

## Skille — co się przydaje w tym projekcie

### Używaj domyślnie

| Skill | Kiedy |
|---|---|
| **polski-w-kodzie** | przy KAŻDYM polskim tekście — odmiana, trzy formy mnogiej, cudzysłowy „…" |
| **prog-wejscia** | teksty ofertowe czyta właściciel firmy, nie programista; tłumacz pojęcia w miejscu użycia |
| **agent-browser** | weryfikacja zmian: `a11y`, `vitals`, zrzuty, testy formularza. Bez tego nie twierdź, że coś działa |

### Do pracy nad treścią i widocznością

| Skill | Kiedy |
|---|---|
| **seo-audit** | audyt techniczny, diagnoza „dlaczego nie rankuję" |
| **schema-markup** | dane strukturalne — serwis ma Service, OfferCatalog, FAQPage, BreadcrumbList, ContactPage |
| **ai-seo** | optymalizacja pod cytowanie w ChatGPT/Perplexity/AI Overviews — realny kanał dla lokalnej firmy usługowej |
| **content-strategy** | planowanie kolejnych artykułów; ostatnia baza fraz jest w GSC |
| **content-production** | pisanie artykułu od zera |
| **pricing-page** | dalsza praca nad `/cennik/` |
| **landing-page** | struktura i copy stron ofertowych (uwaga: sama strategia, nie generator) |

### Do jakości wykonania

| Skill | Kiedy |
|---|---|
| **perfekcja-strony** | doszlifowanie JEDNEJ podstrony metodą audyt → pomiar → naprawa → weryfikacja |
| **better-accessibility** | cały serwis ma dziś 0 naruszeń axe — trzymaj ten stan |
| **better-writing** | mikrocopy: przyciski, komunikaty błędów, stany puste |
| **better-typography**, **better-colors**, **better-layout**, **better-ui** | dopracowanie wizualne w ramach istniejących tokenów |
| **optimize-web-animations** | strona ma marquee, shimmer i `gradientPulse` w pętli — jeśli kiedyś zamuli, zacznij tutaj |
| **interface-review** | przegląd zmian przed wysyłką |

### NIE używaj — zły stack albo zły cel

| Skill | Dlaczego |
|---|---|
| **landing-page-generator** | generuje komponenty Next.js/React w TSX z Tailwindem. Ten serwis to czysty HTML — wstawienie tego rozwali projekt |
| **vercel-react-best-practices** | nie ma tu Reacta ani Next.js |
| **premium-business-website**, **service-business-website**, **alaskamodern-website-generator** | generatory NOWYCH stron od zera; ten serwis już istnieje i ma własny system wizualny |
| **build-awwwards-quality-sites**, **cinematic-scroll-storytelling**, **gsap-scrolltrigger-storytelling** | dokładają GSAP, Lenis, Three.js. Strona ma dziś zero zewnętrznych bibliotek JS i to jest jej atut — sprzedaje szybkość |
| **animate-expo**, **write-swift**, **ask-sonner**, **document-skills:\*** | inne platformy, nie dotyczy |

**Zasada nadrzędna:** ten serwis nie ma ani jednej zewnętrznej biblioteki
JavaScript. Nie dokładaj żadnej bez wyraźnej prośby — „strony pisane od zera,
bez kilkunastu wtyczek" to dosłownie treść oferty na stronie głównej.

---

## Wdrażanie

```powershell
powershell -ExecutionPolicy Bypass -File deploy.ps1 -Lista     # podgląd, bez łączenia
powershell -ExecutionPolicy Bypass -File deploy.ps1            # wysyłka
powershell -ExecutionPolicy Bypass -File deploy.ps1 -Sprzataj  # usuń sieroty (pyta o TAK)
```

FTP na CyberFolks, `ntroixgelh@s75.cyber-folks.pl`, katalog
`/domains/webstudio47.pl/public_html`. Hasło pobierane w locie z zapisanej
sesji FileZilli — w repo nie ma żadnych sekretów.

Wysyłka jest **nieniszcząca**: jawna lista plików przez `put`, nigdy
`synchronize`. Nie kasuje niczego, co wgrano ręcznie.

---

## Stan i punkty odniesienia

**Baza Search Console (3 mies. do 2026-08-30, przed pierwszymi zmianami):**
633 wyświetlenia, 4 kliknięcia, CTR 0,6%, średnia pozycja 42,8.
Zapytania: „tworzenie/projektowanie stron … racibórz" (~248 wyśw.)
oraz „pozycjonowanie / agencja SEO racibórz" (~179 wyśw.).

Do tej bazy porównuj efekty. Realny termin oceny: 2–3 miesiące.

**Zrobione (sierpień 2026):** 4 strony ofertowe, formularz na Apps Script,
Google Consent Mode v2 na wszystkich 13 podstronach, GA4 dodany do bloga,
portfolio oczyszczone z martwych linków, 0 naruszeń axe w całym serwisie.

**Zaplanowane, niezrobione:** case studies per realizacja (5 sztuk siedzi
na jednym URL-u `portfolio.html`), strony lokalne (Wodzisław, Rybnik,
Kędzierzyn, Głubczyce), opinie klientów, konwersja hero blogowych
z PNG 500–770 KB na WebP.
