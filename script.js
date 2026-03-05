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
        mobileMenu.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenu.classList.toggle('open');
        });

        // Close menu when a link is clicked
        const navItems = navLinks.querySelectorAll('a');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenu.classList.remove('open');
            });
        });
    }

    // 5. Submit Form (Mockup)
    const form = document.querySelector('.contact-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const originalText = btn.innerText;
            btn.innerText = 'Wysłano!';
            btn.style.background = 'var(--accent-cyan)';
            form.reset();
            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.background = '';
            }, 3000);
        });
    }

    // 6. Terminology Modals
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
        termLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const termKey = link.getAttribute('data-term');
                if (termGlossary[termKey]) {
                    termModalTitle.textContent = termGlossary[termKey].title;
                    termModalDesc.textContent = termGlossary[termKey].desc;
                    termModal.classList.add('active');
                }
            });
        });

        termModalClose.addEventListener('click', () => {
            termModal.classList.remove('active');
        });

        termModal.addEventListener('click', (e) => {
            if (e.target === termModal) {
                termModal.classList.remove('active');
            }
        });
    }

    // 7. Scroll to Top Button
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

    // 8. Cookie Consent System
    const cookieTrigger = document.getElementById('cookie-trigger');
    const cookieOverlay = document.getElementById('cookie-overlay');
    const cookieModal = document.getElementById('cookie-modal');
    const cookieClose = document.getElementById('cookie-close');
    const cookieClosePrivacy = document.getElementById('cookie-close-privacy');
    const cookieSave = document.getElementById('cookie-save');
    const cookieReject = document.getElementById('cookie-reject');
    const cookieAcceptAll = document.getElementById('cookie-accept-all');
    const cookieShowPrivacy = document.getElementById('cookie-show-privacy');
    const cookieBack = document.getElementById('cookie-back');
    const cookieMainView = document.getElementById('cookie-main-view');
    const cookiePrivacyView = document.getElementById('cookie-privacy-view');

    function openCookieModal() {
        cookieOverlay.classList.add('active');
        cookieModal.classList.add('active');
        // Reset to main view
        cookieMainView.classList.remove('cookie-main-view-hidden');
        cookiePrivacyView.classList.remove('active');
    }

    function closeCookieModal() {
        cookieOverlay.classList.remove('active');
        cookieModal.classList.remove('active');
    }

    function saveCookiePreferences(choice) {
        const functional = document.getElementById('cookie-functional');
        const analytics = document.getElementById('cookie-analytics');
        const prefs = {
            choice: choice,
            functional: choice === 'all' ? true : (choice === 'none' ? false : (functional ? functional.checked : false)),
            analytics: choice === 'all' ? true : (choice === 'none' ? false : (analytics ? analytics.checked : false)),
            timestamp: Date.now()
        };
        localStorage.setItem('cookieConsent', JSON.stringify(prefs));
        closeCookieModal();
    }

    if (cookieTrigger) {
        // Show modal on first visit (no consent stored)
        if (!localStorage.getItem('cookieConsent')) {
            setTimeout(() => { openCookieModal(); }, 1500);
        }

        cookieTrigger.addEventListener('click', openCookieModal);
        cookieOverlay.addEventListener('click', closeCookieModal);
        cookieClose.addEventListener('click', closeCookieModal);
        if (cookieClosePrivacy) cookieClosePrivacy.addEventListener('click', closeCookieModal);

        cookieAcceptAll.addEventListener('click', () => saveCookiePreferences('all'));
        cookieReject.addEventListener('click', () => saveCookiePreferences('none'));
        cookieSave.addEventListener('click', () => saveCookiePreferences('custom'));

        // Privacy policy sub-view toggle
        cookieShowPrivacy.addEventListener('click', () => {
            cookieMainView.classList.add('cookie-main-view-hidden');
            cookiePrivacyView.classList.add('active');
        });

        cookieBack.addEventListener('click', () => {
            cookiePrivacyView.classList.remove('active');
            cookieMainView.classList.remove('cookie-main-view-hidden');
        });
    }



    });
