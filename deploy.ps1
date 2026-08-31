# Deploy webstudio47.pl -> CyberFolks (WinSCP, FTP)
# Wzorowane na supek-irek-modern/deploy.ps1 i life-ratownictwo-web/deploy.ps1.
# Haslo pobierane W LOCIE z zapisanej sesji FileZilli (ntroixgelh@s75) - brak sekretow w repo.
#
# Uzycie:
#   powershell -ExecutionPolicy Bypass -File deploy.ps1 -Lista    # tylko pokaz, co poleci (nic nie wysyla)
#   powershell -ExecutionPolicy Bypass -File deploy.ps1           # wysylka
#   powershell -ExecutionPolicy Bypass -File deploy.ps1 -Sprzataj # usun sieroty z serwera (pyta o potwierdzenie)
#
# Serwis jest statyczny - nie ma builda. Zrodlem jest katalog repo.
# Wysylamy JAWNA LISTE plikow (nie `synchronize`), zeby nic zdalnie nie skasowac.

param(
  [switch]$Lista,
  [switch]$Sprzataj,
  [string]$Remote = '/domains/webstudio47.pl/public_html'
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

# --- Co wysylamy -------------------------------------------------------------
# Celowo POMIJAMY:
#   .git/          - repozytorium
#   apps-script/   - kod backendu formularza, nie ma czego szukac na serwerze
#   style.dev.css  - nieskompresowane zrodlo stylow (60 KB)
#   zdjecia/       - grafiki na Facebooka, nie sa uzywane przez strone

$Pliki = @(
  'index.html',
  'portfolio.html',
  'script.js',
  'style.css',
  'consent.js',
  'page-script.js',
  'page-style.css',
  'arc.js',
  'arc.css',
  'sitemap.xml',
  'robots.txt',
  '.htaccess'
)

$Katalogi = @(
  'blog',
  'realizacje',
  'cennik',
  'kontakt',
  'pozycjonowanie-stron-raciborz',
  'tworzenie-stron-internetowych-raciborz'
)

# Obrazy z katalogu glownego: miniatury realizacji, favicon, obrazek do
# udostepnien. Wczesniej ich tu nie bylo - dzialaly tylko dlatego, ze trafily
# na serwer recznie, przed powstaniem tego skryptu. Kazda nowa albo podmieniona
# miniatura nie zostalaby wyslana.
$Obrazy = @(Get-ChildItem -Path $PSScriptRoot -File |
            Where-Object { $_.Extension -in '.webp', '.png', '.jpg', '.svg', '.ico' } |
            Where-Object { $_.Name -ne 'favicon-original.png' } |
            ForEach-Object { $_.Name })

# --- Kontrola przed wysylka --------------------------------------------------

$brakujace = @()
foreach ($p in $Pliki)    { if (-not (Test-Path "$PSScriptRoot\$p")) { $brakujace += $p } }
foreach ($k in $Katalogi) { if (-not (Test-Path "$PSScriptRoot\$k")) { $brakujace += "$k\" } }
if ($brakujace.Count -gt 0) { throw "Brak w katalogu repo: $($brakujace -join ', ')" }

# Formularz bez podlaczonego backendu to najczestszy blad przy wdrozeniu.
$ps = Get-Content "$PSScriptRoot\page-script.js" -Raw
if ($ps -match 'WSTAW_TUTAJ_ID_WDROZENIA') {
  Write-Host "!! UWAGA: page-script.js nie ma jeszcze adresu Apps Script." -ForegroundColor Yellow
  Write-Host "   Formularz na /kontakt/ pokaze telefon zamiast wysylac wiadomosc." -ForegroundColor Yellow
  Write-Host "   Instrukcja: apps-script\README.md" -ForegroundColor Yellow
  Write-Host ""
}

# .htaccess kaze trzymac CSS i JS w cache przez ROK. Jesli zmienisz ktorys
# z tych plikow, a nie podbijesz "?v=" w HTML-ach, powracajacy odwiedzajacy
# dostana stara wersje - lacznie z formularzem bez adresu Apps Script.
# Kazdy zasob sprawdzamy w pliku HTML, ktory faktycznie go linkuje -
# blog-style.css wystepuje wylacznie w blog\, nie w index.html.
$doSprawdzenia = @(
  @{ Zasob = 'page-style.css';       Html = 'kontakt\index.html' },
  @{ Zasob = 'page-script.js';       Html = 'kontakt\index.html' },
  @{ Zasob = 'consent.js';           Html = 'index.html' },
  @{ Zasob = 'script.js';            Html = 'index.html' },
  @{ Zasob = 'style.css';             Html = 'index.html' },
  @{ Zasob = 'blog\blog-style.css';  Html = 'blog\index.html' },
  @{ Zasob = 'arc.css';              Html = 'portfolio.html' },
  @{ Zasob = 'arc.js';               Html = 'portfolio.html' }
)

foreach ($poz in $doSprawdzenia) {
  $nazwa = Split-Path $poz.Zasob -Leaf
  # "page-script.js" konczy sie na "script.js", wiec kotwiczymy poczatek nazwy
  $wzor = '(?<![-\w])' + [regex]::Escape($nazwa) + '\?v=(\d+)'

  $stempel = (Select-String -Path "$PSScriptRoot\$($poz.Html)" -Pattern $wzor `
                -AllMatches -ErrorAction SilentlyContinue |
              ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value } |
              Select-Object -First 1)
  if (-not $stempel) { continue }

  $plik = Get-Item "$PSScriptRoot\$($poz.Zasob)" -ErrorAction SilentlyContinue
  if (-not $plik) { continue }

  $czasStempla = [DateTimeOffset]::FromUnixTimeSeconds([int64]$stempel).LocalDateTime
  if ($plik.LastWriteTime -gt $czasStempla.AddMinutes(5)) {
    Write-Host "!! UWAGA: $($poz.Zasob) zmieniony po ostatnim podbiciu ?v=$stempel" -ForegroundColor Yellow
    Write-Host "   Powracajacy odwiedzajacy moga dostac stara wersje z cache." -ForegroundColor Yellow
    Write-Host "   Podbij ?v= we wszystkich plikach HTML przed wysylka." -ForegroundColor Yellow
    Write-Host ""
  }
}

if ($Lista) {
  Write-Host "Poleci na $Remote :" -ForegroundColor Cyan
  $Pliki | ForEach-Object { "  $_" }
  Write-Host "  --- obrazy ($($Obrazy.Count)) ---" -ForegroundColor DarkGray
  $Obrazy | ForEach-Object { "  $_" }
  $Katalogi | ForEach-Object {
    $n = (Get-ChildItem "$PSScriptRoot\$_" -Recurse -File).Count
    "  $_\  ($n plikow)"
  }
  Write-Host ""
  Write-Host "Pominiete: .git, apps-script\, style.dev.css, zdjecia\" -ForegroundColor DarkGray
  return
}

# --- Haslo z zapisanej sesji FileZilli ---------------------------------------

[xml]$r = Get-Content "$env:APPDATA\FileZilla\recentservers.xml"
$s = @($r.FileZilla3.RecentServers.Server | Where-Object {
  $_.Host -eq 's75.cyber-folks.pl' -and $_.User -eq 'ntroixgelh' -and $_.Pass.'#text'
})[0]
if (-not $s) { throw "Brak zapisanej sesji ntroixgelh@s75 w FileZilli" }
$pass  = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($s.Pass.'#text'))
$passQ = $pass -replace '"','""'

# --- Skrypt dla WinSCP -------------------------------------------------------

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add('option batch abort')
$lines.Add('option confirm off')
$lines.Add('open ftp://ntroixgelh@s75.cyber-folks.pl:21 -passive=on -password="' + $passQ + '"')
$lines.Add('cd "' + $Remote + '"')

# --- Tryb sprzatania ---------------------------------------------------------
# Zwykle wdrozenie nigdy nie kasuje. Ten tryb kasuje - i tylko to, co jest
# wypisane ponizej z nazwy. Sieroty po realizacjach usunietych z portfolio:
# nic do nich nie linkuje, ale leza publicznie dostepne na serwerze.
if ($Sprzataj) {
  $DoUsuniecia = @(
    'dr-kangur-thumb.webp',
    'dr-kangur-thumb.png',
    'foxy-thumb.webp',
    'foxy-thumb.png',
    'blog/img/hero-business.png',
    'blog/img/hero-comparison.png',
    'blog/img/hero-costs.png',
    'blog/img/hero-responsive.png',
    'blog/img/hero-seo.png',
    'blog/img/hero-wordpress.png'
  )

  Write-Host "TRYB SPRZATANIA - zostana TRWALE usuniete z $Remote :" -ForegroundColor Yellow
  $DoUsuniecia | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
  Write-Host ""
  $odp = Read-Host "Na pewno? Wpisz TAK, zeby potwierdzic"
  if ($odp -ne 'TAK') { Write-Host "Przerwane - nic nie usunieto." -ForegroundColor Cyan; return }

  # `rm` w WinSCP nie zna przelacznika -nofail. Brak pliku sygnalizujemy
  # przez opcje sesji: `failonnomatch off` sprawia, ze nietrafiony wzorzec
  # nie jest bledem, a `batch continue` nie przerywa calej listy na pierwszym.
  $lines.Insert(1, 'option failonnomatch off')
  $lines[0] = 'option batch continue'
  $DoUsuniecia | ForEach-Object { $lines.Add('rm "' + $Remote + '/' + $_ + '"') }
  $lines.Add('exit')

  $tmpS = "$env:TEMP\ws_sprzatanie_webstudio47.txt"
  Set-Content $tmpS $lines -Encoding ascii
  $logS = "$env:TEMP\ws_sprzatanie_webstudio47_out.txt"
  cmd /c "`"C:\Program Files (x86)\WinSCP\WinSCP.com`" /script=`"$tmpS`" /ini=nul > `"$logS`" 2>&1"
  $kodS = $LASTEXITCODE
  Get-Content $logS | Select-Object -Last 20
  Remove-Item $tmpS, $logS -Force
  if ($kodS -ne 0) { throw "WinSCP zakonczyl z kodem $kodS" }

  Write-Host ""
  Write-Host ">> Posprzatane. Sprawdz, czy adresy zwracaja teraz 404." -ForegroundColor Green
  return
}

foreach ($p in ($Pliki + $Obrazy)) {
  $lines.Add('put "' + "$PSScriptRoot\$p" + '" "' + $Remote + '/' + $p + '"')
}
foreach ($k in $Katalogi) {
  # Katalog podany BEZ gwiazdki i BEZ powtorzonej nazwy w celu:
  # "...\cennik" -> "$Remote/" laduje jako "$Remote/cennik".
  # Nieistniejacy katalog zostanie utworzony.
  # Swiadomie bez przelacznikow - `put` nie zna `-mirror`, a kazdy kolejny
  # przelacznik to ryzyko przerwania wysylki w polowie. Koszt: blog/ (3,8 MB
  # zdjec) leci od nowa przy kazdym wdrozeniu.
  $lines.Add('put "' + "$PSScriptRoot\$k" + '" "' + $Remote + '/"')
}
$lines.Add('exit')

$tmp = "$env:TEMP\ws_deploy_webstudio47.txt"
Set-Content $tmp $lines -Encoding ascii

Write-Host ">> Wysylka -> $Remote ..." -ForegroundColor Cyan
$log = "$env:TEMP\ws_deploy_webstudio47_out.txt"
cmd /c "`"C:\Program Files (x86)\WinSCP\WinSCP.com`" /script=`"$tmp`" /ini=nul > `"$log`" 2>&1"
$kod = $LASTEXITCODE
$out = Get-Content $log
Remove-Item $tmp, $log -Force

$out | Select-Object -Last 25
if ($kod -ne 0) { throw "WinSCP zakonczyl z kodem $kod" }

Write-Host ""
Write-Host ">> OK - https://webstudio47.pl zaktualizowane." -ForegroundColor Green
Write-Host "   Sprawdz: /cennik/  /kontakt/  /pozycjonowanie-stron-raciborz/" -ForegroundColor Green
Write-Host "   Pamietaj o zgloszeniu sitemapy w Search Console." -ForegroundColor Green
