# build.ps1 — Atlas Builder (venv + Requirements + PyInstaller)
# Nutzung:
#   ./build.ps1                 # normaler GUI-Build (ohne Konsole)
#   ./build.ps1 -Console        # mit Konsole (zum Debuggen)
#   ./build.ps1 -Clean          # vorher build/dist/spec löschen
#   ./build.ps1 -RecreateVenv   # venv neu erstellen (frische Umgebung)

param(
  [switch]$Clean = $false,
  [switch]$Console = $false,
  [switch]$RecreateVenv = $false
)

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------
# 0) Projektpfade
# ------------------------------------------------------------
$root = (Resolve-Path ".").Path
$venvDir = Join-Path $root "Atlas-venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"

# System-Python als Fallback (nur für venv-Erstellung)
$sysPython = "python"
try {
  $sysPyVersion = & $sysPython -V 2>$null
} catch {
  # Optional: absoluter Pfad als Fallback, wenn du einen festen hast
  $sysPython = "C:\Users\Admin\AppData\Local\Programs\Python\Python313\python.exe"
}

# ------------------------------------------------------------
# 1) venv sicherstellen (oder neu erstellen)
# ------------------------------------------------------------
if ($RecreateVenv -and (Test-Path $venvDir)) {
  Write-Host "Lösche vorhandenes venv: $venvDir" -ForegroundColor DarkYellow
  Remove-Item $venvDir -Recurse -Force
}

if (-not (Test-Path $venvPython)) {
  Write-Host "Erstelle virtuelles Environment: Atlas-venv" -ForegroundColor DarkYellow
  & $sysPython -m venv $venvDir
}

if (-not (Test-Path $venvPython)) {
  throw "Konnte venv nicht erstellen/finden: $venvPython"
}

Write-Host "Using Python: $venvPython" -ForegroundColor Cyan

# ------------------------------------------------------------
# 2) Optional Clean
# ------------------------------------------------------------
if ($Clean) {
  Write-Host "Cleaning build/ & dist/ & Atlas.spec..." -ForegroundColor DarkYellow
  if (Test-Path "$root\build") { Remove-Item "$root\build" -Recurse -Force }
  if (Test-Path "$root\dist")  { Remove-Item "$root\dist"  -Recurse -Force }
  if (Test-Path "$root\Atlas.spec") { Remove-Item "$root\Atlas.spec" -Force }
}

# ------------------------------------------------------------
# 3) Requirements installieren (dev -> runtime)
# ------------------------------------------------------------
& $venvPython -m pip install -U pip setuptools wheel

$reqDev = Join-Path $root "requirements-dev.txt"
$reqRt  = Join-Path $root "requirements.txt"

if (Test-Path $reqDev) {
  Write-Host "Installiere requirements-dev.txt..." -ForegroundColor DarkGray
  & $venvPython -m pip install -r $reqDev
} elseif (Test-Path $reqRt) {
  Write-Host "Installiere requirements.txt..." -ForegroundColor DarkGray
  & $venvPython -m pip install -r $reqRt
} else {
  # Minimal-Set, falls keine Dateien vorhanden
  Write-Host "Keine requirements-Dateien gefunden – installiere Minimal-Set..." -ForegroundColor DarkYellow
  & $venvPython -m pip install `
    "pyinstaller>=6.14" `
    "PySide6~=6.9" `
    "tabulate~=0.9" `
    "psutil~=6.0" `
    "GPUtil~=1.4"
}

# ------------------------------------------------------------
# 4) PyInstaller-Argumente
# ------------------------------------------------------------
if ($Console) {
  $windowFlag = "--console"
} else {
  $windowFlag = "--noconsole"
}

$piArgs = @(
  $windowFlag,
  "--name", "Atlas",
  "--icon", "assets\icons\atlas_icon.ico",
  "--noconfirm",
  "--clean",
  # PySide6 komplett einsammeln (ersetzt ältere --qt-plugins-Flags)
  "--collect-submodules", "PySide6",
  "--collect-data", "PySide6",
  "--collect-binaries", "PySide6",
  # häufig genutzte Extras (für dein Projekt)
  "--collect-submodules", "tabulate",
  "--collect-submodules", "GPUtil",
  "--collect-submodules", "psutil",
  # --- Speech / Audio dependencies ---
  "--collect-binaries", "sounddevice",
  "--collect-submodules", "vosk",
  "--collect-submodules", "numpy",
  # Einstiegspunkt
  "launcher.py"
)

Write-Host "PyInstaller wird mit folgenden Argumenten gestartet:" -ForegroundColor Cyan
$piArgs | ForEach-Object { Write-Host "  $_" }

# ------------------------------------------------------------
# 5) Build ausführen (immer venv-Python nutzen!)
# ------------------------------------------------------------
& $venvPython -m PyInstaller @piArgs
if ($LASTEXITCODE -ne 0) {
  throw "PyInstaller-Build fehlgeschlagen (ExitCode $LASTEXITCODE)."
}

# ------------------------------------------------------------
# 6) Sanity-Check: qwindows.dll in platforms
# ------------------------------------------------------------
$distRoot = Join-Path $root "dist\Atlas"
$qwin1 = Join-Path $distRoot "PySide6\plugins\platforms\qwindows.dll"
$qwin2 = Join-Path $distRoot "PySide6\Qt\plugins\platforms\qwindows.dll"

if ( (Test-Path $qwin1) -or (Test-Path $qwin2) ) {
  Write-Host "OK: Qt Platform Plugin gefunden." -ForegroundColor Green
} else {
  Write-Warning "WARNUNG: qwindows.dll nicht gefunden. App könnte nicht starten."
  Get-ChildItem -Recurse $distRoot -Filter qwindows.dll | Select-Object FullName
}

Write-Host "`nBuild fertig. Starte:  $distRoot\Atlas.exe" -ForegroundColor Green
