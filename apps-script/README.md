# Formularz kontaktowy — wdrożenie backendu

Formularz na `/kontakt/` wysyła dane do aplikacji internetowej Google Apps Script.
Ta z kolei zapisuje zgłoszenie do Arkusza Google i wysyła powiadomienie na
`kontakt@webstudio47.pl`.

Wszystko dzieje się na Twoim koncie Google — dane nie przechodzą przez żadną
firmę trzecią, więc nie trzeba dopisywać nikogo do polityki prywatności.

---

## Krok 1 — arkusz

1. Wejdź na [sheets.new](https://sheets.new) i utwórz nowy arkusz.
2. Nazwij go np. **WebStudio47 — zgłoszenia**.
3. Nie twórz żadnych zakładek ręcznie — skrypt sam założy arkusz `Zgloszenia`
   wraz z nagłówkami przy pierwszym zgłoszeniu.

## Krok 2 — skrypt

1. W arkuszu: **Rozszerzenia → Apps Script**.
2. Usuń zawartość pliku `Kod.gs` i wklej całą treść z
   [`Kod.gs`](Kod.gs) z tego katalogu.
3. Zapisz (Ctrl+S).

## Krok 3 — test przed wdrożeniem

1. Na górze edytora wybierz z listy funkcję **`testZgloszenia`** i kliknij
   **Uruchom**.
2. Google poprosi o uprawnienia — zaakceptuj (ekran „Ta aplikacja nie została
   zweryfikowana" → *Zaawansowane* → *Przejdź do…*). To Twój własny skrypt.
3. Sprawdź, czy w arkuszu pojawił się wiersz i czy na skrzynkę przyszedł mail.

## Krok 4 — wdrożenie

1. **Wdróż → Nowe wdrożenie**.
2. Typ: **Aplikacja internetowa**.
3. Ustaw:
   - *Wykonaj jako*: **Ja**
   - *Kto ma dostęp*: **Wszyscy** ← to jest kluczowe, bez tego formularz
     dostanie błąd
4. Kliknij **Wdróż** i skopiuj **adres aplikacji internetowej**. Wygląda tak:
   `https://script.google.com/macros/s/AKfycb.../exec`

## Krok 5 — podłączenie strony

W pliku [`page-script.js`](../page-script.js), w linii z `ENDPOINT`, zamień
wartość na skopiowany adres:

```js
var ENDPOINT = 'https://script.google.com/macros/s/TU_WKLEJ_SWOJ_ADRES/exec';
```

Wgraj plik na serwer. Gotowe.

> Dopóki adres nie zostanie podmieniony, formularz **nie udaje, że wysyła** —
> pokazuje komunikat z numerem telefonu i adresem e-mail. To celowe.

---

## Aktualizacja skryptu w przyszłości

Po każdej zmianie w `Kod.gs` **nie wystarczy zapisać** — trzeba wdrożyć zmiany,
inaczej strona nadal korzysta ze starej wersji:

**Wdróż → Zarządzaj wdrożeniami →** ikona ołówka przy istniejącym wdrożeniu **→
Wersja: Nowa → Wdróż**.

Ten sposób zachowuje ten sam adres. Wybranie *Nowe wdrożenie* generuje nowy
adres i wymagałoby ponownej zmiany w `page-script.js`.

---

## Rozwiązywanie problemów

| Objaw | Przyczyna | Co zrobić |
|---|---|---|
| Formularz pokazuje błąd wysyłki | wdrożenie ustawione na „Tylko ja" | zmień dostęp na **Wszyscy** i wdróż nową wersję |
| Zgłoszenia nie zapisują się w arkuszu | skrypt utworzony poza arkuszem | skrypt musi być założony przez **Rozszerzenia → Apps Script** w tym arkuszu |
| Mail nie przychodzi | dzienny limit Gmaila (100 maili) albo folder spam | sprawdź spam; przy takim ruchu limit nie ma prawa się wyczerpać |
| Wszystko działa, ale strona nadal pokazuje stary komunikat | pamięć podręczna przeglądarki | podbij `?v=` przy `page-script.js` w `kontakt/index.html` |

## Zabezpieczenie przed spamem

Formularz ma ukryte pole `firma_www` (tzw. honeypot). Człowiek go nie widzi,
bot wypełnia wszystko jak leci. Zgłoszenie z wypełnionym polem jest po cichu
odrzucane — bot dostaje odpowiedź „ok" i nie próbuje dalej.

To wystarcza na automaty. Gdyby kiedyś pojawił się spam kierowany ręcznie,
kolejnym krokiem byłoby dołożenie Cloudflare Turnstile.
