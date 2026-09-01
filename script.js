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
