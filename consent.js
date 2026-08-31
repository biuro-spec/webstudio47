/* ==========================================================================
   consent.js — zgoda na cookies + Google Consent Mode v2

   Wczesniej modal zgody istnial TYLKO na stronie glownej, a jego wybor
   ladowal do localStorage i nie robil nic wiecej: GA4 startowal i tak,
   a "Odrzuc wszystkie" niczego nie odrzucalo. Na pozostalych podstronach
   nie bylo nawet modala.

   Teraz:
   - stan domyslny (denied) ustawia inline'owy skrypt w <head>, PRZED gtag.js
     — inaczej GA4 zdazylby wystartowac, zanim ten plik sie wczyta;
   - ten plik wstrzykuje modal na KAZDEJ podstronie i tlumaczy wybor
     uzytkownika na gtag('consent', 'update', ...).

   Reklam nie prowadzimy, wiec ad_* pozostaje 'denied' zawsze.
   ========================================================================== */

(function () {
    'use strict';

    var KLUCZ = 'cookieConsent';

    var MARKUP = `<button class="cookie-trigger" id="cookie-trigger" aria-label="Ustawienia cookies">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
stroke-linejoin="round">
<circle cx="12" cy="12" r="10" />
<circle cx="8" cy="9" r="1.2" fill="currentColor" stroke="none" />
<circle cx="14" cy="7" r="1" fill="currentColor" stroke="none" />
<circle cx="16" cy="13" r="1.3" fill="currentColor" stroke="none" />
<circle cx="10" cy="15" r="1.1" fill="currentColor" stroke="none" />
<circle cx="6" cy="13" r="0.8" fill="currentColor" stroke="none" />
<circle cx="13" cy="11" r="0.9" fill="currentColor" stroke="none" />
<path d="M15.5 4.5 C17 6, 18 8, 17.5 10" opacity="0.4" />
</svg>
</button>
<div class="cookie-overlay" id="cookie-overlay"></div>
<div class="cookie-modal" id="cookie-modal" role="dialog" aria-modal="true" aria-labelledby="cookie-tytul">
<div class="cookie-view" id="cookie-main-view">
<div class="cookie-modal-header">
<div class="cookie-modal-icon">
<svg viewBox="0 0 24 24" fill="none" stroke="url(#cookie-grad)" stroke-width="1.5">
<defs>
<linearGradient id="cookie-grad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#7c3aed" />
<stop offset="100%" stop-color="#06b6d4" />
</linearGradient>
</defs>
<circle cx="12" cy="12" r="10" />
<circle cx="8" cy="9" r="1.2" fill="#7c3aed" stroke="none" />
<circle cx="14" cy="7" r="1" fill="#06b6d4" stroke="none" />
<circle cx="16" cy="13" r="1.3" fill="#7c3aed" stroke="none" />
<circle cx="10" cy="15" r="1.1" fill="#06b6d4" stroke="none" />
</svg>
</div>
<h3 id="cookie-tytul">Ty kontrolujesz swoje dane</h3>
<button class="cookie-close" id="cookie-close" aria-label="Zamknij">&times;</button>
</div>
<div class="cookie-modal-body">
<p class="cookie-desc">Używamy plików cookie, aby zapewnić prawidłowe działanie strony i&nbsp;jej ciągłe
ulepszanie. Możesz dostosować swoje preferencje&nbsp;poniżej.</p>
<div class="cookie-category">
<div class="cookie-cat-header">
<div>
<h4>Niezbędne</h4>
<p>Zapewniają podstawowe funkcje strony, takie jak nawigacja i&nbsp;bezpieczeństwo. Nie
można ich wyłączyć.</p>
</div>
<span class="cookie-always-on">Zawsze aktywne</span>
</div>
</div>
<div class="cookie-category">
<div class="cookie-cat-header">
<div>
<h4>Funkcjonalne</h4>
<p>Ułatwiają zapisywanie informacji, która zmienia wygląd lub działanie witryny. Na przykład
wybrany język lub preferencje&nbsp;interfejsu.</p>
</div>
<label class="cookie-switch">
<input type="checkbox" id="cookie-functional" checked aria-label="Funkcjonalne">
<span class="cookie-slider"></span>
</label>
</div>
</div>
<div class="cookie-category">
<div class="cookie-cat-header">
<div>
<h4>Statystyka</h4>
<p>Pomagają zrozumieć interakcje odwiedzających z&nbsp;witryną w&nbsp;celu ciągłego
ulepszania usług.</p>
</div>
<label class="cookie-switch">
<input type="checkbox" id="cookie-analytics" checked aria-label="Statystyka">
<span class="cookie-slider"></span>
</label>
</div>
</div>
</div>
<div class="cookie-modal-footer">
<button class="cookie-btn cookie-btn-save" id="cookie-save">Zapisz ustawienia</button>
<button class="cookie-btn cookie-btn-reject" id="cookie-reject">Odrzuć wszystkie</button>
<button class="cookie-btn cookie-btn-accept" id="cookie-accept-all">Akceptuj wszystkie</button>
</div>
<div class="cookie-privacy-link">
<button id="cookie-show-privacy">Polityka prywatności</button>
</div>
</div>
<div class="cookie-view cookie-privacy-view" id="cookie-privacy-view">
<div class="cookie-modal-header">
<button class="cookie-back" id="cookie-back" aria-label="Wróć">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
<path d="M19 12H5M12 19l-7-7 7-7" />
</svg>
</button>
<h3>Polityka prywatności</h3>
<button class="cookie-close" id="cookie-close-privacy" aria-label="Zamknij">&times;</button>
</div>
<div class="cookie-modal-body cookie-privacy-body">
<h4>1. Administrator danych</h4>
<p>Administratorem Twoich danych osobowych jest WebStudio47, Racibórz. Kontakt: <a
href="mailto:kontakt@webstudio47.pl">kontakt@webstudio47.pl</a></p>
<h4>2. Cele przetwarzania danych</h4>
<p>Dane przetwarzamy w celu: świadczenia usług drogą elektroniczną, zapewnienia prawidłowego działania
strony, analizy statystycznej ruchu na&nbsp;stronie oraz kontaktu w&nbsp;odpowiedzi na&nbsp;Twoje
zapytania.</p>
<h4>3. Podstawa prawna</h4>
<p>Przetwarzanie odbywa się na&nbsp;podstawie art. 6 ust. 1 lit. a, b i&nbsp;f RODO — Twojej zgody,
realizacji umowy oraz prawnie uzasadnionego interesu administratora.</p>
<h4>4. Twoje prawa</h4>
<p>Masz prawo do: dostępu do swoich danych, ich sprostowania, usunięcia, ograniczenia przetwarzania,
przenoszenia danych oraz wniesienia sprzeciwu. Możesz także cofnąć zgodę w&nbsp;dowolnym momencie.
</p>
<h4>5. Pliki cookies</h4>
<p>Strona wykorzystuje pliki cookies niezbędne do jej prawidłowego funkcjonowania. Pliki funkcjonalne
i&nbsp;analityczne wymagają Twojej zgody, którą możesz cofnąć w&nbsp;każdej chwili klikając ikonę
ciasteczka w&nbsp;lewym dolnym rogu.</p>
<h4>6. Kontakt</h4>
<p>W sprawach związanych z ochroną danych osobowych prosimy o kontakt: <strong>tel. 602 622 840</strong>
lub e-mail: <a href="mailto:kontakt@webstudio47.pl">kontakt@webstudio47.pl</a></p>
</div>
</div>
</div>`;

    /* --- Odczyt i zapis wyboru --------------------------------------------- */

    function odczytajWybor() {
        try {
            return JSON.parse(localStorage.getItem(KLUCZ) || 'null');
        } catch (e) {
            return null;
        }
    }

    function zapiszWybor(prefs) {
        try {
            localStorage.setItem(KLUCZ, JSON.stringify(prefs));
        } catch (e) {
            /* tryb prywatny albo zablokowane dane witryn — trudno, zgoda
               obowiazuje wtedy tylko do konca sesji */
        }
    }

    /* --- Przekazanie zgody do Google --------------------------------------- */

    function zastosujZgode(prefs) {
        if (typeof gtag !== 'function') return;

        gtag('consent', 'update', {
            analytics_storage: prefs.analytics ? 'granted' : 'denied',
            functionality_storage: prefs.functional ? 'granted' : 'denied',
            personalization_storage: prefs.functional ? 'granted' : 'denied',
            ad_storage: 'denied',
            ad_user_data: 'denied',
            ad_personalization: 'denied'
        });
    }

    /* --- Modal -------------------------------------------------------------- */

    // <aside> zamiast golego <div>: bez punktu orientacyjnego czytniki
    // ekranu zglaszaja te tresc jako lezaca poza struktura strony.
    // Wszystkie trzy elementy sa position:fixed, wiec uklad sie nie zmienia.
    var kontener = document.createElement('aside');
    kontener.setAttribute('aria-label', 'Ustawienia prywatnosci');
    kontener.innerHTML = MARKUP;
    document.body.appendChild(kontener);

    var trigger = document.getElementById('cookie-trigger');
    var overlay = document.getElementById('cookie-overlay');
    var modal = document.getElementById('cookie-modal');
    var widokGlowny = document.getElementById('cookie-main-view');
    var widokPolityki = document.getElementById('cookie-privacy-view');
    var polFunkcjonalne = document.getElementById('cookie-functional');
    var polStatystyka = document.getElementById('cookie-analytics');

    if (!modal || !overlay) return;

    var ostatnioAktywny = null;

    function otworz() {
        ostatnioAktywny = document.activeElement;
        overlay.classList.add('active');
        modal.classList.add('active');
        widokGlowny.classList.remove('cookie-main-view-hidden');
        widokPolityki.classList.remove('active');

        var pierwszy = modal.querySelector('button, input');
        if (pierwszy) pierwszy.focus();
    }

    function zamknij() {
        overlay.classList.remove('active');
        modal.classList.remove('active');
        if (ostatnioAktywny && ostatnioAktywny.focus) ostatnioAktywny.focus();
    }

    function zapiszIZamknij(wybor) {
        var prefs = {
            choice: wybor,
            functional: wybor === 'all' ? true : (wybor === 'none' ? false : !!(polFunkcjonalne && polFunkcjonalne.checked)),
            analytics: wybor === 'all' ? true : (wybor === 'none' ? false : !!(polStatystyka && polStatystyka.checked)),
            timestamp: Date.now()
        };

        zapiszWybor(prefs);
        zastosujZgode(prefs);
        zamknij();
    }

    /* --- Podpiecie zdarzen -------------------------------------------------- */

    var zapisany = odczytajWybor();

    // Przelaczniki maja pokazywac to, co uzytkownik wybral poprzednio.
    if (zapisany) {
        if (polFunkcjonalne) polFunkcjonalne.checked = !!zapisany.functional;
        if (polStatystyka) polStatystyka.checked = !!zapisany.analytics;
    } else {
        // Pierwsza wizyta — pytamy. Do czasu odpowiedzi obowiazuje 'denied'
        // ustawione w <head>, wiec GA4 nic nie zapisuje.
        setTimeout(otworz, 1500);
    }

    trigger.addEventListener('click', otworz);
    overlay.addEventListener('click', zamknij);
    document.getElementById('cookie-close').addEventListener('click', zamknij);

    var zamknijPolityke = document.getElementById('cookie-close-privacy');
    if (zamknijPolityke) zamknijPolityke.addEventListener('click', zamknij);

    document.getElementById('cookie-accept-all').addEventListener('click', function () { zapiszIZamknij('all'); });
    document.getElementById('cookie-reject').addEventListener('click', function () { zapiszIZamknij('none'); });
    document.getElementById('cookie-save').addEventListener('click', function () { zapiszIZamknij('custom'); });

    document.getElementById('cookie-show-privacy').addEventListener('click', function () {
        widokGlowny.classList.add('cookie-main-view-hidden');
        widokPolityki.classList.add('active');
    });

    document.getElementById('cookie-back').addEventListener('click', function () {
        widokPolityki.classList.remove('active');
        widokGlowny.classList.remove('cookie-main-view-hidden');
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) zamknij();
    });
})();
