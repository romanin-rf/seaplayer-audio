import asyncio
from asyncio import AbstractEventLoop
from numpy import ndarray, vstack as npvstack, zeros as npzeros
from sounddevice import OutputStream
from typing_extensions import Any, Optional, NoReturn, Callable, deprecated
from .._types import AudioSamplerate, AudioChannels, AudioDType
from ..base import AsyncSoundDeviceStreamerBase, SoundDeviceStreamerBase, StreamerState
from ..queues import AsyncQueue, Queue

# ! Main Class
class CallbackSoundDeviceStreamer(SoundDeviceStreamerBase):
    __steamer_type__ = 'callback-sounddevice'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None,
        precallback: Optional[Callable[[int], Any]]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.queue: Queue[ndarray] = Queue(1)
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback__
        )
        self.precallback = precallback if (precallback is not None) else (lambda frames: None)
        self.buffer: Optional[ndarray] = None
    
    def __callback__(self, outdata: ndarray, frames: int, time, status):
        self.precallback(frames)
        if self.buffer is None:
            try:
                d = self.queue.get()
            except:
                return
            wdata = d[:frames]
            self.buffer = d[frames:]
        elif len(self.buffer) >= frames:
            wdata = self.buffer[:frames]
            self.buffer = self.buffer[frames:]
        elif (len(self.buffer) < frames) and (not self.queue.qsize() == 0):
            try:
                d = self.queue.get()
            except:
                return
            wdata = self.buffer.copy()
            self.buffer = None
            needed = frames - len(wdata)
            wdata = npvstack([wdata, d[:needed]])
            self.buffer = d[needed:]
        elif (len(self.buffer) < frames) and self.queue.empty():
            wdata = self.buffer.copy()
            self.buffer = None
            needed = frames - len(wdata)
            wdata = npvstack([wdata, npzeros((needed, 2), dtype=outdata.dtype)])
        else:
            self.buffer = None
            return
        outdata[:] = wdata
    
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
            try: self.queue.abort()
            except: pass
            self.stream.stop()
    
    def abort(self):
        self.state |= StreamerState.LOCKED
        try: self.queue.abort()
        except: pass
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    def send(self, data: ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            self.queue.put(data)
            return True
        return False

class AsyncCallbackSoundDeviceStreamer(AsyncSoundDeviceStreamerBase):
    __steamer_type__ = 'async-callback-sounddevice'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        loop: Optional[AbstractEventLoop]=None,
        device: Optional[int]=None
    ):
        super().__init__(samplerate, channels, dtype, closefd, loop, device)
        self.queue: AsyncQueue[ndarray] = AsyncQueue(1)
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback__
        )
        self.buffer: Optional[ndarray] = None
    
    def __callback__(self, outdata: ndarray, frames: int, time, status):
        if self.buffer is None:
            try:
                d = asyncio.run_coroutine_threadsafe(self.queue.get(), self.loop).result()
            except:
                return
            wdata = d[:frames]
            self.buffer = d[frames:]
        elif len(self.buffer) >= frames:
            wdata = self.buffer[:frames]
            self.buffer = self.buffer[frames:]
        elif (len(self.buffer) < frames) and (not self.queue.qsize() == 0):
            try:
                d = asyncio.run_coroutine_threadsafe(self.queue.get(), self.loop).result()
            except:
                return
            wdata = self.buffer.copy()
            self.buffer = None
            needed = frames - len(wdata)
            wdata = npvstack([wdata, d[:needed]])
            self.buffer = d[needed:]
        elif (len(self.buffer) < frames) and self.queue.empty():
            wdata = self.buffer.copy()
            self.buffer = None
            needed = frames - len(wdata)
            wdata = npvstack([wdata, npzeros((needed, 2), dtype=outdata.dtype)])
        else:
            self.buffer = None
            return
        outdata[:] = wdata
    
    async def is_busy(self) -> bool:
        return self.queue.qsize() >= self.queue.maxsize
    
    @deprecated("!!! NOT IMPLEMENTED !!!")
    async def run(self) -> NoReturn:
        raise NotImplementedError
    
    async def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.stream.start()
            self.state &= ~StreamerState.LOCKED
    
    async def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            try: await self.queue.abort()
            except: pass
            self.stream.stop()
    
    async def abort(self):
        self.state |= StreamerState.LOCKED
        try: await self.queue.abort()
        except: pass
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    async def send(self, data: ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            await self.queue.put(data)
            return True
        return False