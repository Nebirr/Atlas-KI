# 🧭 Atlas AI

A Windows desktop assistant built with **PySide6**.  
Now with **Live speech recognition** and **Push-to-Talk** (configurable hotkey) — the **English Vosk model is bundled** with the installer for plug-and-play.

---

## ✨ Features
- Modern GUI (PySide6)
- **Live speech recognition** (auto-finalize after brief silence)
- **Push-to-Talk** (press & hold) + **configurable hotkey** (e.g., Space / Ctrl+Space)
- **Plug & Play installer** (Inno Setup) — EN Vosk model included
- Clean packaging (PyInstaller onedir)
- Modular command/intent system (open apps/folders/websites, system info)

---

## 🚀 Getting Started (Windows)

1. Download the latest **Atlas-Setup-*.exe** from the [Releases](../../releases) page.  
2. Run the installer (installs to *Program Files*, requires admin).  
3. Launch **Atlas** from the Start menu or desktop.

**Quick test**
- **Live ON** → speak → short pause → ✅ final text  
- **Live OFF** → hold the PTT button or your **hotkey** → speak → release → ✅ final  
- Say **“help”** → Help dialog opens

> The installer also sets `ATLAS_VOSK_MODEL_DIR` to the bundled model:  
> `C:\Program Files\Atlas\models\vosk\vosk-model-small-en-us-0.15`

---

## 🧱 Project Structure
VS_Atlas/
-atlas/ # App code (GUI, logic, speech, services)
│  atlas_gui/
│  speech/
│  stt/
- assets/ # icons, etc.
- models/
│  vosk/
│  vosk-model-small-en-us-0.15/ # bundled speech model (via installer)
- dist/ # PyInstaller output (ignored in git)
- build/ # PyInstaller build cache (ignored)
- installer.iss # Inno Setup script (plug & play)
- requirements.txt
- README.md

---

## ⚙️ Requirements
- Windows 10/11 (64-bit)
- **Microphone**
- (For building from source) Python **3.11+**, Inno Setup 6+ (for installer)

---
## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE.txt) file for details.
