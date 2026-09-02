document.addEventListener('DOMContentLoaded', () => {

    // 1. Reveal Elements on Scroll
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');

                // If it's a stat number, start counting
                if (entry.target.classList.contains('stat-item')) {
                    const number = entry.target.querySelector('.stat-number');
                    if (number && !number.classList.contains('counted')) {
                        animateValue(number);
                        number.classList.add('counted');
                    }
                }
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => revealObserver.observe(el));

    // 2. Animate Stats Value
    function animateValue(obj) {
        const target = +obj.getAttribute('data-target');
        const duration = 2000;
        const start = 0;
        let startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            obj.innerHTML = Math.floor(progress * (target - start) + start) + (target === 100 ? '%' : '');
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = target + (target === 100 ? '%' : '');
            }
        }
        window.requestAnimationFrame(step);
    }

    // 3. Header Glass Effect & Shrink
    const header = document.getElementById('main-header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 80) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 4. Mobile Menu Toggle
    const mobileMenu = document.getElementById('mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenu) {
        // Czytnik ekranu musi wiedzieć, czy menu jest rozwinięte
        const syncExpanded = () => {
            mobileMenu.setAttribute('aria-expanded', navLinks.classList.contains('active'));
        };

        mobileMenu.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenu.classList.toggle('open');
            syncExpanded();
        });

        // Close menu when a link is clicked
        const navItems = navLinks.querySelectorAll('a');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenu.classList.remove('open');
                syncExpanded();
            });
        });

        // Escape zamyka menu
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                mobileMenu.classList.remove('open');
                syncExpanded();
                mobileMenu.focus();
            }
        });
    }

    // 5. Terminology Modals
    const termGlossary = {
        seo: {
            title: "SEO (Optymalizacja)",
            desc: "SEO to szereg działań, dzięki którym Twoja strona 'podoba się' wyszukiwarkom takim jak Google. Oznacza to wyższą pozycję w wynikach wyszukiwania, co wprost przekłada się na większą ilość odwiedzin i potencjalnych klientów całkowicie za darmo."
        },
        nextjs: {
            title: "Next.js & React",
            desc: "Supernowoczesne technologie tworzenia stron wywodzące się od twórców Facebooka. Wyróżnia je błyskawiczne ładowanie, niezawodność i bezpieczeństwo. Strona ładuje się 'w mgnieniu oka' i nie posiada powolnych przeładowań znanych z ubiegłej dekady."
        },
        saas: {
            title: "SaaS (Oprogramowanie jako usługa)",
            desc: "W pełni działająca usługa dostępna przez przeglądarkę internetową, sprzedawana najczęściej jako abonament. Dobrym przykładem jest Netflix czy program do e-faktur – oprogramowanie wisi na serwerze, a Ty tylko z niego korzystasz z dowolnego urządzenia."
        }
    };

    const termModal = document.getElementById('term-modal');
    const termModalTitle = document.getElementById('term-modal-title');
    const termModalDesc = document.getElementById('term-modal-desc');
    const termModalClose = document.getElementById('term-modal-close');
    const termLinks = document.querySelectorAll('.term-link');

    if (termModal && termLinks.length > 0) {
        let termOstatnioAktywny = null;

        const zamknijTerm = () => {
            termModal.classList.remove('active');
            if (termOstatnioAktywny && termOstatnioAktywny.focus) termOstatnioAktywny.focus();
        };

        termLinks.forEach(link => {
            // .term-link to <span>, wiec bez tego nie da sie go dosiegnac klawiaturą
            link.setAttribute('tabindex', '0');
            link.setAttribute('role', 'button');

            const otworz = (e) => {
                e.preventDefault();
                const termKey = link.getAttribute('data-term');
                if (!termGlossary[termKey]) return;
                termOstatnioAktywny = link;
                termModalTitle.textContent = termGlossary[termKey].title;
                termModalDesc.textContent = termGlossary[termKey].desc;
                termModal.classList.add('active');
                termModalClose.focus();
            };

            link.addEventListener('click', otworz);
            link.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') otworz(e);
            });
        });

        termModalClose.addEventListener('click', zamknijTerm);

        termModal.addEventListener('click', (e) => {
            if (e.target === termModal) zamknijTerm();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && termModal.classList.contains('active')) zamknijTerm();
        });
    }

    // 6. Scroll to Top Button
    const scrollTopBtn = document.getElementById('scroll-top-btn');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });

        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Zgoda na cookies zyje teraz w consent.js — razem z Consent Mode v2
    // i modalem wstrzykiwanym na kazdej podstronie. Wczesniejsza wersja
    // zapisywala wybor do localStorage i nie robila z nim nic wiecej.

});

