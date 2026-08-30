/**
 * WebStudio47 — odbiór zgłoszeń z formularza kontaktowego.
 *
 * Zapisuje każde zgłoszenie do Arkusza Google i wysyła powiadomienie
 * na adres firmowy. Wdrożenie: patrz apps-script/README.md
 */

// ——— Konfiguracja ————————————————————————————————————————————————

var POWIADOMIENIE_NA = 'kontakt@webstudio47.pl';
var NAZWA_ARKUSZA = 'Zgloszenia';

// Nazwy tematów w formularzu → czytelne etykiety w mailu i arkuszu.
var TEMATY = {
  strona: 'Strona firmowa',
  landing: 'Landing page',
  sklep: 'Sklep internetowy',
  aplikacja: 'Aplikacja webowa',
  seo: 'Pozycjonowanie (SEO)',
  audyt: 'Audyt SEO',
  wizytowka: 'Profil Firmy w Google',
  inne: 'Coś innego'
};

// ——— Wejście ——————————————————————————————————————————————————————

function doPost(e) {
  try {
    var dane = odczytajDane(e);

    if (!dane.imie || !dane.email || !dane.wiadomosc) {
      return odpowiedz({ status: 'error', message: 'Brak wymaganych pól.' });
    }

    // Honeypot: pole niewidoczne na stronie. Wypełnione = bot.
    // Odpowiadamy sukcesem, żeby bot nie próbował dalej.
    if (dane.firma_www) {
      return odpowiedz({ status: 'ok' });
    }

    zapiszDoArkusza(dane);
    wyslijPowiadomienie(dane);

    return odpowiedz({ status: 'ok' });

  } catch (blad) {
    console.error('Blad obslugi zgloszenia: ' + blad);
    return odpowiedz({ status: 'error', message: 'Błąd po stronie serwera.' });
  }
}

/**
 * Odpowiada na żądanie GET — przydatne do sprawdzenia, czy wdrożenie żyje.
 */
function doGet() {
  return odpowiedz({ status: 'ok', message: 'WebStudio47 — odbiornik formularza działa.' });
}

// ——— Logika ———————————————————————————————————————————————————————

function odczytajDane(e) {
  var p = (e && e.parameter) ? e.parameter : {};

  return {
    imie: (p.imie || '').trim(),
    email: (p.email || '').trim(),
    telefon: (p.telefon || '').trim(),
    firma: (p.firma || '').trim(),
    temat: TEMATY[p.temat] || p.temat || '—',
    budzet: (p.budzet || '').trim() || '—',
    wiadomosc: (p.wiadomosc || '').trim(),
    strona: (p.strona || '').trim(),
    firma_www: (p.firma_www || '').trim()
  };
}

function zapiszDoArkusza(dane) {
  var plik = SpreadsheetApp.getActiveSpreadsheet();
  var arkusz = plik.getSheetByName(NAZWA_ARKUSZA);

  if (!arkusz) {
    arkusz = plik.insertSheet(NAZWA_ARKUSZA);
    arkusz.appendRow([
      'Data', 'Imię', 'Firma', 'E-mail', 'Telefon',
      'Temat', 'Budżet', 'Wiadomość', 'Podstrona'
    ]);
    arkusz.getRange(1, 1, 1, 9).setFontWeight('bold');
    arkusz.setFrozenRows(1);
  }

  arkusz.appendRow([
    new Date(),
    dane.imie,
    dane.firma,
    dane.email,
    dane.telefon,
    dane.temat,
    dane.budzet,
    dane.wiadomosc,
    dane.strona
  ]);
}

function wyslijPowiadomienie(dane) {
  var tytul = 'Zapytanie ze strony: ' + dane.temat +
    (dane.firma ? ' — ' + dane.firma : ' — ' + dane.imie);

  var tresc =
    'Nowe zapytanie z webstudio47.pl\n' +
    '───────────────────────────────\n\n' +
    'Imię:      ' + dane.imie + '\n' +
    'Firma:     ' + (dane.firma || '—') + '\n' +
    'E-mail:    ' + dane.email + '\n' +
    'Telefon:   ' + (dane.telefon || '—') + '\n' +
    'Temat:     ' + dane.temat + '\n' +
    'Budżet:    ' + dane.budzet + '\n' +
    'Podstrona: ' + (dane.strona || '—') + '\n\n' +
    'Wiadomość:\n' +
    dane.wiadomosc + '\n';

  var opcje = { name: 'Formularz webstudio47.pl' };

  // Odpowiedź „Odpowiedz" w kliencie poczty trafi wprost do klienta.
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(dane.email)) {
    opcje.replyTo = dane.email;
  }

  MailApp.sendEmail(POWIADOMIENIE_NA, tytul, tresc, opcje);
}

// ——— Pomocnicze ———————————————————————————————————————————————————

function odpowiedz(obiekt) {
  return ContentService
    .createTextOutput(JSON.stringify(obiekt))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Uruchom raz ręcznie z edytora, żeby sprawdzić zapis i wysyłkę maila
 * bez wypełniania formularza na stronie.
 */
function testZgloszenia() {
  var wynik = doPost({
    parameter: {
      imie: 'Jan',
      firma: 'Testowa sp. z o.o.',
      email: 'jan@example.com',
      telefon: '600 100 200',
      temat: 'strona',
      budzet: '2000-5000',
      wiadomosc: 'To jest testowe zgłoszenie wysłane z edytora Apps Script.',
      strona: '/kontakt/'
    }
  });

  console.log(wynik.getContent());
}
