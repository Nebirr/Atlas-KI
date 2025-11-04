from __future__ import annotations
from vosk import Model, KaldiRecognizer
import json

class VoskEngine:
    def __init__(self, model_path: str, sample_rate: int = 16000):
        self.model = Model(model_path)
        self.sample_rate = sample_rate
        self.rec = KaldiRecognizer(self.model, sample_rate)

    def accept_audio(self, pcm16: bytes):
     
        if self.rec.AcceptWaveform(pcm16):
            res = json.loads(self.rec.Result())
            txt = (res.get("text") or "").strip()
            return (txt if txt else None, None)
        else:
            res = json.loads(self.rec.PartialResult())
            part = (res.get("partial") or "").strip()
            return (None, part if part else None)

    def reset(self) -> None:
        self.rec = KaldiRecognizer(self.model, self.sample_rate)