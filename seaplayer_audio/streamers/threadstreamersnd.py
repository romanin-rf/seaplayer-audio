import time
import queue
import asyncio
import numpy as np
import sounddevice as sd
from threading import Thread
from asyncio import AbstractEventLoop
from typing_extensions import Optional, NoReturn
from ..functions import aiorun, aiowrap
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


class AsyncThreadSoundDeviceStreamer(AsyncSoundDeviceStreamerBase):
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
        self.state = StreamerState(StreamerState.LOCKED)
        self.queue: asyncio.Queue[np.ndarray] = asyncio.Queue(1)
        self.__stream_abort = aiowrap(self.loop, self.stream.abort)
        self.__stream_stop = aiowrap(self.loop, self.stream.stop)
        self.__stream_start = aiowrap(self.loop, self.stream.start)
        self.__stream_write = aiowrap(self.loop, self.stream.write)
    
    async def is_busy(self) -> bool:
        return self.queue.qsize() >= 1
    
    async def run(self) -> NoReturn:
        if not self.stream.active:
            await self.__stream_start()
        self.state |= StreamerState.STARTED
        while StreamerState.RUNNING in self.state:
            try:
                if StreamerState.LOCKED not in self.state:
                    data = await self.queue.get(timeout=0.01)
                    await self.__stream_write(data)
            except queue.Empty:
                pass
        if self.stream.active:
            await self.__stream_abort()
            await self.__stream_stop()
        self.state &= ~StreamerState.STARTED
    
    async def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.state &= ~StreamerState.LOCKED
            # TODO: Написать метод...
            while StreamerState.STARTED not in self.state:
                await asyncio.sleep(0.01)
    
    async def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            await self.queue.task_done()
            await self.__stream_abort()
            await self.__stream_stop()
            while StreamerState.STARTED in self.state:
                await asyncio.sleep(0.01)
    
    async def abort(self):
        self.state |= StreamerState.LOCKED
        await self.queue.task_done()
        await self.__stream_abort()
        self.state &= ~StreamerState.LOCKED
    
    async def send(self, data: np.ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            await self.queue.put(data)
            return True
        return False