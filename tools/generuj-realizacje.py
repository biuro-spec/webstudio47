#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator stron case studies dla webstudio47.pl.

Chrome strony (nagłówek, stopka, dane strukturalne) jest wspólny, żeby nie
rozjechał się przy zmianach. Treść każdej realizacji jest pisana osobno —
opisujemy wyłącznie to, co da się sprawdzić na żywej stronie klienta.
Żadnych wymyślonych wyników ani opinii.

Uruchomienie:  python tools/generuj-realizacje.py
"""

import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pomiary

KATALOG = pathlib.Path(__file__).resolve().parent.parent
BAZA = "https://webstudio47.pl"

def sekcja_dlaczego(r):
    """Sekcja „Dlaczego tak, a nie inaczej" — rozumowanie stojące za projektem.

    Case studies miały po 250–330 słów i sprowadzały się do wyliczenia funkcji,
    czyli do tego, co każdy konkurent może napisać o sobie tak samo. Rozumowanie
    jest jedyną częścią, której nie da się skopiować, bo trzeba było te decyzje
    faktycznie podjąć. Realizacja bez tego pola po prostu nie dostaje sekcji —
    lepiej brak sekcji niż sekcja wypełniona ogólnikami.
    """
    akapity = r.get("dlaczego") or []
    if not akapity:
        return ""
    tresc = "\n".join(f'                    <p>{a}</p>' for a in akapity)
    return (
        "\n        <!-- Dlaczego tak -->\n"
        '        <section>\n'
        '            <div class="container">\n'
        '                <div class="prose reveal">\n'
        '                    <h2>Dlaczego tak, a&nbsp;nie inaczej</h2>\n'
        f'{tresc}\n'
        '                </div>\n'
        '            </div>\n'
        '        </section>\n'
    )


def mala_pierwsza(t):
    """Obniza tylko pierwsza litere — .lower() zjadalby skrotowce.

    „Aplikacja SaaS" po .lower() stawala sie „aplikacja saas", i to
    zarowno w danych strukturalnych, jak i w atrybucie alt czytanym przez
    czytnik ekranu. Dla pozostalych branz wynik jest taki sam jak dotad.
    """
    return t[:1].lower() + t[1:]


def bezp(tekst):
    """html.escape, ale nie psuje twardych spacji wpisanych w tresci.

    Bez tego „&nbsp;" wstawione przez tools/sierotki.py wychodzi z escape'a
    jako widoczne „&amp;nbsp;" — czytelnik widzi wtedy w zdaniu doslowny
    ciag znakow zamiast spacji. Zdarzylo sie to 2026-09-01 w opisach meta
    i pytaniach FAQ.
    """
    return html.escape(tekst).replace('&amp;nbsp;', '&nbsp;')

FB = "https://www.facebook.com/profile.php?id=61578430357755"

# ——— Treść realizacji ————————————————————————————————————————————————

REALIZACJE = [
    dict(
        slug="strona-dla-salonu-groomerskiego",
        klient="hOla Perros",
        branza="Salon groomerski",
        miasto="Racibórz",
        domena="holaperros.pl",
        miniatura="holaperros-thumb.webp",
        tytul="Strona dla salonu groomerskiego — hOla Perros",
        opisMeta="Strona dla salonu pielęgnacji psów w Raciborzu: cennik usług z czasem zabiegu, galeria metamorfoz, sklepik i szybki kontakt. Zobacz, jak powstała.",
        h1="Strona dla salonu groomerskiego",
        lead="Salon pielęgnacji i&nbsp;strzyżenia psów w&nbsp;Raciborzu. Marka premium, która musiała wyglądać premium także w&nbsp;internecie — i&nbsp;skrócić drogę od obejrzenia cennika do umówienia wizyty.",
        wyzwanie=[
            "Groomer sprzedaje coś, czego nie widać na cenniku: <strong>spokój psa podczas wizyty</strong>. Suchy wykaz usług i&nbsp;cen tego nie odda — trzeba było pokazać atmosferę salonu i&nbsp;efekt pracy.",
            "Drugi problem był praktyczny. Najczęstsze pytania — ile trwa zabieg i&nbsp;ile kosztuje przy takim psie — wracały w&nbsp;każdej rozmowie. Strona musiała odpowiedzieć na nie, zanim ktokolwiek podniesie słuchawkę.",
        ],
        zbudowane=[
            ("Rezerwacja terminu — zbudowana, na razie wyłączona",
             "Moduł rezerwacji jest gotowy i&nbsp;czeka na jedną decyzję: właścicielka woli "
             "na tym etapie umawiać wizyty osobiście, bo czas zabiegu waha się od&nbsp;1,5 "
             "do&nbsp;4 godzin i&nbsp;zależy od psa. Dlatego na stronie widać dziś trzy drogi "
             "kontaktu — telefon, WhatsApp z&nbsp;gotową treścią wiadomości i&nbsp;Instagram. "
             "Włączenie rezerwacji to przełącznik, nie nowy projekt."),
            ("Galeria metamorfoz", "Zdjęcia przed i&nbsp;po są tu głównym argumentem sprzedażowym — pokazują poziom wykonania lepiej niż jakikolwiek opis."),
            ("Przejrzysty cennik według rozmiaru psa", "Najczęstsze pytanie w&nbsp;tej branży brzmi „ile to będzie kosztować u&nbsp;mojego psa”. Odpowiedź jest na stronie, nie w&nbsp;rozmowie telefonicznej."),
            ("Sklepik z&nbsp;akcesoriami", "Ręcznie zdobione obroże i&nbsp;złote zawieszki z&nbsp;grawerem — dodatkowy kanał sprzedaży obok samych zabiegów."),
            ("Blog poradnikowy", "Treści o&nbsp;pielęgnacji, które ściągają ruch z&nbsp;wyszukiwarki na długo po publikacji."),
        ],
        design="Jasna, elegancka typografia z&nbsp;krojem szeryfowym w&nbsp;nagłówkach — celowo bliżej estetyki salonu kosmetycznego niż sklepu zoologicznego. Marka jest premium i&nbsp;wygląd strony miał to potwierdzać, zanim klient przeczyta pierwsze zdanie.",
        dlaczego=[
            "Strona główna to jedna długa strona i kolejność sekcji nie jest przypadkowa: kto prowadzi salon, menu zabiegów, cennik, sklepik, najczęstsze pytania, kontakt. Blog i metamorfozy dostały osobne adresy, poza tą stroną.",
            "Rezerwacja terminu jest zbudowana, ale dziś jej nie widać — i to nie jest przeoczenie. Właścicielka woli na tym etapie umawiać wizyty sama, bo czas zabiegu jest różny; cennik podaje go przy każdej pozycji, od 1,5 do 4 godzin. Umawianie prowadzą więc trzy przyciski: telefon, WhatsApp z gotową treścią wiadomości i Instagram. Wolę zostawić gotowy moduł wyłączony niż zmuszać kogoś do narzędzia, którego jeszcze nie chce. Sklepik też został bez koszyka: trzy pozycje i jeden przycisk „Zapytaj o dostępne wzory”, zamiast udawanego sklepu internetowego.",
            "Kompromis dotyczył wyglądu. Marka jest premium, więc chciałem dużego zdjęcia na wejściu, szeryfowych nagłówków i złota — a to kosztuje czas ładowania. Zdjęcie otwierające ma podane wymiary i jest wczytywane z najwyższym priorytetem. Ceny podałem widełkami, nie jedną kwotą, razem z orientacyjnym czasem zabiegu. Wolałem napisać to wprost na stronie niż tłumaczyć przy odbiorze psa.",
            "PageSpeed Insights zmierzył 92 na telefonie i 100 na komputerze. To pomiar z jednego dnia, nie dowód na sprzedaż.",
        ],
        tagi=["Groomer", "Rezerwacja (wyłączona)", "Cennik z czasem zabiegu", "Sklepik", "Blog", "SEO lokalne"],
    ),
    dict(
        slug="strona-dla-zlotej-raczki",
        klient="Super Irek",
        branza="Usługi remontowe",
        miasto="Racibórz",
        domena="superirek.pl",
        miniatura="superirek-thumb.webp",
        tytul="Strona dla złotej rączki — Super Irek",
        opisMeta="Strona dla usług remontowych i montażowych w Raciborzu, zbudowana wokół jednego celu: telefonu od klienta. Zobacz, jak powstała.",
        h1="Strona dla złotej rączki",
        lead="Montaż mebli, drobna hydraulika, lampy i&nbsp;gniazdka, poprawki po fachowcach. Usługa, w&nbsp;której klient dzwoni od razu albo nie dzwoni wcale.",
        wyzwanie=[
            "Ta branża ma jeden problem z&nbsp;wiarygodnością: <strong>każdy może napisać, że „montuje meble”</strong>. Klient wpuszcza obcą osobę do mieszkania, więc decyduje na podstawie zaufania, nie ceny.",
            "Do tego ścieżka jest krótka. Ktoś ma popsuty kran teraz i&nbsp;albo zadzwoni w&nbsp;ciągu minuty, albo pójdzie do następnego wyniku w&nbsp;Google.",
        ],
        zbudowane=[
            ("Numer telefonu jako główny element", "Widoczny w&nbsp;nagłówku, w&nbsp;sekcji otwierającej i&nbsp;jako przyklejony przycisk na telefonie. Cała strona prowadzi do jednego działania."),
            ("Autorska ilustracja maskotki", "Zamiast zdjęć stockowych — rozpoznawalna postać, która nadaje marce twarz i&nbsp;odróżnia ją od konkurencji z&nbsp;tego samego miasta."),
            ("Rozbicie na konkretne usługi", "Osobne sekcje dla montażu mebli, hydrauliki, elektryki i&nbsp;poprawek. Każda odpowiada na inne zapytanie w&nbsp;wyszukiwarce."),
            ("Galeria realizacji", "Zdjęcia z&nbsp;prawdziwych zleceń — dowód, że firma istnieje i&nbsp;pracuje."),
            ("Opinie sąsiadów", "Społeczny dowód słuszności w&nbsp;formie, która pasuje do usługi lokalnej: rekomendacja od kogoś z&nbsp;okolicy."),
        ],
        design="Zieleń i&nbsp;biel, dużo powietrza, duże przyciski. Strona ma być czytelna dla osoby po pięćdziesiątce przeglądającej ją na telefonie — bo to jest realny klient tej usługi.",
        dlaczego=[
            "Strona główna nie jest katalogiem usług, tylko odpowiedzią na pytanie „czy wpuszczę tę osobę do mieszkania”. Konkret przeniosłem na osobne adresy: montaż mebli, drobna hydraulika, lampy i gniazdka, lustra i telewizory, poprawki po fachowcach. Każdy ma własny nagłówek i własne pytania na dole.",
            "Odradziłem formułę „wycena indywidualna”. Cennik z widełkami stoi na osobnej podstronie, razem z minimalną wartością zlecenia i zasadą dojazdu poza miasto. Ostateczna wycena i tak jest przed startem, i tak jest to na stronie napisane.",
            "Nie zrobiłem bloga ani rezerwacji online, choć u innych klientów robię jedno i drugie. Formularz nie trafia do żadnego panelu ani skrzynki — składa wiadomość na WhatsAppa. Nie ma czego pilnować i nie ma się gdzie logować. Nie budowałem też osobnych stron pod każdą wieś w powiecie; jest jedna lista miejscowości.",
            "PageSpeed pokazał 89 na komórce i 97 na komputerze. To pomiar z jednego dnia, nie dowód na sprzedaż, i ważniejszy jest tu ten gorszy wynik. Strona ma się pokazać, zanim ktoś wróci do wyników.",
        ],
        tagi=["Usługi lokalne", "Konwersja", "Ilustracja", "SEO lokalne"],
    ),
    dict(
        slug="strona-dla-firmy-sprzatajacej",
        klient="Czysto-Po",
        branza="Firma sprzątająca",
        miasto="Racibórz",
        domena="czysto-po.pl",
        miniatura="czysto-po-thumb.webp",
        tytul="Strona dla firmy sprzątającej — Czysto-Po",
        opisMeta="Strona dla firmy sprzątającej z Raciborza: ozonowanie, dezynfekcja, sprzątanie po zgonach i po remontach. Zobacz, jak powstała.",
        h1="Strona dla firmy sprzątającej",
        lead="Sprzątanie mieszkań, ozonowanie, dezynfekcja, sprzątanie po zgonach i&nbsp;po zbieractwie. Usługi, których szuka się w&nbsp;bardzo różnych stanach emocjonalnych.",
        wyzwanie=[
            "Ta firma świadczy usługi z&nbsp;dwóch zupełnie różnych światów. Sprzątanie po remoncie zamawia się na spokojnie, z&nbsp;wyprzedzeniem. <strong>Sprzątanie po zgonie zamawia się w&nbsp;najgorszym tygodniu swojego życia.</strong>",
            "Jeden ton komunikacji nie mógł obsłużyć obu sytuacji. Strona musiała być rzeczowa tam, gdzie klient porównuje oferty, i&nbsp;powściągliwa tam, gdzie potrzebuje po prostu pomocy.",
        ],
        zbudowane=[
            ("Rozdzielenie usług na osobne sekcje", "Każda usługa specjalistyczna ma własny opis i&nbsp;własny język. Klient trafia od razu do swojej sytuacji, nie do ogólnego cennika."),
            ("Wyciszony ton przy usługach trudnych", "Bez wykrzykników i&nbsp;sprzedażowego entuzjazmu tam, gdzie byłby nie na miejscu. Konkret, dyskrecja, telefon."),
            ("Treść pod zapytania długiego ogona", "„Sprzątanie po zbieractwie”, „ozonowanie mieszkania” — to są frazy o&nbsp;małym wolumenie, ale bardzo wysokiej intencji zakupowej."),
            ("Szybkie ładowanie", "Bez zbędnych bibliotek. Ktoś w&nbsp;sytuacji kryzysowej nie czeka na animacje."),
        ],
        design="Czysta struktura, wyraźna hierarchia, duży kontrast. Estetyka jest tu drugorzędna — pierwszorzędne jest to, żeby w&nbsp;piętnaście sekund dało się znaleźć właściwą usługę i&nbsp;numer telefonu.",
        dlaczego=[
            "Cała strona to jeden dokument, a menu to kotwice do sekcji. Nie ma podstron, bo nie ma po co ich klikać. Klient tej firmy przychodzi z jedną sprawą — zalane mieszkanie, remont do posprzątania, pluskwy — i chce dojść do numeru telefonu bez przeładowania strony. Numer stoi w nagłówku od pierwszej sekundy.",
            "Ramą całej strony jest jedna osoba. Na pierwszym ekranie stoi „Jedna osoba — Ty znasz mnie z imienia”, a w sekcji „Dlaczego warto zadzwonić” — „Jedna osoba — zawsze ta sama”. To była decyzja, nie skromność. Firma jednoosobowa może udawać dużą i wtedy przegrywa na każdym punkcie, którego nie ma. Może też zrobić z tego argument: dzwonisz do konkretnego człowieka, ten sam człowiek przyjeżdża i sprząta.",
            "W menu jest „Cennik”, a na stronie nie ma żadnych kwot ani widełek. Odradziłem je: przy sprzątaniu po zbieractwie czy po zalaniu wycena zależy od tego, co zastanie się na miejscu, a kwota z internetu, której potem nie da się dotrzymać, kosztuje więcej niż jej brak. Zamiast cen strona powtarza zasadę — „Wycenę podaję dopiero po oględzinach miejsca pracy”. Nie ma też opinii klientów ani galerii „przed i po”; przy części tych zleceń nie wypada o nie prosić.",
            "PageSpeed z dnia pomiaru: 99 na komputerze, 77 na komórce. To nie jest dowód na sprzedaż, tylko informacja, ile strona każe czekać. Przy usługach takich jak sprzątanie po zalaniu czy po zgonie ma to znaczenie — to sytuacje, których nikt nie planował. 77 nie jest wynikiem idealnym i tego nie ukrywam.",
        ],
        tagi=["Usługi", "Marketing", "Konwersja", "SEO"],
    ),
    dict(
        slug="strona-dla-firmy-klimatyzacyjnej",
        klient="Alaska",
        branza="Klimatyzacja i&nbsp;chłodnictwo",
        miasto="Racibórz",
        domena="alaskarp.pl",
        miniatura="alaska-thumb.webp",
        tytul="Strona dla firmy klimatyzacyjnej — Alaska",
        opisMeta="Strona dla firmy klimatyzacyjnej i chłodniczej z Raciborza działającej od 1997 roku. Animowane wejście, blog, panel realizacji. Zobacz, jak powstała.",
        h1="Strona dla firmy klimatyzacyjnej",
        lead="Montaż i&nbsp;serwis klimatyzacji oraz chłodnictwo przemysłowe. Firma z&nbsp;Raciborza działająca od 1997 roku — z&nbsp;dorobkiem, którego wcześniej nie było widać w&nbsp;internecie.",
        wyzwanie=[
            "Firma z&nbsp;takim stażem ma coś, czego nowe podmioty nie kupią za żadne pieniądze: <strong>blisko trzydzieści lat realizacji</strong>. Problem w&nbsp;tym, że w&nbsp;internecie wyglądała jak każda inna.",
            "Druga rzecz: klimatyzacja to dwa różne rynki naraz. Osoba montująca split w&nbsp;salonie i&nbsp;zakład potrzebujący chłodni to inni klienci z&nbsp;innymi pytaniami.",
        ],
        zbudowane=[
            ("Animowane wejście", "Krótka sekwencja otwierająca, która buduje wrażenie firmy technologicznej, a&nbsp;nie zakładu usługowego z&nbsp;lat dziewięćdziesiątych."),
            ("Rozdzielenie oferty", "Klimatyzacja dla domu i&nbsp;chłodnictwo przemysłowe jako osobne ścieżki, każda z&nbsp;własnym językiem i&nbsp;własnymi frazami."),
            ("Panel do dodawania realizacji", "Właściciel sam wrzuca zdjęcia z&nbsp;montaży, bez dzwonienia do wykonawcy strony. Portfolio rośnie samo."),
            ("Blog techniczny", "Odpowiedzi na pytania, które klienci i&nbsp;tak zadają przy wycenie — a&nbsp;przy okazji materiał dla wyszukiwarki."),
            ("Optymalizacja wydajności", "WebP, leniwe ładowanie obrazów i&nbsp;dzielenie kodu. Strona z&nbsp;animacjami nie musi być ciężka."),
        ],
        design="Chłodna paleta błękitów, mocne zdjęcia urządzeń, duże liczby przy stażu firmy. Wszystko podporządkowane jednemu przekazowi: to nie jest firma założona w&nbsp;zeszłym roku.",
        dlaczego=[
            "Strona główna jest jedna i mieści wszystko w sekcjach: firma, oferta, salon, pytania, kontakt. Nie rozbiłem sześciu usług na sześć podstron, bo klient tej firmy nie przegląda menu — szuka w upał albo przy awarii lady chłodniczej. Osobne adresy dostały tylko realizacje i blog.",
            "Dwa numery telefonu są rozdzielone celowo: serwis i właściciel osobno, salon sprzedaży osobno. Kto dzwoni z awarią, nie trafia do sprzedawcy klimatyzatorów. Przy adresie salonu dopisałem punkt orientacyjny — „1 Maja 4, przy SP Orlen”.",
            "Cennika nie ma i to była moja rekomendacja. Koszt montażu zależy od typu urządzenia, liczby jednostek i warunków technicznych — kwota podana z góry byłaby albo zawyżona na zapas, albo do odwołania przy pierwszej wizycie. Zamiast niej w pytaniach stoi wprost, od czego ta cena zależy, i że wycena u klienta jest bezpłatna. Wolę stronę, która czegoś nie obiecuje, niż taką, która się z obietnicy wycofuje.",
            "Pomiar PageSpeed z dnia sprawdzenia: 96 na komputerze, 67 na komórce. Ten niższy wynik to cena za animowane wejście i duże zdjęcia urządzeń — zapłacona świadomie. Gdyby to była strona pogotowia, wyciąłbym animację bez wahania. Numer telefonu siedzi w górnym pasku, nie tylko na dole w kontakcie.",
        ],
        tagi=["Klimatyzacja", "Animacje", "Panel klienta", "Blog"],
    ),
    dict(
        slug="strona-dla-przychodni",
        klient="Life-Centrum",
        branza="Placówka medyczna",
        miasto="Racibórz",
        domena="life-centrum.pl",
        # Projekt w toku: pod life-centrum.pl stoi jeszcze stary WordPress,
        # nasza wersja nie jest wdrozona. Bez tej flagi strona obiecywalaby
        # „zobacz na zywo” i prowadzila na cudza prace — a oferta obok mowi
        # „strony pisane od zera, bez kilkunastu wtyczek”.
        wRealizacji=True,
        miniatura="life-centrum-thumb.webp",
        tytul="Strona dla przychodni — Life-Centrum",
        opisMeta="Strona dla centrum zdrowia w Raciborzu: usługi medyczne, punkt pobrań, lekarze specjaliści. Zobacz, jak powstała.",
        h1="Strona dla placówki medycznej",
        lead="Centrum zdrowia w&nbsp;Raciborzu: lekarze specjaliści, punkt pobrań krwi, usługi pielęgniarskie. Placówka, do której trafia się w&nbsp;konkretnej sprawie i&nbsp;chce się szybko wiedzieć, czy to właściwe miejsce.",
        wyzwanie=[
            "Pacjent nie przegląda strony przychodni dla przyjemności. Ma pytanie — <strong>czy przyjmuje tu ortopeda, o&nbsp;której otwierają punkt pobrań, czy trzeba być na czczo</strong> — i&nbsp;chce odpowiedzi w&nbsp;kilkanaście sekund.",
            "Strona medyczna ma też inny ciężar niż zwykła firmowa: musi budzić zaufanie, nie sprzedawać. Każdy element sprzedażowy działa tu przeciwko sobie.",
        ],
        zbudowane=[
            ("Architektura informacji wokół pytań pacjenta", "Nie wokół struktury organizacyjnej placówki. Punkt wejścia to potrzeba, nie dział."),
            ("Sekcja punktu pobrań z&nbsp;zasadami przygotowania", "Najczęściej zadawane pytanie w&nbsp;każdej placówce z&nbsp;laboratorium — odpowiedź jest na stronie, nie w&nbsp;słuchawce."),
            ("Prezentacja specjalistów", "Twarz i&nbsp;specjalizacja. W&nbsp;medycynie zaufanie buduje konkretna osoba, nie logo."),
            ("Spokojna, czytelna typografia", "Duży stopień pisma, wysoki kontrast, dużo światła. Część pacjentów to osoby starsze."),
            ("Dane strukturalne placówki medycznej", "Godziny, adres i&nbsp;zakres usług podane w&nbsp;formie, którą Google rozumie i&nbsp;pokazuje w&nbsp;wynikach."),
        ],
        design="Biel, błękit i&nbsp;dużo przestrzeni. Świadomie bez efektów — w&nbsp;tej branży „wow” jest podejrzane, a&nbsp;spokój wiarygodny.",
        dlaczego=[
            "Zaznaczam od razu: pod tym adresem stoi jeszcze poprzednia strona centrum, moja wersja nie jest wdrożona. Piszę więc o decyzjach, nie o efekcie na żywo. Pierwsza dotyczyła układu. Dotychczasowa strona rozkłada się na specjalizacje — neurologia, logopedia, psychologia, dietetyka, każda osobno w menu. Pacjent nie myśli nazwami działów, tylko sprawą, z którą przychodzi. Ułożyłem stronę wokół tej sprawy, a nazwy specjalizacji zostawiłem jako drugą warstwę.",
            "Punkt pobrań dostał osobne miejsce, bo ma osobne godziny: działa krócej niż reszta centrum. Ktoś, kto zobaczy godziny placówki i przyjedzie po południu, przyjedzie na nic. Dołożyłem do tego zasady przygotowania do badania.",
            "Nie zrobiłem rejestracji online i to była decyzja, nie zaniechanie. Na stronie stoją dwa numery telefonu i nie ma żadnego systemu rezerwacji terminów. Formularz rezerwacji, którego nikt nie obsługuje w trakcie dyżuru, jest gorszy niż widoczny numer, bo obiecuje termin, którego nie potwierdza. Odpuściłem też animacje i efekty. W medycynie strona ma uspokajać, a nie robić wrażenie.",
            "Nie mam wyniku PageSpeed do pokazania i nie podstawię pod niego cudzej pracy. Pomiar zrobię, kiedy moja wersja stanie pod adresem. Szybkość znaczy tu zresztą co innego niż w sklepie: nikt nie porzuca koszyka, ale ktoś sprawdza godziny punktu pobrań na telefonie, w biegu.",
        ],
        tagi=["Medycyna", "UX", "Dostępność", "SEO"],
    ),
    dict(
        slug="strona-dla-transportu-medycznego",
        klient="Life-Ratownictwo",
        branza="Transport medyczny",
        miasto="Racibórz",
        domena="life-ratownictwo.pl",
        miniatura="life-ratownictwo-thumb.webp",
        tytul="Strona dla transportu medycznego",
        opisMeta="Strona dla firmy transportu medycznego i zabezpieczeń imprez: prywatna karetka, transport międzynarodowy, obsługa wydarzeń. Zobacz, jak powstała.",
        h1="Strona dla firmy transportu medycznego",
        lead="Prywatna karetka, transport międzynarodowy pacjentów i&nbsp;zabezpieczenie medyczne imprez masowych. Trzy usługi, trzech zupełnie różnych odbiorców.",
        wyzwanie=[
            "Na tę stronę trafiają ludzie w&nbsp;skrajnie różnych sytuacjach. <strong>Rodzina szukająca transportu dla chorego krewnego</strong> i <strong>organizator festynu, który musi mieć zabezpieczenie medyczne</strong>, nie potrzebują tych samych informacji.",
            "Pierwszy dzwoni pod wpływem stresu i&nbsp;chce wiedzieć, czy da się dziś. Drugi porównuje oferty i&nbsp;potrzebuje zakresu, uprawnień i&nbsp;konkretów do przetargu.",
        ],
        zbudowane=[
            ("Rozdzielenie ścieżek od pierwszego ekranu", "Transport pacjenta i&nbsp;zabezpieczenie wydarzeń jako dwie osobne drogi. Nikt nie musi czytać nie swojej sekcji."),
            ("Konkret zamiast ogólników przy zabezpieczeniach", "Rodzaje zespołów, wyposażenie, zakres — to, czego szuka organizator wypełniający dokumentację."),
            ("Prosty, spokojny język przy transporcie", "Bez żargonu medycznego. Osoba w&nbsp;stresie ma zrozumieć od pierwszego czytania."),
            ("Telefon dostępny z&nbsp;każdego miejsca", "W tej branży kontakt telefoniczny wygrywa z&nbsp;formularzem i&nbsp;strona to odzwierciedla."),
            ("Galeria z&nbsp;prawdziwych zabezpieczeń", "Zdjęcia z&nbsp;realnych wydarzeń zamiast zdjęć stockowych karetek."),
        ],
        design="Czerwień i&nbsp;granat, mocne zdjęcia, wyraźna hierarchia. Powaga bez straszenia — to usługa, przy której estetyka ma schodzić na drugi plan wobec czytelności.",
        dlaczego=[
            "Na pierwszym ekranie stoją dwa numery telefonu i przycisk „Zadzwoń teraz\", a numer jedzie z użytkownikiem w pływającym guziku przez całą długość strony. Formularza kontaktowego na stronie głównej nie ma. Osoba szukająca transportu dla leżącego krewnego nie czeka na odpowiedź mailem. Drugi przycisk, „Wyceń transport\", obsługuje tych, którzy planują z wyprzedzeniem.",
            "Na stronie głównej nie ma mapy, nie ma FAQ ani pełnego cennika. Jest za to sekcja „Zgodność z prawem\": wpis do rejestru podmiotów leczniczych, normy ambulansów, uprawnienia ratowników. Leży poniżej usług — rodzinie pacjenta nie wchodzi w drogę, a organizator imprezy masowej znajduje tam dane, których potrzebuje do własnej dokumentacji, bez dzwonienia.",
            "Firma ma dziś transport, zabezpieczenia imprez, szkolenia, punkt pobrań i opiekę pielęgniarską. W sekcji usług transport stoi pierwszy, szkolenia niżej. Blog zbiera artykuły w kategoriach Transport medyczny, Prawo, Zabezpieczenia i Pierwsza pomoc — każdy tytuł to jedno pytanie wpisywane w wyszukiwarkę.",
            "Wynik PageSpeed — 90 na komórce, 99 na komputerze — to pomiar z jednego dnia i nie mówi nic o sprzedaży. Szybkość nie jest tu punktem w rankingu, tylko warunkiem, żeby numer zdążył się w ogóle pokazać.",
        ],
        tagi=["Ratownictwo", "Architektura informacji", "SEO"],
    ),
    dict(
        slug="aplikacja-do-wystawiania-faktur",
        klient="WystawFakture.eu",
        branza="Aplikacja SaaS",
        miasto=None,
        domena="wystawfakture.eu",
        miniatura="wystawfakture-thumb.webp",
        tytul="Aplikacja do faktur — WystawFakture.eu",
        opisMeta="Darmowy generator faktur online bez rejestracji: faktury VAT, proforma i korekty, gotowość na KSeF. Zobacz, jak powstała aplikacja.",
        h1="Aplikacja do wystawiania faktur",
        lead="Generator faktur działający w&nbsp;przeglądarce, bez zakładania konta. Faktury VAT, proformy i&nbsp;korekty, zgodne z&nbsp;polskimi przepisami i&nbsp;przygotowane na KSeF.",
        wyzwanie=[
            "Rynek programów do faktur jest zatłoczony, ale prawie każdy zaczyna od tego samego: <strong>załóż konto, potwierdź e-mail, wybierz plan</strong>. Dla kogoś, kto musi wystawić jedną fakturę, to bariera nie do przejścia.",
            "Druga trudność jest merytoryczna. Faktura to dokument regulowany — układ pól, sposób liczenia VAT i&nbsp;wymagane oznaczenia wynikają z&nbsp;przepisów, nie z&nbsp;upodobań projektanta.",
        ],
        zbudowane=[
            ("Wystawienie faktury bez rejestracji", "Wchodzisz, wypełniasz, pobierasz PDF. Konto jest opcją dla wracających, nie warunkiem wstępu."),
            ("Trzy typy dokumentów", "Faktura VAT, proforma i&nbsp;korekta — każda z&nbsp;własnymi regułami i&nbsp;własnym układem pól."),
            ("Liczenie zgodne z&nbsp;przepisami", "Stawki, kwoty i&nbsp;zaokrąglenia liczone po stronie aplikacji, żeby użytkownik nie musiał tego sprawdzać kalkulatorem."),
            ("Przygotowanie pod KSeF", "Struktura danych ułożona tak, żeby wejście obowiązkowego e-fakturowania nie wymagało przepisywania aplikacji od zera."),
            ("Panel klienta dla wracających", "Zapisani kontrahenci i&nbsp;historia dokumentów dla tych, którzy fakturują regularnie."),
        ],
        design="Interfejs narzędziowy, nie marketingowy. Formularz zajmuje środek ekranu, wszystko inne schodzi z&nbsp;drogi. Przy aplikacji użytkowej najlepszy design to ten, którego się nie zauważa.",
        dlaczego=[
            "Założyłem, że nikt nie szuka „generatora faktur” ot tak — trafia tu z wyszukiwarki, w środku roboty, z konkretnym pytaniem. Dlatego strona główna jest przedsionkiem, a samo narzędzie stoi pod osobnym adresem. Blog i FAQ odpowiadają na pytania, od których zaczyna się szukanie: faktura korygująca, faktura bez NIP, split payment, KSeF.",
            "Nie ma cennika, nie ma planów, nie ma ekranu rejestracji. Dane faktury zostają w przeglądarce i nie idą na serwer. To decyzja z ceną: bez kont nie powstaje baza użytkowników, nie ma listy adresów, nie ma odzyskania dokumentu po wyczyszczeniu przeglądarki.",
            "Ciężar aplikacji schowałem za przyciskiem. Po drugiej stronie jest podgląd dokumentu, baza kontrahentów, eksport do KSeF, tryb ciemny i skróty klawiszowe.",
            "Pomiar PageSpeed z dnia badania: 88 na komórce, 99 na komputerze. To nie jest dowód na sprzedaż — to informacja o tym, ile trwa dojście do formularza. Osiemdziesiąt osiem, nie sto — narzędzie, które liczy i składa dokument w przeglądarce, ma swój koszt.",
        ],
        tagi=["SaaS", "Aplikacja webowa", "Panel klienta", "PDF"],
    ),
    dict(
        slug="aplikacja-z-kalkulatorami",
        klient="9 Dom",
        branza="Aplikacja webowa",
        miasto=None,
        domena="9dom.pl",
        miniatura="9dom-thumb.webp",
        tytul="Aplikacja z kalkulatorami — 9 Dom",
        opisMeta="Aplikacja z kalkulatorami astrologii wedyjskiej i numerologii: kosmogram, astrokartografia, cykle czasu, panel użytkownika. Zobacz, jak powstała.",
        h1="Aplikacja webowa z&nbsp;kalkulatorami",
        lead="Kalkulatory astrologii wedyjskiej i&nbsp;numerologii: kosmogram, astrokartografia, cykle czasu, mapa życia. Obliczenia astronomiczne podane językiem, który da się zrozumieć bez przygotowania.",
        wyzwanie=[
            "To nie jest strona informacyjna, tylko <strong>zestaw narzędzi liczących</strong>. Każdy kalkulator wymaga własnej logiki, a&nbsp;wyniki muszą się zgadzać — błąd w&nbsp;obliczeniach kompromituje cały serwis.",
            "Druga trudność to próg wejścia. Dziedzina ma własne słownictwo, którego użytkownik z&nbsp;zewnątrz nie zna. Wynik obliczeń bez wyjaśnienia jest bezużyteczny.",
        ],
        zbudowane=[
            ("Zestaw powiązanych kalkulatorów", "Kosmogram, numerologia, astrokartografia i&nbsp;cykle czasu jako osobne narzędzia korzystające ze wspólnej podstawy obliczeniowej."),
            ("Wyjaśnienia w&nbsp;miejscu użycia", "Pojęcia tłumaczone tam, gdzie się pojawiają, a&nbsp;nie na osobnej stronie ze słownikiem. Użytkownik uczy się przy okazji korzystania."),
            ("Panel użytkownika", "Zapisane profile i&nbsp;wyniki, żeby nie wpisywać daty urodzenia przy każdej wizycie."),
            ("Rozbudowana część treściowa", "Horoskop roczny i&nbsp;materiały wyjaśniające — to one przyprowadzają ruch z&nbsp;wyszukiwarki do narzędzi."),
        ],
        design="Ciemna, nocna paleta ze złotem i&nbsp;szeryfowym krojem w&nbsp;nagłówkach. Temat jest poważny i&nbsp;wyraźnie zaznaczony w&nbsp;komunikacie: „nie przepowiadamy przyszłości”.",
        dlaczego=[
            "W menu 9 Dom nie ma „o nas” ani „oferty”. Każda z ośmiu pozycji — Ścieżka, Mapa Życia, Dla par, Rodzina, Mapy, Kosmogram, Numerologia, Horoskop 2026 — jest narzędziem, które coś liczy. Strona główna też niczego nie sprzedaje: układa sześć pytań, od „Kim jestem?” do „Co teraz?”. Tak zbudowałem tę nawigację, bo tutaj nikt nie wchodzi po nazwę techniki. Wchodzi z pytaniem i nie zna słownictwa, którym się na nie odpowiada.",
            "Nie postawiłem bramki przed wynikiem. Kosmogram liczy się bez konta i bez płatności; panel jest dla osób, które wracają, a nie przepustką. Zrezygnowałem też z horoskopów dla dwunastu znaków, choć to najprostsza droga po ruch z wyszukiwarki. Serwis liczy pozycje z zodiaku syderycznego i taka rubryka byłaby doklejona wbrew reszcie — w pytaniach i odpowiedziach przy horoskopie rocznym stoi to wprost.",
            "Pomiar szybkości z dnia sprawdzenia: 73 na komórce, 94 na komputerze. Aplikacja z ośmioma kalkulatorami, kalendarzami dat i wyszukiwaniem miejsc waży więcej niż strona z ofertą. Wygrała dokładność: pod kalkulatorem stoi sekcja „jak to liczymy”, bo w narzędziu liczącym rozbieżność z innym serwisem podważa cały wynik.",
            "Dla tej branży ten wynik znaczy co innego niż dla usługi lokalnej. Do warsztatu czy salonu ktoś wchodzi po numer telefonu i odchodzi po chwili — tam pierwsze sekundy są całym kontaktem. Tutaj użytkownik przyszedł wypełnić formularz z datą i miejscem urodzenia. Krytyczny jest moment po kliknięciu „oblicz”, a nie pierwsza sekunda. Punkty na komórce zostają jako dług do spłacenia.",
        ],
        tagi=["Aplikacja", "Kalkulatory", "Panel", "Treści"],
    ),
    dict(
        slug="serwis-tresciowy-z-narzedziem",
        klient="Karta Dnia",
        branza="Serwis treściowy",
        miasto=None,
        domena="karta-dnia.pl",
        miniatura="karta-dnia-thumb.webp",
        tytul="Serwis treściowy z narzędziem — Karta Dnia",
        opisMeta="Tarot online po polsku: karta dnia, rozkłady z interpretacją i znaczenia wszystkich 78 kart. Zobacz, jak powstał serwis.",
        h1="Serwis treściowy z&nbsp;narzędziem",
        lead="Rozkłady tarota z&nbsp;interpretacją i&nbsp;znaczenia wszystkich 78 kart, bez rejestracji. Serwis, w&nbsp;którym treść i&nbsp;narzędzie napędzają się nawzajem.",
        wyzwanie=[
            "Sam generator rozkładów nie wystarczy — <strong>nikt go nie znajdzie</strong>. Ruch w&nbsp;tej niszy przychodzi z&nbsp;zapytań o&nbsp;znaczenia poszczególnych kart, a&nbsp;nie z&nbsp;zapytania o&nbsp;narzędzie.",
            "Odwrotnie też nie zadziała: serwis z&nbsp;samymi opisami kart to jeden z&nbsp;tysiąca. Potrzebny był powód, żeby zostać dłużej niż na jedno przeczytanie.",
        ],
        zbudowane=[
            ("Deterministyczny silnik rozkładów", "Losowanie i&nbsp;interpretacja liczone po stronie aplikacji, spójnie i&nbsp;powtarzalnie — bez podpinania zewnętrznych usług."),
            ("Osobna strona dla każdej z&nbsp;78 kart", "Każda odpowiada na własne zapytanie w&nbsp;wyszukiwarce. To jest właściwy fundament ruchu w&nbsp;tej niszy."),
            ("Brak rejestracji", "Rozkład w&nbsp;minutę, bez konta i&nbsp;bez podawania adresu e-mail. Bariera wejścia zredukowana do zera."),
            ("Wyraźne postawienie sprawy", "„Tarot, który nie wróży — pomaga myśleć”. Deklaracja, która ustawia oczekiwania i&nbsp;odróżnia serwis od konkurencji."),
        ],
        design="Głęboka zieleń butelkowa, złote akcenty, ilustracje kart jako główny element wizualny. Estetyka rytuału, nie jarmarku.",
        dlaczego=[
            "W mapie strony jest ponad sto adresów: 78 stron pojedynczych kart, 12 znaków zodiaku, dwanaście tekstów w dziale Wiedza, do tego strona główna, rozkład i karta dnia. Każdy z nich może być pierwszym, jaki ktoś zobaczy, dlatego strona karty kończy się przejściem do poprzedniej i następnej oraz odnośnikiem do rozkładu. Treść nie jest dodatkiem do narzędzia, tylko drogą do niego.",
            "Nie ma kont, newslettera ani reklam — na rozkładzie stoi wprost „nie wymaga konta”. Dziennik odczytów zapisuje się wyłącznie w przeglądarce i strona mówi to wprost, razem z ceną tej decyzji: nie trafia na serwer, znika po wyczyszczeniu danych przeglądarki i nie zobaczysz go na innym urządzeniu. Wybrałem to świadomie: wejście bez bramki zamiast zbierania adresów. Zamiast konta został link — adres zapisanego rozkładu odtwarza dokładnie ten sam układ.",
            "Jedno tarcie zostawiłem celowo. Własne pytanie jest osobnym krokiem, przed wyborem układu i przed odsłonięciem kart — dodatkowy przystanek tuż przed efektem. Serwis stoi na zdaniu, które sam wypisuje na stronie rozkładu: „Pytanie jest tu najważniejsze — ważniejsze niż to, które karty wypadną”. Odradziłem też obiecywanie przyszłości; nagłówek strony głównej brzmi „Tarot, który nie wróży. Pomaga myśleć.”.",
            "Pomiar PageSpeed: 97 na komórce, 100 na komputerze — jeden pomiar z jednego dnia, nie dowód na cokolwiek poza szybkością. W serwisie treściowym liczy się on nie tylko na stronie głównej, bo wejściem może być każda z podstron.",
        ],
        tagi=["Serwis treściowy", "Narzędzie", "SEO", "Bez rejestracji"],
    ),
]

# ——— Kontrola długości ————————————————————————————————————————————————
# Google ucina tytuł ok. 60 znaków, opis ok. 155. Generator MUSI to
# wymuszać, bo inaczej limit istnieje wyłącznie w czyjejś pamięci —
# a tak właśnie powstało 20 stron ze ściętymi tytułami.

LIMIT_TYTUL = 60
LIMIT_OPIS = 155


def _widoczna_dlugosc(t):
    """Dlugosc tak, jak ja liczy wyszukiwarka: encja to JEDEN znak.

    Tytul jest jednoczesnie tekstem do wyswietlenia i wartoscia mierzona
    przez limit SEO. Bez tej normalizacji „&nbsp;" liczylo sie jako szesc
    znakow i strażnik odrzucal poprawny tytul (2026-09-01).
    """
    return len(re.sub(r'&[a-z]+;', ' ', t))


def sprawdz_dlugosc(tytul, opis, gdzie):
    if _widoczna_dlugosc(tytul) > LIMIT_TYTUL:
        raise ValueError(f'{gdzie}: tytul ma {_widoczna_dlugosc(tytul)} znakow, limit {LIMIT_TYTUL} -> {tytul}')
    if _widoczna_dlugosc(opis) > LIMIT_OPIS:
        raise ValueError(f'{gdzie}: opis ma {_widoczna_dlugosc(opis)} znakow, limit {LIMIT_OPIS}')


# ——— Szablon ————————————————————————————————————————————————————————

def naglowek_strony(r, stempel):
    url = f"{BAZA}/realizacje/{r['slug']}/"
    sprawdz_dlugosc(f'{r["tytul"]} | WebStudio47', r["opisMeta"], r["slug"])
    schema_dzielo = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": f"{r['klient']} — {mala_pierwsza(r['branza'])}",
        "headline": r["tytul"],
        "description": r["opisMeta"],
        "url": url,
        "image": f"{BAZA}/{r['miniatura']}",
        "genre": r["branza"],
        "inLanguage": "pl",
        "creator": {
            "@type": "ProfessionalService",
            "name": "WebStudio47",
            "@id": f"{BAZA}/#organizacja",
            "url": BAZA,
            "telephone": "+48602622840",
            "email": "kontakt@webstudio47.pl",
            "sameAs": [FB],
        },
        "about": {"@type": "Organization", "name": r["klient"], "url": f"https://{r['domena']}"},
        "keywords": ", ".join(r["tagi"]),
    }
    if r["miasto"]:
        schema_dzielo["locationCreated"] = {"@type": "Place", "name": r["miasto"]}

    schema_okruszki = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": f"{BAZA}/"},
            {"@type": "ListItem", "position": 2, "name": "Realizacje", "item": f"{BAZA}/portfolio.html"},
            {"@type": "ListItem", "position": 3, "name": r["klient"], "item": url},
        ],
    }

    return f'''<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bezp(r["tytul"])} | WebStudio47</title>
    <meta name="description" content="{bezp(r["opisMeta"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/png" href="/favicon.png">
    <meta name="theme-color" content="#0a0a0f">

    <!-- Font naglowkow rownolegle z arkuszem: bez tego H1 przemalowuje
         sie po podmianie fontu i LCP przesuwa sie o ~2 s (2026-09-01). -->
    <link rel="preload" href="/fonty/spacegrotesk-700-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonty/spacegrotesk-700-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
        <!-- CSS krytyczny wbudowany: usuwa jeden lot do serwera
         ze sciezki pierwszego malowania. Reszta arkusza dociaga sie
         bez blokowania renderowania. Sklada to tools/krytyczny-css.py
         — nie edytuj tego bloku recznie. -->
    <style id="krytyczny">@font-face{font-family:'Inter Fallback';src:local('Arial');size-adjust:107.09%;ascent-override:90.46%;descent-override:22.52%;line-gap-override:0.00%} @font-face {font-family:'Inter'; font-style:normal; font-weight:300; font-display:swap; src:url(/fonty/inter-300-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/inter-400-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/inter-400-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/inter-500-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/inter-500-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/inter-600-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/inter-600-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Inter'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/inter-700-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Inter'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/inter-700-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/spacegrotesk-400-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:400; font-display:swap; src:url(/fonty/spacegrotesk-400-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/spacegrotesk-500-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:500; font-display:swap; src:url(/fonty/spacegrotesk-500-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/spacegrotesk-600-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:600; font-display:swap; src:url(/fonty/spacegrotesk-600-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/spacegrotesk-700-latin-ext.woff2) format('woff2'); unicode-range:U+0100-017F} @font-face {font-family:'Space Grotesk'; font-style:normal; font-weight:700; font-display:swap; src:url(/fonty/spacegrotesk-700-latin.woff2) format('woff2'); unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}:root{--bg-primary:#0a0a0f;--bg-secondary:#12121a;--accent-purple:#8b5cf6;--accent-cyan:#06b6d4;--text-primary:#ffffff;--text-secondary:#a1a1aa;--text-muted:#8a8a93;--glass-bg:rgba(255, 255, 255, 0.03);--glass-border:rgba(255, 255, 255, 0.1);--grad-primary:linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));--grad-surface:linear-gradient(180deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 100%);--section-pady:60px;--header-height:80px;--border-radius:16px;--transition:all 0.3s cubic-bezier(0.4, 0, 0.2, 1)}*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}html{scroll-behavior:smooth}body{background-color:var(--bg-primary);color:var(--text-primary);font-family:Inter,'Inter Fallback',sans-serif;line-height:1.6;overflow-x:hidden}.font-special,h1,h2,h3,h4{font-family:'Space Grotesk','Space Grotesk Fallback',sans-serif;font-weight:700}.container{max-width:1200px;margin:0 auto;padding:0 24px}section{padding:var(--section-pady) 0;position:relative}.text-gradient{background:linear-gradient(135deg,var(--accent-purple),var(--accent-cyan),var(--accent-purple));background-size:200% 200%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:inline-block;animation:gradientPulse 4s ease-in-out infinite}.glass{background:var(--glass-bg);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--glass-border);border-radius:var(--border-radius)}.btn{display:inline-flex;align-items:center;padding:12px 24px;border-radius:100px;font-weight:600;text-decoration:none;transition:var(--transition);cursor:pointer;border:none}.btn-primary{background:var(--grad-primary);color:#fff;box-shadow:0 4px 15px rgba(124,58,237,.3)}.btn-outline{border:1px solid var(--glass-border);color:var(--text-primary);background:0 0}header{position:fixed;top:24px;left:50%;transform:translateX(-50%);width:min(95%,1100px);z-index:1000;height:auto;padding:16px 0;display:flex;align-items:center;border-radius:50px;transition:all .5s cubic-bezier(.4, 0, .2, 1)}.nav-container{display:flex;justify-content:space-between;align-items:center;width:100%;padding:0 40px;transition:all .5s ease}.nav-spacer{flex-grow:1;transition:flex-grow .5s ease}.logo{font-size:1.6rem;color:var(--text-primary);text-decoration:none;letter-spacing:-1px;transition:all .5s ease}.logo span{color:var(--accent-cyan)}.nav-links{display:flex;list-style:none;gap:32px;align-items:center}.nav-links a{color:var(--text-secondary);text-decoration:none;font-size:1.05rem;font-weight:500;transition:var(--transition);text-shadow:0 0 10px rgba(255,255,255,0)}.hero{min-height:100vh;display:flex;align-items:center;padding-top:calc(var(--header-height) + 40px);overflow:hidden}.hero-bg{position:absolute;top:0;left:0;width:100%;height:100%;z-index:-1;background:radial-gradient(circle at 70% 30%,rgba(124,58,237,.15),transparent 40%),radial-gradient(circle at 30% 70%,rgba(6,182,212,.15),transparent 40%)}.hero-content{max-width:800px}.hero h1{font-size:clamp(2.8rem, 5.5vw, 4rem);line-height:1.15;margin-bottom:20px;letter-spacing:-1px}.text-white{color:#fff}.text-gradient-alt{background:linear-gradient(135deg,var(--accent-cyan),#3b82f6,#8b5cf6);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;transition:background-position .8s ease}.shimmer{position:relative;background:linear-gradient(to right,var(--accent-purple) 0,var(--accent-cyan) 25%,#fff 50%,var(--accent-cyan) 75%,var(--accent-purple) 100%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer-swipe 8s linear infinite}.hero h1{transition:var(--transition)}.hero p{font-size:1.25rem;color:var(--text-secondary);margin-bottom:40px;max-width:600px}.hero-btns{display:flex;gap:16px}.delay-1{transition-delay:0.2s}.delay-2{transition-delay:0.4s}.delay-3{transition-delay:0.6s}.scroll-indicator{position:absolute;bottom:30px;left:50%;transform:translateX(-50%)}.mouse{width:26px;height:42px;border:2px solid var(--text-muted);border-radius:20px;position:relative}.menu-toggle{display:none;flex-direction:column;gap:6px;cursor:pointer;background:0 0;border:none;padding:8px;border-radius:8px;transition:var(--transition)}.menu-toggle span{display:block;width:26px;height:2px;background:var(--text-primary);border-radius:2px;transition:var(--transition)}.reveal{opacity:0;transform:translateY(40px);transition:all .8s cubic-bezier(.4, 0, .2, 1)}.reveal.active{opacity:1;transform:translateY(0)}@media (max-width:768px){.menu-toggle{display:flex}.nav-links{display:flex!important;position:absolute;top:calc(100% + 10px);left:0;width:100%;background:rgba(10,10,15,.95);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--glass-border);border-radius:24px;flex-direction:column;padding:30px;align-items:center;gap:20px;opacity:0;visibility:hidden;transform:translateY(-20px);transition:all .3s ease;z-index:999}.nav-links.active{opacity:1;visibility:visible;transform:translateY(0)}.hero h1{font-size:3rem}.hero-btns{flex-direction:column}.stats-grid{grid-template-columns:1fr}.section-header h2{font-size:2rem}.menu-toggle.open span:first-child{transform:rotate(45deg) translate(5px,6px)}.menu-toggle.open span:nth-child(2){opacity:0}.menu-toggle.open span:last-child{transform:rotate(-45deg) translate(5px,-6px)}}html{scrollbar-width:thin;scrollbar-color:var(--accent-purple) var(--bg-primary)}.floating-phone-btn{display:none;position:fixed;bottom:90px;right:30px;width:50px;height:50px;border-radius:50%;z-index:9999;align-items:center;justify-content:center;background:var(--bg-secondary);text-decoration:none;transition:opacity .4s ease,transform .4s ease}.floating-phone-btn svg{width:22px;height:22px}@media (max-width:768px){.floating-phone-btn{display:flex;bottom:80px;right:20px;width:44px;height:44px}.floating-phone-btn svg{width:20px;height:20px}}.scroll-top-btn{position:fixed;bottom:30px;right:30px;width:50px;height:50px;border-radius:50%;border:none;cursor:pointer;z-index:9999;display:flex;align-items:center;justify-content:center;background:var(--bg-secondary);opacity:0;visibility:hidden;transform:translateY(20px);transition:opacity .4s ease,visibility .4s ease,transform .4s ease}.scroll-top-btn svg{width:22px;height:22px;fill:none;stroke:url(#arrow-grad);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:transform .3s ease}@media (max-width:768px){:root{--section-pady:60px}header{width:95%!important}header.scrolled{width:90%!important}.nav-links{display:none}.nav-links.active{display:flex!important}.menu-toggle{display:flex!important}.nav-container{padding:0 20px}.hero{padding-top:calc(var(--header-height) + 20px)}.hero h1{font-size:clamp(2rem, 6vw, 2.8rem)}.hero p{font-size:.95rem}.hero-btns{flex-direction:column;gap:12px}.hero-btns .btn{width:100%;text-align:center}.section-header h2{font-size:clamp(1.6rem, 5vw, 2.2rem)}.section-header{margin-bottom:40px}.stats-grid{grid-template-columns:1fr;gap:16px}.stat-number{font-size:2.5rem}.services-grid{grid-template-columns:1fr}.service-card{padding:28px}.portfolio-grid{grid-template-columns:1fr;gap:24px}.process-steps{grid-template-columns:1fr 1fr;gap:24px}.needs-grid{grid-template-columns:1fr}.why-grid{grid-template-columns:1fr}.contact-cta{padding:40px 24px}.phone-cta{padding:20px 24px;gap:16px}.phone-digits{font-size:1.4rem}.contact-secondary{flex-direction:column;gap:16px;align-items:center}.footer-grid{grid-template-columns:1fr;gap:32px;text-align:center}.footer-tagline{max-width:none}.footer-bottom{flex-direction:column;gap:8px;text-align:center}.scroll-top-btn{bottom:20px;right:20px;width:44px;height:44px}}@media (max-width:480px){:root{--section-pady:48px}.container{padding:0 16px}.hero h1{font-size:1.8rem;letter-spacing:-.5px}.hero p{font-size:.9rem}.section-header h2{font-size:1.5rem}.stats-grid{grid-template-columns:1fr;gap:16px}.stat-number{font-size:2.2rem}.process-steps{grid-template-columns:1fr}.step-num{font-size:3rem}.project-img{height:200px}.need-item{padding:24px}.phone-cta{flex-direction:column;text-align:center}.phone-number{align-items:center}.phone-digits{font-size:1.6rem}.tech-track span:not(.tech-sep){font-size:1.1rem;padding:4px 8px}}@media (max-width:768px){.hero{align-items:flex-start!important;padding-top:calc(var(--header-height) + 30px)!important;min-height:85vh!important}.hero-content{margin-top:.5rem}.hero h1{font-size:clamp(2rem, 7vw, 2.9rem)!important}}.reveal-hero{animation:hero-wjazd .7s cubic-bezier(.4,0,.2,1) both}.reveal-hero.delay-1{animation-delay:.15s}.reveal-hero.delay-2{animation-delay:.3s}.reveal-hero.delay-3{animation-delay:.45s}@media (prefers-reduced-motion:reduce){.reveal-hero{animation:none}}

@media (prefers-reduced-motion: reduce) {

    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }

    .reveal {
        opacity: 1;
        transform: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    .info-card::before,
    .info-card::after {
        transition: none;
    }
}

@media (min-width: 1281px) {
    .nav-links {
        gap: 26px;
    }

    .nav-links a {
        font-size: 1rem;
    }
}

@media (max-width: 1280px) {
    .menu-toggle {
        display: flex;
    }

    .nav-links {
        display: flex !important;
        position: absolute;
        top: calc(100% + 10px);
        left: 0;
        width: 100%;
        background: rgba(10, 10, 15, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        flex-direction: column;
        padding: 30px;
        align-items: center;
        gap: 20px;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-20px);
        transition: all 0.3s ease;
        z-index: 999;
    }

    .nav-links.active {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }

    /* Hamburger — animacja krzyżyka */
    .menu-toggle.open span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 6px);
    }

    .menu-toggle.open span:nth-child(2) {
        opacity: 0;
    }

    .menu-toggle.open span:nth-last-child(1) {
        transform: rotate(-45deg) translate(5px, -6px);
    }
}

@media (prefers-reduced-motion: reduce) {
    .faq-item::details-content { transition: none; }
    /* lagodniej, nie zero: samo przenikanie, bez ruchu w pionie */
    .form-status { transition: opacity 250ms ease-out; transform: none; }
}

@media (prefers-reduced-motion: reduce) {
    .karuzela-tor { scroll-behavior: auto; }
    .blog-karta:hover .blog-karta-obraz img { transform: none; }
    .karuzela-kropka,
    .karuzela-kropka::before { transition: none; }
}

/* ---- Animacje ozdobne nad zagieciem: skonczona liczba przebiegow -------
   Speed Index mierzy, jak dlugo WIDOCZNY obszar sie zmienia. Nieskonczona
   animacja w hero sprawia, ze strona nigdy nie jest wizualnie gotowa,
   a zaden pozniejszy fragment nie ma juz szans tego odrobic.

   Zmierzone 2026-09-01 na komputerze: FCP 0,2 s i LCP 0,8 s (oceny 1,00
   i 0,97), a mimo to wydajnosc 81 — bo Speed Index wyszedl 6,6 s z ocena
   ZERO. Winne byly puls gradientu i polysk na naglowku hero, chodzace
   w kolko od pierwszej klatki.

   Zostaja jako efekt WEJSCIA: gradient przechodzi dwa razy, polysk raz
   i obraz sie uspokaja. Naglowki sekcji nizej zachowuja puls bez zmian
   — sa pod zagieciem, wiec pomiaru nie dotykaja. */
.hero .text-gradient,
.hero .text-gradient-alt {
    animation-iteration-count: 2;
}

.hero .shimmer {
    animation-iteration-count: 1;
}@keyframes gradientPulse{0%,100%{background-position:0 50%}50%{background-position:100% 50%}}@keyframes shimmer-swipe{0%{background-position:-200% center}100%{background-position:200% center}}@keyframes hero-wjazd{from{transform:translateY(40px)}to{transform:translateY(0)}}</style>
    <link rel="preload" href="/style.css?v={stempel}" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="/style.css?v={stempel}"></noscript>

    <!-- Fonty self-hosted w style.css - patrz komentarz tamze -->

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:locale" content="pl_PL">
    <meta property="og:site_name" content="WebStudio47">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{bezp(r["tytul"])}">
    <meta property="og:description" content="{bezp(r["opisMeta"])}">
    <meta property="og:image" content="{BAZA}/{r["miniatura"]}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{bezp(r["tytul"])}">
    <meta name="twitter:description" content="{bezp(r["opisMeta"])}">
    <meta name="twitter:image" content="{BAZA}/{r["miniatura"]}">

    <!-- Zgoda na cookies (Google Consent Mode v2).
         MUSI byc przed gtag.js: inaczej GA4 zapisze dane, zanim ktokolwiek
         wyrazi zgode. Obsluge modala ma consent.js. -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}

        gtag('consent', 'default', {{
            ad_storage: 'denied',
            ad_user_data: 'denied',
            ad_personalization: 'denied',
            analytics_storage: 'denied',
            functionality_storage: 'denied',
            personalization_storage: 'denied',
            security_storage: 'granted',
            wait_for_update: 500
        }});

        try {{
            var wybor = JSON.parse(localStorage.getItem('cookieConsent') || 'null');
            if (wybor) {{
                gtag('consent', 'update', {{
                    analytics_storage: wybor.analytics ? 'granted' : 'denied',
                    functionality_storage: wybor.functional ? 'granted' : 'denied',
                    personalization_storage: wybor.functional ? 'granted' : 'denied'
                }});
            }}
        }} catch (e) {{ }}
    </script>

    <!-- Google Analytics (GA4) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-NV6W571RJB"></script>
    <script>
        gtag('js', new Date());
        gtag('config', 'G-NV6W571RJB', {{ anonymize_ip: true }});
    </script>

    <!-- Dane strukturalne: realizacja -->
    <script type="application/ld+json">
{json.dumps(schema_dzielo, ensure_ascii=False, indent=2)}
    </script>

    <!-- Dane strukturalne: okruszki -->
    <script type="application/ld+json">
{json.dumps(schema_okruszki, ensure_ascii=False, indent=2)}
    </script>
</head>
'''


NAWIGACJA = '''
<body>

    <!-- Header / Nav -->
    <header id="main-header">
        <div class="container nav-container">
            <a href="/" class="logo font-special">&lt;WebStudio<span>47</span>&gt;</a>
            <div class="nav-spacer"></div>
            <nav>
                <ul class="nav-links">
                    <li><a href="/tworzenie-stron-internetowych-raciborz/">Strony&nbsp;WWW</a></li>
                    <li><a href="/pozycjonowanie-stron-raciborz/">Pozycjonowanie</a></li>
                    <li><a href="/portfolio.html" class="active" aria-current="page">Realizacje</a></li>
                    <li><a href="/cennik/">Cennik</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/kontakt/">Kontakt</a></li>
                    <li><a href="tel:+48602622840" class="btn btn-primary btn-sm">602 622 840</a></li>
                </ul>
                <button class="menu-toggle" id="mobile-menu" aria-label="Menu nawigacyjne" aria-expanded="false">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </nav>
        </div>
    </header>
'''


def stopka(stempel):
    return f'''
    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div class="footer-logo font-special">&lt;WebStudio<span>47</span>&gt;</div>
                    <p class="footer-tagline">Strony internetowe dla firm, które traktują swój biznes poważnie. Nie
                        robię stron dla każdego — i&nbsp;właśnie dlatego te, które robię, wyglądają tak, jak wyglądają.</p>
                </div>
                <div class="footer-nav">
                    <p class="footer-heading">Oferta</p>
                    <ul>
                        <li><a href="/tworzenie-stron-internetowych-raciborz/">Strony internetowe</a></li>
                        <li><a href="/pozycjonowanie-stron-raciborz/">Pozycjonowanie</a></li>
                        <li><a href="/cennik/">Cennik</a></li>
                        <li><a href="/portfolio.html">Realizacje</a></li>
                        <li><a href="/blog/">Blog</a></li>
                        <li><a href="/kontakt/">Kontakt</a></li>
                    </ul>
                </div>
                <div class="footer-contact-info">
                    <p class="footer-heading">Kontakt</p>
                    <p><a href="tel:+48602622840">602 622 840</a></p>
                    <p><a href="mailto:kontakt@webstudio47.pl">kontakt@webstudio47.pl</a></p>
                    <p>Racibórz, Woj. Śląskie</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 WebStudio47. Projektowanie stron internetowych — Racibórz.</p>
                <p class="footer-note">Ograniczona liczba zleceń miesięcznie. Jakość ponad ilość.</p>
            </div>
        </div>
    </footer>

    <aside class="akcje-plywajace" aria-label="Szybkie akcje">
        <a href="tel:+48602622840" class="floating-phone-btn" id="floating-phone-btn" aria-label="Zadzwoń">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="phone-float-grad" x1="0%" y1="100%" x2="0%" y2="0%">
                        <stop offset="0%" stop-color="#7c3aed" />
                        <stop offset="100%" stop-color="#06b6d4" />
                    </linearGradient>
                </defs>
                <path
                    d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"
                    stroke="url(#phone-float-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                </path>
            </svg>
        </a>
        <button class="scroll-top-btn" id="scroll-top-btn" aria-label="Przewiń do góry">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="arrow-grad" x1="0%" y1="100%" x2="0%" y2="0%">
                        <stop offset="0%" stop-color="#7c3aed" />
                        <stop offset="100%" stop-color="#06b6d4" />
                    </linearGradient>
                </defs>
                <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
        </button>
    </aside>

    <script src="/script.js?v={stempel}" defer></script>
    <script src="/consent.js?v={stempel}" defer></script>
</body>

</html>
'''


def tresc(r, poprzednia, nastepna):
    wyzwanie = '\n'.join(f'                    <p>{x}</p>' for x in r["wyzwanie"])
    zbudowane = '\n'.join(
        f'''                    <div class="info-card glass reveal">
                        <h3>{bezp(t)}</h3>
                        <p>{o}</p>
                    </div>''' for t, o in r["zbudowane"])
    tagi = '\n'.join(f'                    <li>{bezp(t)}</li>' for t in r["tagi"])
    lokalizacja = f' · {r["miasto"]}' if r["miasto"] else ''

    # Realizacja w toku: nie obiecujemy „zobacz na zywo”, bo pod adresem
    # stoi jeszcze poprzednia strona klienta. Etykieta mowi wprost, na jakim
    # etapie jest projekt — to uczciwsze niz link, ktory prowadzi donikad,
    # i bezpieczniejsze niz zdjecie calej realizacji z portfolio.
    if r.get("wRealizacji"):
        przycisk_zywo = ('<span class="btn btn-primary" aria-disabled="true" '
                         'style="opacity:.65;cursor:default">Projekt w realizacji</span>')
        podpis_zrzutu = (f'{bezp(r["klient"])} — projekt w realizacji, '
                         f'strona nie jest jeszcze wdrożona')
    else:
        przycisk_zywo = (f'<a href="https://{r["domena"]}" target="_blank" '
                         f'rel="noopener" class="btn btn-primary">Zobacz stronę na żywo</a>')
        podpis_zrzutu = (f'{bezp(r["klient"])} — <a href="https://{r["domena"]}" '
                         f'target="_blank" rel="noopener">{r["domena"]}</a>')

    nawigacja_realizacji = ''
    if poprzednia or nastepna:
        czesci = []
        if poprzednia:
            czesci.append(f'<a href="/realizacje/{poprzednia["slug"]}/">&larr; {bezp(poprzednia["klient"])}</a>')
        czesci.append('<a href="/portfolio.html">Wszystkie realizacje</a>')
        if nastepna:
            czesci.append(f'<a href="/realizacje/{nastepna["slug"]}/">{bezp(nastepna["klient"])} &rarr;</a>')
        nawigacja_realizacji = f'''
        <section class="section-alt">
            <div class="container">
                <nav class="realizacje-nawigacja" aria-label="Inne realizacje">
                    {' '.join(czesci)}
                </nav>
            </div>
        </section>
'''

    return f'''
    <main>

        <!-- Hero -->
        <section class="page-hero">
            <div class="container">
                <nav class="breadcrumbs" aria-label="Okruszki">
                    <a href="/">Strona główna</a>
                    <span aria-hidden="true">›</span>
                    <a href="/portfolio.html">Realizacje</a>
                    <span aria-hidden="true">›</span>
                    <span>{bezp(r["klient"])}</span>
                </nav>
                <p class="realizacja-branza">{bezp(r["branza"])}{lokalizacja}</p>
                <h1 class="reveal-hero"><span class="text-white">{bezp(r["h1"])}</span><br>
                    <span class="text-gradient">{bezp(r["klient"])}</span></h1>
                <p class="page-hero-lead reveal-hero delay-1">{r["lead"]}</p>
                <div class="page-hero-btns reveal-hero delay-2">
                    {przycisk_zywo}
                    <a href="/kontakt/" class="btn btn-outline">Chcę podobną</a>
                </div>
            </div>
        </section>

        <!-- Zrzut -->
        <section style="padding-top:0">
            <div class="container">
                <figure class="realizacja-zrzut reveal">
                    <img src="/{r["miniatura"].replace("-thumb.", "-hero.")}" width="1600" height="900" loading="lazy" decoding="async"
                        alt="Strona internetowa {bezp(r["klient"])} — {bezp(mala_pierwsza(r["branza"]))}{bezp(lokalizacja)}">
                    <figcaption>{podpis_zrzutu}</figcaption>
                </figure>
            </div>
        </section>

        <!-- Wyzwanie -->
        <section class="section-alt">
            <div class="container">
                <div class="prose reveal">
                    <h2>Wyzwanie</h2>
{wyzwanie}
                </div>
            </div>
        </section>

        <!-- Co zbudowałem -->
        <section>
            <div class="container">
                <div class="section-header reveal">
                    <h2 class="text-gradient">Co zbudowałem</h2>
                </div>
                <div class="card-grid">
{zbudowane}
                </div>
            </div>
        </section>

        <!-- Design -->
        <section class="section-alt">
            <div class="container">
                <div class="prose reveal">
                    <h2>Kierunek wizualny</h2>
                    <p>{r["design"]}</p>
                    <h3>Zakres prac</h3>
                    <ul class="check-list">
{tagi}
                    </ul>
                </div>
            </div>
        </section>
{sekcja_dlaczego(r)}{pomiary.sekcja(r['klient'], r['domena'])}{nawigacja_realizacji}
        <!-- CTA -->
        <section>
            <div class="container">
                <div class="cta-band glass reveal">
                    <h2 class="text-gradient">Chcesz taką stronę dla siebie?</h2>
                    <p>Piętnaście minut rozmowy i wiesz, ile to kosztuje w Twoim przypadku i ile potrwa.
                        Widełki cenowe znajdziesz w&nbsp;<a href="/cennik/">cenniku</a>.</p>
                    <div class="cta-band-btns">
                        <a href="tel:+48602622840" class="btn btn-primary">Zadzwoń: 602 622 840</a>
                        <a href="/kontakt/" class="btn btn-outline">Opisz swój projekt</a>
                    </div>
                </div>
            </div>
        </section>

    </main>
'''


def main():
    import time
    stempel = int(time.time())
    kat = KATALOG / 'realizacje'
    kat.mkdir(exist_ok=True)

    for i, r in enumerate(REALIZACJE):
        poprzednia = REALIZACJE[i - 1] if i > 0 else None
        nastepna = REALIZACJE[i + 1] if i < len(REALIZACJE) - 1 else None
        strona = (naglowek_strony(r, stempel) + NAWIGACJA
                  + tresc(r, poprzednia, nastepna) + stopka(stempel))
        cel = kat / r['slug']
        cel.mkdir(exist_ok=True)
        (cel / 'index.html').write_text(strona, encoding='utf-8')
        print(f"  realizacje/{r['slug']}/  ({len(strona) // 1024} KB)")

    print(f"\nWygenerowano {len(REALIZACJE)} stron, stempel ?v={stempel}")


if __name__ == '__main__':
    main()
