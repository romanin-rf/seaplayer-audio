from queue import Queue
from numpy import ndarray, vstack as npvstack, zeros as npzeros
from sounddevice import OutputStream
from typing_extensions import Optional, NoReturn, deprecated
from .._types import AudioSamplerate, AudioChannels, AudioDType
from ..base import SoundDeviceStreamerBase, StreamerState


# ! Main Class
class CallbackSoundDeviceStreamer(SoundDeviceStreamerBase):
    __steamer_type__ = 'callback-sounddevice'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.queue: Queue[ndarray] = Queue(1)
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback
        )
        self.buffer: Optional[ndarray] = None
    
    def __callback(self, outdata: ndarray, frames: int, time, status):
        if self.buffer is None:
            d = self.queue.get()
            wdata = d[:frames]
            self.buffer = d[frames:]
        elif len(self.buffer) >= frames:
            wdata = self.buffer[:frames]
            self.buffer = self.buffer[frames:]
        elif (len(self.buffer) < frames) and (not self.queue.empty()):
            d = self.queue.get()
            wdata = self.buffer.copy()
            self.buffer = None
            needed = frames - len(wdata)
            wdata = npvstack([wdata, d[:needed]])
            self.buffer = d[needed:]
        elif (len(self.buffer) < frames) and self.queue.empty():
            wdata = self.buffer.copy()
            self.buffer = None
            needed = frames - len(wdata)
            wdata = npvstack([wdata, npzeros((2, 2), dtype=outdata.dtype)[:needed]])
        try:
            outdata[:] = wdata
        except ValueError:
            if self.buffer is not None:
                wdata = self.buffer.copy()
                self.buffer = None
                needed = frames - len(wdata)
                wdata = npvstack([wdata, npzeros((2, 2), dtype=outdata.dtype)[:needed]])
                outdata[:] = wdata
            else:
                outdata[:] = npzeros((2, 2), dtype=outdata.dtype)[:frames]
    
    def is_busy(self) -> bool:
        return self.queue.qsize() >= 1
    
    @deprecated("!!! NOT IMPLEMENTED !!!")
    def run(self) -> NoReturn:
        raise NotImplementedError
    
    def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.stream.start()
            self.state &= ~StreamerState.LOCKED
    
    def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            try: self.queue.task_done()
            except: pass
            self.stream.stop()
    
    def abort(self):
        self.state |= StreamerState.LOCKED
        try: self.queue.task_done()
        except: pass
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    def send(self, data: ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            self.queue.put(data)
            return True
        return False