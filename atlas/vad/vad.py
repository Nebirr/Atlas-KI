import numpy as np

class VAD:
    def __init__(self, sample_rate=16000, frame_ms=20, rms_thresh=0.01, hangover_ms=200):
        self.sample_rate = sample_rate
        self.frame_len = int(sample_rate * frame_ms / 1000)
        self.rms_thresh = rms_thresh
        self.hangover_frames = max(1, int(hangover_ms / frame_ms))
        self._hang = 0

    def is_speech(self, pcm16: bytes) -> bool:
        if len(pcm16) != self.frame_len * 2:
            return False
        x = np.frombuffer(pcm16, dtype=np.int16).astype(np.float32) / 32768.0
        rms = float(np.sqrt(np.mean(x * x)) + 1e-9)
        if rms >= self.rms_thresh:
            self._hang = self.hangover_frames
            return True
        if self._hang > 0:
            self._hang -= 1
            return True
        return False