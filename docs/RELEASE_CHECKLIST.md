\# Release Checkliste – Atlas KI



\## Vorbereiten

\- \[ ] Version im Code erhöht (z. B. `\_\_version\_\_` oder Konstanten)

\- \[ ] Version in `installer.iss` (`AppVersion=`) angepasst

\- \[ ] CHANGELOG / RELEASE\_TEMPLATE ausgefüllt

\- \[ ] `.gitignore` aktuell (keine dist/Output/EXE im Repo)



\## Build

\- \[ ] `./build.ps1 -Clean` ausgeführt (frischer Build)

\- \[ ] App testweise gestartet (`dist/Atlas/Atlas.exe`)

\- \[ ] (Optional) Speech-Modellpfad getestet (%AppData%\\Atlas\\models\\vosk\\...)



\## Installer

\- \[ ] `installer.iss` mit Inno Setup kompiliert

\- \[ ] Installer startet App nach Installation

\- \[ ] Deinstallation funktioniert (Einträge im Startmenü/Uninstaller ok)



\## Tag \& Release

\- \[ ] Git-Tag gesetzt: `git tag vX.Y.Z \&\& git push --tags`

\- \[ ] GitHub → Releases → \*Draft new release\*

\- \[ ] Tag vX.Y.Z ausgewählt

\- \[ ] `Atlas-Setup-X.Y.Z.exe` als Asset hochgeladen

\- \[ ] Release-Text aus `RELEASE\_TEMPLATE.md` eingefügt

\- \[ ] (Optional) SHA256-Checksum hinzugefügt



\## Smoke-Test

\- \[ ] Installation auf „frischem“ Windows (ohne Dev-Tools) geprüft

\- \[ ] Starten ohne Internet getestet

\- \[ ] Pfade/Logs/Permissions ok

