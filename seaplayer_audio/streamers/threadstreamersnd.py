import time
import queue
import numpy as np
import sounddevice as sd
from threading import Thread
from typing_extensions import Optional, NoReturn
from .._types import AudioSamplerate, AudioChannels, AudioDType
from ..base import SoundDeviceStreamerBase, AsyncSoundDeviceStreamerBase, StreamerState

# ^ Thread Streamer

class ThreadSoundDeviceStreamer(SoundDeviceStreamerBase):
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None
    ):
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device
        )
        self.state = StreamerState(StreamerState.LOCKED)
        self.thread = Thread(target=self.run)
        self.queue: queue.Queue[np.ndarray] = queue.Queue(1)
    
    def is_busy(self) -> bool:
        return self.queue.qsize() >= 1
    
    def run(self) -> NoReturn:
        if not self.stream.active:
            self.stream.start()
        self.state |= StreamerState.STARTED
        while StreamerState.RUNNING in self.state:
            try:
                if StreamerState.LOCKED not in self.state:
                    data = self.queue.get(timeout=0.01)
                    self.stream.write(data)
            except queue.Empty:
                pass
        if self.stream.active:
            self.stream.abort()
            self.stream.stop()
        self.state &= ~StreamerState.STARTED
    
    def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.state &= ~StreamerState.LOCKED
            self.thread.start()
            while StreamerState.STARTED not in self.state:
                time.sleep(0.01)
    
    def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            self.queue.task_done()
            self.stream.abort()
            self.stream.stop()
            while StreamerState.STARTED in self.state:
                time.sleep(0.01)
    
    def abort(self):
        self.state |= StreamerState.LOCKED
        self.queue.task_done()
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    def send(self, data: np.ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            self.queue.put(data)
            return True
        return False
