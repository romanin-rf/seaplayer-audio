import time
import queue
import asyncio
import numpy as np
import sounddevice as sd
from threading import Thread
from asyncio import AbstractEventLoop
from typing_extensions import Optional
from .._types import AudioSamplerate, AudioChannels, AudioDType
from ..base import SoundDeviceStreamerBase, AsyncSoundDeviceStreamerBase, StreamerState

# ^ Thread Streamer

class ThreadSoundDeviceStreamer(SoundDeviceStreamerBase):
    __steamer_type__ = 'thread-sounddevice'
    
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
        return self.queue.qsize() >= self.queue.maxsize
    
    def run(self) -> None:
        if not self.stream.active:
            self.stream.start()
        self.state |= StreamerState.STARTED
        while StreamerState.RUNNING in self.state:
            try:
                data = self.queue.get(timeout=0.01)
                self.stream.write(data)
            except queue.Empty:
                pass
        if self.stream.active:
            self.stream.stop()
        self.state &= ~StreamerState.STARTED
    
    def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.thread.start()
            while StreamerState.STARTED not in self.state:
                time.sleep(0.01)
            self.state &= ~StreamerState.LOCKED
    
    def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            try: self.queue.task_done()
            except: pass
            self.stream.stop()
            while StreamerState.STARTED in self.state:
                time.sleep(0.01)
    
    def abort(self):
        self.state |= StreamerState.LOCKED
        try: self.queue.task_done()
        except: pass
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    def send(self, data: np.ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            self.queue.put(data)
            return True
        return False


class AsyncThreadSoundDeviceStreamer(AsyncSoundDeviceStreamerBase):
    __steamer_type__ = 'async-thread-sounddevice'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        loop: Optional[AbstractEventLoop]=None,
        device: Optional[int]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, loop, device)
        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device
        )
        self.task: Optional[asyncio.Task] = None
        self.state = StreamerState(StreamerState.LOCKED)
        self.queue: asyncio.Queue[np.ndarray] = asyncio.Queue(1)
    
    async def is_busy(self) -> bool:
        return self.queue.qsize() >= self.queue.maxsize
    
    def run(self) -> None:
        if not self.stream.active:
            self.stream.start()
        self.state |= StreamerState.STARTED
        while StreamerState.RUNNING in self.state:
            try:
                data = asyncio.run_coroutine_threadsafe(self.queue.get(timeout=0.01), self.loop).result()
                self.stream.write(data)
            except queue.Empty:
                pass
        if self.stream.active:
            self.stream.stop()
        self.state &= ~StreamerState.STARTED
    
    async def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.task = asyncio.create_task(asyncio.to_thread(self.run))
            while StreamerState.STARTED not in self.state:
                await asyncio.sleep(0.01)
            self.state &= ~StreamerState.LOCKED
    
    async def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            try: self.queue.task_done()
            except: pass
            self.stream.stop()
            while (StreamerState.STARTED in self.state) or (not self.task.done()):
                await asyncio.sleep(0.01)
    
    async def abort(self):
        self.state |= StreamerState.LOCKED
        try: self.queue.task_done()
        except: pass
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    async def send(self, data: np.ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            await self.queue.put(data)
            return True
        return False