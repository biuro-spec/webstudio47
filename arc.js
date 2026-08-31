/* ==========================================================================
   arc.js — galeria realizacji na łuku 3D

   Ustawia karty na okręgu i obraca nim. Zero bibliotek, zero zależności.

   Progresywne ulepszenie: bez tego pliku portfolio zostaje zwykłą siatką
   kart i wszystko dziala. Klasa `arc-on` na <html> wlacza tryb luku dopiero
   wtedy, gdy przegladarka i uzytkownik to uniosa.
   ========================================================================== */

(function () {
    'use strict';

    var arc = document.querySelector('[data-arc]');
    if (!arc) return;

    var karty = Array.prototype.slice.call(arc.querySelectorAll('.arc-card'));
    if (karty.length < 2) return;

    // Szanujemy ustawienie systemowe. Nie sprawdzamy tego raz na starcie -
    // uzytkownik moze je zmienic w trakcie.
    var mniejRuchu = window.matchMedia('(prefers-reduced-motion: reduce)');
    var szeroki = window.matchMedia('(min-width: 901px)');

    // Bez transformacji 3D nie ma o czym mowic
    if (!CSS.supports('transform-style', 'preserve-3d')) return;

    document.documentElement.classList.add('arc-on');

    /* --- Geometria luku -------------------------------------------------- */

    var PROMIEN = 680;   // px - jak bardzo karty uciekaja w glab
    var ROZSTAW = 33;    // stopni miedzy sasiednimi kartami

    var pozycja = 0;     // biezaca pozycja w "kartach" (moze byc ulamkowa)
    var cel = 0;         // dokad zmierzamy
    var animacja = null;

    function ustawKarty() {
        for (var i = 0; i < karty.length; i++) {
            var odchylka = i - pozycja;
            var kat = odchylka * ROZSTAW;
            var rad = kat * Math.PI / 180;

            // Karta na okregu: srodkowa ladzie na z=0, boczne uciekaja w glab
            var x = Math.sin(rad) * PROMIEN;
            var z = Math.cos(rad) * PROMIEN - PROMIEN;

            var k = karty[i];
            k.style.setProperty('--x', x.toFixed(1) + 'px');
            k.style.setProperty('--z', z.toFixed(1) + 'px');
            k.style.setProperty('--kat', (-kat).toFixed(2) + 'deg');

            // Im dalej od srodka, tym ciemniej
            var dystans = Math.abs(odchylka);
            k.style.setProperty('--cien', Math.min(dystans * 0.22, 0.72).toFixed(2));

            // Karty schowane za innymi nie lapia klikniec ani fokusa
            var poza = dystans > 2.6;
            k.setAttribute('aria-hidden', poza ? 'true' : 'false');
            var link = k.querySelector('a');
            if (link) link.tabIndex = poza ? -1 : 0;

            // Bliższe karty rysowane na wierzchu
            k.style.zIndex = String(1000 - Math.round(dystans * 10));
        }

        odswiezSterowanie();
    }

    /* --- Plynne dojscie do celu ------------------------------------------ */

    function animuj() {
        var roznica = cel - pozycja;

        if (Math.abs(roznica) < 0.0008) {
            pozycja = cel;
            ustawKarty();
            animacja = null;
            return;
        }

        pozycja += roznica * 0.12;   // wygladzanie
        ustawKarty();
        animacja = requestAnimationFrame(animuj);
    }

    function doCelu(nowy) {
        cel = Math.max(0, Math.min(karty.length - 1, nowy));
        if (!animacja) animacja = requestAnimationFrame(animuj);
    }

    function skoczDo(indeks) {
        doCelu(indeks);
    }

    /* --- Sterowanie ------------------------------------------------------ */

    var btnPrev = document.querySelector('[data-arc-prev]');
    var btnNext = document.querySelector('[data-arc-next]');
    var licznik = document.querySelector('[data-arc-licznik]');

    function odswiezSterowanie() {
        var biezaca = Math.round(pozycja);
        if (btnPrev) btnPrev.disabled = cel <= 0.01;
        if (btnNext) btnNext.disabled = cel >= karty.length - 1.01;
        if (licznik) licznik.textContent = (biezaca + 1) + ' / ' + karty.length;
    }

    if (btnPrev) btnPrev.addEventListener('click', function () { doCelu(Math.round(cel) - 1); });
    if (btnNext) btnNext.addEventListener('click', function () { doCelu(Math.round(cel) + 1); });

    // Strzalki dzialaja, gdy fokus jest gdziekolwiek w galerii
    arc.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') { e.preventDefault(); doCelu(Math.round(cel) - 1); }
        if (e.key === 'ArrowRight') { e.preventDefault(); doCelu(Math.round(cel) + 1); }
    });

    // Tab na ukrytej karcie ma ja przywolac, a nie zostawic fokus w pustce
    karty.forEach(function (k, i) {
        k.addEventListener('focusin', function () {
            if (Math.abs(i - cel) > 0.5) doCelu(i);
        });
    });

    /* --- Przeciaganie ---------------------------------------------------- */

    var ciagnie = false, startX = 0, startPoz = 0, ruszyl = false;

    arc.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return;
        ciagnie = true;
        ruszyl = false;
        startX = e.clientX;
        startPoz = cel;
        arc.setPointerCapture(e.pointerId);
        arc.classList.add('is-dragging');
    });

    arc.addEventListener('pointermove', function (e) {
        if (!ciagnie) return;
        var dx = e.clientX - startX;
        if (Math.abs(dx) > 4) ruszyl = true;
        // 320 px przeciagniecia = jedna karta
        cel = Math.max(0, Math.min(karty.length - 1, startPoz - dx / 320));
        if (!animacja) animacja = requestAnimationFrame(animuj);
    });

    function koniecCiagniecia() {
        if (!ciagnie) return;
        ciagnie = false;
        arc.classList.remove('is-dragging');
        doCelu(Math.round(cel));   // dociagniecie do najblizszej karty
    }

    arc.addEventListener('pointerup', koniecCiagniecia);
    arc.addEventListener('pointercancel', koniecCiagniecia);

    // Klikniecie po przeciagnieciu nie powinno otwierac realizacji
    arc.addEventListener('click', function (e) {
        if (ruszyl) { e.preventDefault(); ruszyl = false; }
    }, true);

    /* --- Kolko myszy ------------------------------------------------------ */

    var kolkoTimer = null;

    arc.addEventListener('wheel', function (e) {
        // Poziome kolko i gest touchpada obracaja luk. Pionowe zostawiamy
        // stronie - inaczej odbieramy uzytkownikowi przewijanie strony.
        if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
        e.preventDefault();
        cel = Math.max(0, Math.min(karty.length - 1, cel + e.deltaX / 300));
        if (!animacja) animacja = requestAnimationFrame(animuj);

        clearTimeout(kolkoTimer);
        kolkoTimer = setTimeout(function () { doCelu(Math.round(cel)); }, 130);
    }, { passive: false });

    /* --- Reakcja na zmiane warunkow -------------------------------------- */

    function przelicz() {
        if (mniejRuchu.matches || !szeroki.matches) {
            // Tryb listy - czyscimy transformacje, zeby nic nie zostalo
            karty.forEach(function (k) {
                k.style.cssText = '';
                k.setAttribute('aria-hidden', 'false');
                var a = k.querySelector('a');
                if (a) a.tabIndex = 0;
            });
            return;
        }
        ustawKarty();
    }

    mniejRuchu.addEventListener('change', przelicz);
    szeroki.addEventListener('change', przelicz);
    window.addEventListener('resize', przelicz);

    przelicz();
})();
