// Service worker w najskromniejszej mozliwej postaci: przepuszcza kazde
// zadanie do sieci i nic nie zapisuje.
//
// PO CO WIEC ISTNIEJE: Chrome proponuje instalacje strony na ekranie
// glownym dopiero wtedy, gdy widzi zarejestrowany worker z obsluga zdarzenia
// fetch. Bez niego zostaje reczne „dodaj do ekranu glownego", ktorego
// prawie nikt nie znajduje.
//
// CZEGO CELOWO NIE ROBI: nie cache'uje. Worker trzymajacy kopie plikow
// potrafi serwowac stara wersje strony jeszcze dlugo po wdrozeniu, i to
// w sposob, ktorego uzytkownik nie umie naprawic. Przy stronie firmowej
// aktualizowanej co kilka dni ta cena jest za wysoka — cache mamy juz
// na brzegu CDN i w naglowkach, gdzie da sie nim sterowac.

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => { /* przepuszczamy do sieci */ });
