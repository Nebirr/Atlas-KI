from __future__ import annotations
import os, platform
from pathlib import Path
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QKeySequenceEdit
from atlas.speech.controller import SpeechController
from atlas.atlas_gui.services.settings_service import load_settings, save_settings

def _en_model_dir() -> str:
    env = os.environ.get("ATLAS_VOSK_MODEL_DIR")
    if env and os.path.isdir(env):
        return env

    try:
        import sys
        from pathlib import Path
        if getattr(sys, "frozen", False):
            app_dir = Path(sys.executable).resolve().parent 
        else:
            app_dir = Path(__file__).resolve().parents[2]
        cand = app_dir / "models" / "vosk" / "vosk-model-small-en-us-0.15"
        if cand.is_dir():
            return str(cand)
    except Exception:
        pass

    base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    return os.path.join(base, "Atlas", "models", "vosk", "vosk-model-small-en-us-0.15")

def _seq_text_portable(seq: QKeySequence) -> str:
    return seq.toString(QKeySequence.PortableText) or "Space"

def _seq_to_parts(seq: QKeySequence) -> tuple[QtCore.Qt.KeyboardModifiers, QtCore.Qt.Key]:
    if seq.count() == 0:
        return QtCore.Qt.NoModifier, QtCore.Qt.Key_Space

    txt = seq.toString(QKeySequence.PortableText)
    if not txt:
        return QtCore.Qt.NoModifier, QtCore.Qt.Key_Space

    up = txt.upper()

    mods = QtCore.Qt.NoModifier
    if "CTRL+"  in up: mods |= QtCore.Qt.ControlModifier
    if "SHIFT+" in up: mods |= QtCore.Qt.ShiftModifier
    if "ALT+"   in up: mods |= QtCore.Qt.AltModifier
    if "META+"  in up: mods |= QtCore.Qt.MetaModifier

    base = up.split("+")[-1] if "+" in up else up

    special = {
        "SPACE": QtCore.Qt.Key_Space, "TAB": QtCore.Qt.Key_Tab,
        "ESC": QtCore.Qt.Key_Escape, "ESCAPE": QtCore.Qt.Key_Escape,
        "ENTER": QtCore.Qt.Key_Return, "RETURN": QtCore.Qt.Key_Return,
        "BACKSPACE": QtCore.Qt.Key_Backspace, "DELETE": QtCore.Qt.Key_Delete,
        "HOME": QtCore.Qt.Key_Home, "END": QtCore.Qt.Key_End,
        "PAGEUP": QtCore.Qt.Key_PageUp, "PAGEDOWN": QtCore.Qt.Key_PageDown,
        "UP": QtCore.Qt.Key_Up, "DOWN": QtCore.Qt.Key_Down,
        "LEFT": QtCore.Qt.Key_Left, "RIGHT": QtCore.Qt.Key_Right,
    }
    if base in special:
        return mods, special[base]

    if base.startswith("F") and base[1:].isdigit():
        n = int(base[1:])
        if 1 <= n <= 35:
            return mods, getattr(QtCore.Qt, f"Key_F{n}")

    if len(base) == 1 and base.isdigit():
        return mods, getattr(QtCore.Qt, f"Key_{base}")

    if len(base) == 1 and "A" <= base <= "Z":
        return mods, getattr(QtCore.Qt, f"Key_{base}")

    return mods, QtCore.Qt.Key_Space

def _mods_to_keys(mods: QtCore.Qt.KeyboardModifiers) -> set[int]:
    """Für keyRelease: welche Mod-Tasten gehören zur Kombi?"""
    keys = set()
    if mods & QtCore.Qt.ShiftModifier:   keys.add(int(QtCore.Qt.Key_Shift))
    if mods & QtCore.Qt.ControlModifier: keys.add(int(QtCore.Qt.Key_Control))
    if mods & QtCore.Qt.AltModifier:     keys.add(int(QtCore.Qt.Key_Alt))
    if mods & QtCore.Qt.MetaModifier:    keys.add(int(QtCore.Qt.Key_Meta))
    return keys