// ===== Kafelki jak kartki papieru (inspiracja: MengTo/sketchbook) =====
// Karta pochyla sie w 3D za kursorem, jakby byla sztywna kartka trzymana
// w palcach. Tylko transform — kompozytor, zero layoutu/paintu w petli.
// Wylacznie mysz (hover+fine) i tylko bez prefers-reduced-motion.
(function () {
    var mysz = window.matchMedia('(hover: hover) and (pointer: fine)');
    var spokoj = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (!mysz.matches || spokoj.matches) return;

    var MAKS_Y = 4;   // stopnie obrotu wokol osi pionowej
    var MAKS_X = 3;   // wokol poziomej — mniejszy, bo karty sa szersze niz wyzsze

    document.querySelectorAll('.card-grid .info-card').forEach(function (karta) {
        var klatka = null;

        karta.addEventListener('pointerenter', function () {
            karta.classList.add('karta-3d');
        });

        karta.addEventListener('pointermove', function (e) {
            if (klatka) return;
            klatka = requestAnimationFrame(function () {
                klatka = null;
                var r = karta.getBoundingClientRect();
                var px = (e.clientX - r.left) / r.width - 0.5;   // -0.5 .. 0.5
                var py = (e.clientY - r.top) / r.height - 0.5;
                karta.style.transform =
                    'perspective(900px)' +
                    ' rotateX(' + (-py * 2 * MAKS_X).toFixed(2) + 'deg)' +
                    ' rotateY(' + (px * 2 * MAKS_Y).toFixed(2) + 'deg)' +
                    ' translateY(-4px)';
            });
        });

        karta.addEventListener('pointerleave', function () {
            if (klatka) { cancelAnimationFrame(klatka); klatka = null; }
            karta.style.transform = '';
            karta.classList.remove('karta-3d');
        });
    });
})();

// ===== Karuzela artykulow (#blog na stronie glownej) =====
// Przewijanie zostawiamy przegladarce (scroll-snap): swipe, gladzik,
// Shift+kolko i strzalki klawiatury dzialaja bez naszego udzialu.
// Tutaj dokładamy tylko to, czego CSS nie da: strzalki i kropki.
// Kto ma wylaczony JS, dostaje sprawna karuzele bez sterowania —
// dlatego przyciski powstaja tu, a nie w HTML.
(function () {
    var tor = document.getElementById('blogTor');
    if (!tor) return;

    var karty = Array.prototype.slice.call(tor.querySelectorAll('.blog-karta'));
    if (karty.length < 2) return;

    var otoczka = tor.parentElement;
    var spokoj = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var ruch = spokoj ? 'auto' : 'smooth';

    // Szerokosc karty czytamy na biezaco — zmienia sie z szerokoscia okna
    // (clamp w CSS), wiec zapisanie jej raz zepsuloby krok po obroceniu telefonu.
    function krok() {
        return karty[0].getBoundingClientRect().width + 24;
    }

    function strzalka(kierunek, etykieta, znak) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'karuzela-strzalka karuzela-' + kierunek;
        b.setAttribute('aria-label', etykieta);
        b.setAttribute('aria-controls', 'blogTor');
        b.textContent = znak;
        b.addEventListener('click', function () {
            tor.scrollBy({ left: kierunek === 'dalej' ? krok() : -krok(), behavior: ruch });
        });
        otoczka.appendChild(b);
        return b;
    }

    var wstecz = strzalka('wstecz', 'Poprzedni artykuł', '‹');
    var dalej = strzalka('dalej', 'Następny artykuł', '›');

    var kropki = document.createElement('div');
    kropki.className = 'karuzela-kropki';
    var listaKropek = karty.map(function (karta, i) {
        var k = document.createElement('button');
        k.type = 'button';
        k.className = 'karuzela-kropka';
        k.setAttribute('aria-label', 'Artykuł ' + (i + 1) + ' z ' + karty.length);
        k.addEventListener('click', function () {
            // block:'nearest' — inaczej przegladarka przy okazji przewinelaby
            // strone w pionie do sekcji bloga.
            karta.scrollIntoView({ inline: 'start', block: 'nearest', behavior: ruch });
        });
        kropki.appendChild(k);
        return k;
    });
    otoczka.parentNode.insertBefore(kropki, otoczka.nextSibling);

    var czeka = false;
    function odswiez() {
        var i = Math.round(tor.scrollLeft / krok());
        if (i < 0) i = 0;
        if (i > karty.length - 1) i = karty.length - 1;
        listaKropek.forEach(function (k, n) {
            if (n === i) {
                k.setAttribute('aria-current', 'true');
            } else {
                k.removeAttribute('aria-current');
            }
        });
        wstecz.disabled = tor.scrollLeft <= 4;
        dalej.disabled = tor.scrollLeft + tor.clientWidth >= tor.scrollWidth - 4;
    }

    tor.addEventListener('scroll', function () {
        if (czeka) return;
        czeka = true;
        requestAnimationFrame(function () { czeka = false; odswiez(); });
    }, { passive: true });

    window.addEventListener('resize', odswiez);

    // Na szerokim ekranie zaczynamy od SRODKA zestawu: karuzela od razu
    // pokazuje karty po obu stronach wyroznionej i widac, ze da sie jechac
    // w obie strony. Na telefonie odwrotnie — miesci sie tam jedna karta,
    // a strzalki sa schowane, wiec start od srodka chowalby dwa najnowsze
    // wpisy bez czytelnego sposobu powrotu. Tam zaczynamy od pierwszej.
    var szeroki = window.matchMedia('(min-width: 641px)').matches;
    var poczatkowa = szeroki ? Math.max(0, Math.floor((karty.length - 1) / 2)) : 0;
    if (poczatkowa) {
        // Bez plynnego przewijania — przy wejsciu na strone nic nie ma jechac.
        tor.scrollLeft = krok() * poczatkowa;
    }

    odswiez();
})();


// ===== Rejestracja workera — wylacznie po to, zeby dalo sie zainstalowac =====
// Chrome proponuje „zainstaluj aplikacje" dopiero, gdy widzi workera z obsluga
// fetch. Sam worker nic nie cache'uje (patrz komentarz w sw.js), wiec nie ma
// ryzyka, ze ktos zostanie ze stara wersja strony.
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/sw.js').catch(function () {
            // brak workera nie psuje niczego — strona dziala normalnie
        });
    });
}
