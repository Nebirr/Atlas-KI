\# Atlas KI



Desktop-KI mit \*\*PySide6\*\*, \*\*Offline-Spracherkennung (Vosk)\*\*, eigenem \*\*PyInstaller-Build\*\* und \*\*Inno Setup-Installer\*\*.



\## Features

\- Moderne GUI (PySide6)

\- Sauberer Build via PowerShell (`build.ps1`)

\- Windows-Installer mit Inno Setup (`installer.iss`)



---



\## Projektstruktur (Kurz)



atlas/ # Quellcode

build.ps1 # Build-Skript (PyInstaller)

installer.iss # Inno Setup-Script

requirements.txt # Laufzeit-Pakete

requirements-dev.txt # Build-Pakete



---



\## Voraussetzungen

\- \*\*Windows 10/11\*\*

\- \*\*Python 3.11+\*\*

\- (optional) \*\*Inno Setup\*\* installiert für den Installer



---



\## Installation (Dev-Umgebung)

```powershell

python -m venv Atlas-venv

.\\Atlas-venv\\Scripts\\Activate.ps1

pip install -r requirements-dev.txt



\# normale App-Builds

.\\build.ps1



\# Debug mit Konsole

.\\build.ps1 -Console



Output: dist\\Atlas\\Atlas.exe