class SpeechWidget(QtWidgets.QWidget):
    def __init__(self, username: str, parent=None, on_final_text=None):
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  
        self._ptt_active = False
        self._capturing  = False
        self.username    = username
        self.on_final_text = on_final_text

        self.settings = load_settings(self.username)
        stored = getattr(self.settings, "ptt_key", "Space")  
        self._ptt_seq = QKeySequence.fromString(stored, QKeySequence.PortableText)
        self._ptt_mods, self._ptt_key = _seq_to_parts(self._ptt_seq)
        self._ptt_mod_keys = _mods_to_keys(self._ptt_mods)

        model_dir = _en_model_dir()
        if not os.path.isdir(model_dir):
            QtWidgets.QMessageBox.warning(
                self, "Vosk model missing",
                "Expected English model at:\n" + model_dir +
                "\n\nSet ATLAS_VOSK_MODEL_DIR to override."
            )

        self.ctrl = SpeechController(model_dir, parent=self)

        top_row = QtWidgets.QHBoxLayout()
        self.live_toggle = QtWidgets.QCheckBox("Live-Erkennung (Mic always on)")

        self.ptt_label  = QtWidgets.QLabel(f"PTT: {_seq_text_portable(self._ptt_seq)}")
        self.ptt_change = QtWidgets.QPushButton("Change")
        self.ptt_edit   = QKeySequenceEdit()
        self.ptt_edit.setVisible(False)
        self.ptt_edit.setKeySequence(self._ptt_seq)

        top_row.addWidget(self.live_toggle)
        top_row.addStretch(1)
        top_row.addWidget(self.ptt_label)
        top_row.addWidget(self.ptt_change)
        top_row.addWidget(self.ptt_edit)

        self.ptt_btn = QtWidgets.QPushButton("🎤 Push to Talk (hold)")
        self.ptt_btn.setMinimumHeight(56)

        self.status = QtWidgets.QLabel("Ready.")
        self.status.setWordWrap(True)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addLayout(top_row)          
        lay.addWidget(self.ptt_btn)
        lay.addWidget(self.status, 1)

        is_live = (getattr(self.settings, "speech_mode", "ptt") == "live")
        self.live_toggle.setChecked(is_live)
        self._apply_mode_ui(is_live)
        self.ctrl.set_mode("live" if is_live else "ptt")

        self.live_toggle.toggled.connect(self._on_live_toggled)
        self.ptt_btn.pressed.connect(self.ctrl.start_listening)
        self.ptt_btn.released.connect(self.ctrl.stop_listening)

        self.ctrl.partial_text.connect(lambda t: self._set_status(f"⚡ {t}"))
        self.ctrl.final_text.connect(self._on_final_text)          
        self.ctrl.listening_changed.connect(lambda b: self._set_status("🎙️ listening…" if b else "⏹️ idle"))
        self.ctrl.error.connect(lambda e: self._set_status(f"❗ {e}"))

        self.ptt_change.clicked.connect(self._begin_capture)
        self.ptt_edit.keySequenceChanged.connect(self._on_seq_changed)
        self.ptt_edit.editingFinished.connect(self._end_capture)

    def _on_live_toggled(self, checked: bool):
        self._apply_mode_ui(checked)
        self.settings.speech_mode = "live" if checked else "ptt"
        save_settings(self.username, self.settings)
        self.ctrl.set_mode(self.settings.speech_mode)

    def _apply_mode_ui(self, live: bool):
        self.ptt_btn.setEnabled(not live)
        if live:
            self._set_status("Mic always on – speak and pause for final ✅")
        else:
            self._set_status(f"PTT: hold button or {_seq_text_portable(self._ptt_seq)}")

    def _begin_capture(self):
        self._capturing = True
        self.ptt_edit.setKeySequence(self._ptt_seq)
        self.ptt_edit.setVisible(True)
        self.ptt_edit.setFocus(QtCore.Qt.OtherFocusReason)
        self._set_status("🔁 Press desired combo (e.g., Ctrl+Space)…")

    def _on_seq_changed(self, seq: QKeySequence):
        self.ptt_label.setText(f"PTT: {_seq_text_portable(seq)}")

    def _end_capture(self):
        seq = self.ptt_edit.keySequence()
        txt = _seq_text_portable(seq)
        self._ptt_seq = seq
        self._ptt_mods, self._ptt_key = _seq_to_parts(seq)
        self._ptt_mod_keys = _mods_to_keys(self._ptt_mods)

        self.settings.ptt_key = txt
        save_settings(self.username, self.settings)

        self.ptt_edit.setVisible(False)
        self._capturing = False
        self._set_status(f"🔑 PTT bound to '{txt}'")  

    def keyPressEvent(self, e):
        if self._capturing or e.isAutoRepeat():
            return super().keyPressEvent(e)

        if not self.live_toggle.isChecked():
            event_mods = e.modifiers()
            event_key  = e.key()
            if (event_mods == self._ptt_mods) and (event_key == self._ptt_key) and not self._ptt_active:
                self._ptt_active = True
                self.ctrl.start_listening()
                e.accept()
                return
        super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if self._capturing or e.isAutoRepeat():
            return super().keyReleaseEvent(e)

        if self._ptt_active and not self.live_toggle.isChecked():
            released = e.key()
            if released == self._ptt_key or released in self._ptt_mod_keys:
                self._ptt_active = False
                self.ctrl.stop_listening()
                e.accept()
                return
        super().keyReleaseEvent(e)

    def _on_final_text(self, text: str):
        self._set_status(f"✅ {text}")
        if self.on_final_text:
            self.on_final_text(text)

    def _set_status(self, msg: str):
        self.status.setText(msg)

    def closeEvent(self, e):
        self.ctrl.stop_continuous()
        super().closeEvent(e)