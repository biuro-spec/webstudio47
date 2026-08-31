# Deploy webstudio47.pl -> CyberFolks (WinSCP, FTP)
# Wzorowane na supek-irek-modern/deploy.ps1 i life-ratownictwo-web/deploy.ps1.
# Haslo pobierane W LOCIE z zapisanej sesji FileZilli (ntroixgelh@s75) - brak sekretow w repo.
#
# Uzycie:
#   powershell -ExecutionPolicy Bypass -File deploy.ps1 -Lista    # tylko pokaz, co poleci (nic nie wysyla)
#   powershell -ExecutionPolicy Bypass -File deploy.ps1           # wysylka
#
# Serwis jest statyczny - nie ma builda. Zrodlem jest katalog repo.
# Wysylamy JAWNA LISTE plikow (nie `synchronize`), zeby nic zdalnie nie skasowac.

param(
  [switch]$Lista,
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
  'sitemap.xml',
  'robots.txt',
  '.htaccess'
)

$Katalogi = @(
  'blog',
  'cennik',
  'kontakt',
  'pozycjonowanie-stron-raciborz',
  'tworzenie-stron-internetowych-raciborz'
)

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
foreach ($zasob in @('page-style.css', 'page-script.js', 'script.js', 'consent.js')) {
  $stempel = (Select-String -Path "$PSScriptRoot\index.html", "$PSScriptRoot\kontakt\index.html" `
                -Pattern ([regex]::Escape($zasob) + '\?v=(\d+)') -AllMatches -ErrorAction SilentlyContinue |
              ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value } |
              Select-Object -First 1)
  if (-not $stempel) { continue }
  $plik = Get-Item "$PSScriptRoot\$zasob"
  $czasStempla = [DateTimeOffset]::FromUnixTimeSeconds([int64]$stempel).LocalDateTime
  if ($plik.LastWriteTime -gt $czasStempla.AddMinutes(5)) {
    Write-Host "!! UWAGA: $zasob zmieniony po ostatnim podbiciu ?v=$stempel" -ForegroundColor Yellow
    Write-Host "   Powracajacy odwiedzajacy moga dostac stara wersje z cache." -ForegroundColor Yellow
    Write-Host "   Podbij ?v= we wszystkich plikach HTML przed wysylka." -ForegroundColor Yellow
    Write-Host ""
  }
}

if ($Lista) {
  Write-Host "Poleci na $Remote :" -ForegroundColor Cyan
  $Pliki | ForEach-Object { "  $_" }
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

foreach ($p in $Pliki) {
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
