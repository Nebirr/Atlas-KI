from PySide6.QtCore import QThread, Signal
import sounddevice as sd
import numpy as np
import queue

class MicWorker(QThread):
    audio_frame =Signal(bytes)
    
    def __init__(self, rate=16000, frame_ms =20, parent=None, device=None):
        super().__init__(parent)
        self.rate = rate
        self.frame_len = int(rate * frame_ms / 1000)
        self._q = queue.Queue(maxsize=50)
        self._running = False
        self.device = device

    def run(self):
        self._running = True

        def cb(indata, frames, time, status):
            
            pcm16 = (np.clip(indata[:, 0], -1.0, 1.0) * 32767).astype(np.int16).tobytes()
            try:
                self._q.put_nowait(pcm16)
            except queue.Full:
                pass
        
        with sd.InputStream(channels=1, 
                            samplerate=self.rate, 
                            blocksize=self.frame_len,
                            dtype='float32',
                            callback=cb, 
                            device=self.device):
            while self._running:
                try:
                    chunk = self._q.get(timeout=0.1)
                    self.audio_frame.emit(chunk)
                except queue.Empty:
                    pass

    def stop(self):
        self._running = False
        self.wait(500)