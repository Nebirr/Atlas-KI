# 🧭 Atlas AI

A Windows desktop assistant built with **PySide6**, featuring a modular architecture,  
a clean build pipeline using **PyInstaller**, and a professional **Inno Setup** installer.

---

## ✨ Features
- Modern GUI built with **PySide6**
- Modular command/intent system (open apps, folders, websites, system info)
- One-click build via PowerShell (`build.ps1`)
- Professional Windows installer (`installer.iss`)
- Optional continuous integration (GitHub Actions)

> 🗣️ *Speech recognition and TTS are planned for future updates.*

---

## 🧱 Project Structure

atlas/ # Core source code (GUI, logic, tasks)
build.ps1 # Build script (PyInstaller)
installer.iss # Inno Setup script
requirements.txt # Runtime dependencies
requirements-dev.txt # Dev/Build dependencies

---

## ⚙️ Requirements
- Windows 10/11 (64-bit)
- Python 3.11+
- (optional) Inno Setup 6+ (for building the installer manually)

---

🗺️ Roadmap

Offline Speech Recognition (Vosk + WebRTC VAD)

Text-to-Speech responses

Automatic update checker (GitHub Releases)

Settings window with user paths and themes