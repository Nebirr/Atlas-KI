from __future__ import annotations
from PySide6.QtCore import QObject, Signal
from atlas.audio.mic_worker import MicWorker
from atlas.stt.vosk_engine import VoskEngine

class SpeechController(QObject):
    partial_text = Signal(str)
    final_text = Signal(str)
    listening_changed = Signal(bool)
    error = Signal(str)

    def __init__(self, model_path: str, parent=None, device=None, sample_rate: int = 16000):
        super().__init__(parent)
        self.sample_rate = sample_rate
        self.mic = MicWorker(rate=sample_rate, parent=self, device=device)
        self.stt = VoskEngine(model_path, sample_rate)
        self.mic.audio_frame.connect(self._on_frame)

        self._listening = False      
        self._continuous = False     

    
    def start_listening(self) -> None:
        if self._listening:
            return
        self._listening = True
        if not self.mic.isRunning():
            self.mic.start()
        self.listening_changed.emit(True)

    def stop_listening(self) -> None:
        if not self._listening:
            return
        self._listening = False
        if not self._continuous and self.mic.isRunning():
            self.mic.stop()
        self.listening_changed.emit(False)

    
    def start_continuous(self) -> None:
        self._continuous = True
        if not self.mic.isRunning():
            self.mic.start()
        self.listening_changed.emit(True)

    def stop_continuous(self) -> None:
        self._continuous = False
        if not self._listening and self.mic.isRunning():
            self.mic.stop()
        self.listening_changed.emit(False)

    def set_mode(self, mode: str) -> None:  
        if mode == "live":
            self.start_continuous()
        else:
            self.stop_continuous()

    
    def _on_frame(self, pcm16: bytes) -> None:
        try:
            final_txt, partial_txt = self.stt.accept_audio(pcm16)
            if partial_txt:
                self.partial_text.emit(partial_txt)
            if final_txt:
                final_txt = final_txt.strip()
                if final_txt:
                    self.final_text.emit(final_txt)
        except Exception as e:
            self.error.emit(str(e))