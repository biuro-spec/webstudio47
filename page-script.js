/* ==========================================================================
   page-script.js — obsługa formularza kontaktowego (Google Apps Script)
   Ładowany tylko na podstronach z formularzem. Wymaga script.js dla nawigacji.
   ========================================================================== */

(function () {
    'use strict';

    // Adres wdrożonej aplikacji internetowej Apps Script.
    // Instrukcja wdrożenia: apps-script/README.md
    var ENDPOINT = 'https://script.google.com/macros/s/WSTAW_TUTAJ_ID_WDROZENIA/exec';

    var form = document.getElementById('kontakt-form');
    if (!form) return;

    var statusBox = document.getElementById('form-status');
    var submitBtn = form.querySelector('.form-submit');
    var submitLabel = submitBtn ? submitBtn.textContent : '';

    /* --- Temat z adresu (np. /kontakt/?temat=seo) ------------------------ */

    (function prefillTopic() {
        var wanted = new URLSearchParams(window.location.search).get('temat');
        var select = form.elements.temat;
        if (!wanted || !select) return;

        for (var i = 0; i < select.options.length; i++) {
            if (select.options[i].value === wanted) {
                select.selectedIndex = i;
                return;
            }
        }
    })();

    /* --- Walidacja ------------------------------------------------------- */

    var RULES = {
        imie: function (v) {
            if (v.trim().length < 2) return 'Podaj imię — choćby samo imię, bez nazwiska.';
            return '';
        },
        email: function (v) {
            if (!v.trim()) return 'Bez adresu e-mail nie będę mieć jak odpisać.';
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())) return 'Ten adres wygląda na niekompletny.';
            return '';
        },
        telefon: function (v) {
            if (!v.trim()) return '';
            var digits = v.replace(/[^0-9]/g, '');
            if (digits.length < 9) return 'Numer telefonu wygląda na za krótki.';
            return '';
        },
        wiadomosc: function (v) {
            if (v.trim().length < 20) return 'Napisz kilka zdań więcej — łatwiej mi będzie ocenić, czy pomogę.';
            return '';
        }
    };

    function errorBoxFor(field) {
        return document.getElementById('err-' + field.name);
    }

    function validateField(field) {
        var rule = RULES[field.name];
        if (!rule) return true;

        var message = rule(field.value);
        var box = errorBoxFor(field);

        if (message) {
            field.setAttribute('aria-invalid', 'true');
            if (box) box.textContent = message;
            return false;
        }

        field.removeAttribute('aria-invalid');
        if (box) box.textContent = '';
        return true;
    }

    Object.keys(RULES).forEach(function (name) {
        var field = form.elements[name];
        if (!field) return;

        // Walidujemy dopiero po opuszczeniu pola — nie krzyczymy podczas pisania.
        field.addEventListener('blur', function () { validateField(field); });
        field.addEventListener('input', function () {
            if (field.getAttribute('aria-invalid') === 'true') validateField(field);
        });
    });

    /* --- Komunikaty ------------------------------------------------------ */

    function setStatus(type, html) {
        if (!statusBox) return;
        statusBox.className = 'form-status ' + type;
        statusBox.innerHTML = html;
    }

    function clearStatus() {
        if (!statusBox) return;
        statusBox.className = 'form-status';
        statusBox.textContent = '';
    }

    function setBusy(busy) {
        if (!submitBtn) return;
        submitBtn.disabled = busy;
        submitBtn.textContent = busy ? 'Wysyłam…' : submitLabel;
    }

    /* --- Wysyłka --------------------------------------------------------- */

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        clearStatus();

        // Honeypot — boty wypełniają wszystko, ludzie tego pola nie widzą.
        if (form.elements.firma_www && form.elements.firma_www.value) return;

        var firstInvalid = null;
        Object.keys(RULES).forEach(function (name) {
            var field = form.elements[name];
            if (field && !validateField(field) && !firstInvalid) firstInvalid = field;
        });

        var consent = form.elements.zgoda;
        var brakZgody = consent && !consent.checked;

        if (firstInvalid) {
            // Puste pola są ważniejsze niż zgoda — o niej powiemy, gdy reszta będzie gotowa.
            setStatus('err', 'Popraw zaznaczone pola i wyślij ponownie.');
            firstInvalid.focus();
            return;
        }

        if (brakZgody) {
            setStatus('err', 'Zaznacz zgodę na kontakt — bez niej nie mogę przetwarzać Twoich danych.');
            consent.focus();
            return;
        }

        if (ENDPOINT.indexOf('WSTAW_TUTAJ') !== -1) {
            setStatus('err', 'Formularz nie jest jeszcze podłączony. Zadzwoń: <a href="tel:+48602622840">602 622 840</a> lub napisz na <a href="mailto:kontakt@webstudio47.pl">kontakt@webstudio47.pl</a>.');
            return;
        }

        setBusy(true);

        var payload = new URLSearchParams();
        payload.append('imie', form.elements.imie.value.trim());
        payload.append('email', form.elements.email.value.trim());
        payload.append('telefon', form.elements.telefon ? form.elements.telefon.value.trim() : '');
        payload.append('firma', form.elements.firma ? form.elements.firma.value.trim() : '');
        payload.append('temat', form.elements.temat ? form.elements.temat.value : '');
        payload.append('budzet', form.elements.budzet ? form.elements.budzet.value : '');
        payload.append('wiadomosc', form.elements.wiadomosc.value.trim());
        payload.append('strona', window.location.pathname);

        // URLSearchParams daje Content-Type: application/x-www-form-urlencoded,
        // czyli żądanie „proste" — bez preflightu, którego Apps Script nie obsługuje.
        fetch(ENDPOINT, { method: 'POST', body: payload })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (!data || data.status !== 'ok') throw new Error(data && data.message ? data.message : 'Odpowiedź serwera bez potwierdzenia.');

                setStatus('ok', '<strong>Dziękuję — wiadomość dotarła.</strong><br>Odzywam się w ciągu jednego dnia roboczego. Jeśli sprawa jest pilna, dzwoń: <a href="tel:+48602622840">602 622 840</a>.');
                form.reset();

                if (typeof gtag === 'function') {
                    gtag('event', 'generate_lead', {
                        event_category: 'formularz',
                        event_label: form.elements.temat ? form.elements.temat.value : 'kontakt'
                    });
                }
            })
            .catch(function () {
                setStatus('err', 'Nie udało się wysłać wiadomości. Napisz na <a href="mailto:kontakt@webstudio47.pl">kontakt@webstudio47.pl</a> albo zadzwoń: <a href="tel:+48602622840">602 622 840</a>.');
            })
            .finally(function () {
                setBusy(false);
            });
    });
})();
