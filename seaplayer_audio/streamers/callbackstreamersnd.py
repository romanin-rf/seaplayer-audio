import queue
import asyncio
import numpy as np
from enum import Flag, auto
from queue import Queue
from asyncio import AbstractEventLoop, Queue as AsyncQueue
from numpy import ndarray
from sounddevice import OutputStream, CallbackFlags
# > Typing
from typing_extensions import Any, Optional, NoReturn, Callable, deprecated
# > Local Imports
from .._types import AudioSamplerate, AudioChannels, AudioDType
from ..base import AsyncSoundDeviceStreamerBase, SoundDeviceStreamerBase, StreamerState

# ! Types

class CallbackSettingsFlag(Flag):
    FILL_ZEROS = auto()

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
        precallback: Optional[Callable[[int], Any]]=None,
        flag: Optional[CallbackSettingsFlag]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.queue: Queue[ndarray] = Queue(1)
        self.buffer: Optional[ndarray] = None
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback__
        )
        self.precallback = precallback if (precallback is not None) else (lambda frames: None)
        self.flag = flag if (flag is not None) else CallbackSettingsFlag(0)
    
    def __callback__(self, outdata: ndarray, frames: int, time, status: CallbackFlags):
        if self.buffer is not None:
            if len(self.buffer) == frames:
                wdata = self.buffer.copy()
                self.buffer = None
            elif len(self.buffer) > frames:
                wdata = self.buffer[:frames]
                self.buffer = self.buffer[frames:]
            else:
                self.precallback(frames - len(self.buffer))
                try:
                    qdata = self.queue.get_nowait()
                except queue.Empty:
                    return
                size = len(qdata) + len(self.buffer)
                if size > frames:
                    wdata = np.vstack( [self.buffer, qdata[:frames]], dtype=outdata.dtype )
                    self.buffer = qdata[frames:]
                elif size == frames:
                    wdata = np.vstack( [self.buffer, qdata], dtype=outdata.dtype )
                    self.buffer = None
                else:
                    if CallbackSettingsFlag.FILL_ZEROS in self.flag:
                        wdata = np.vstack([ self.buffer, qdata, np.zeros((frames - size, self.channels), dtype=outdata.dtype) ], dtype=outdata.dtype)
                        self.buffer = None
                    else:
                        self.buffer = np.vstack( [self.buffer, qdata], dtype=outdata.dtype )
                        return
        else:
            self.precallback(frames)
            try:
                qdata = self.queue.get_nowait()
            except queue.Empty:
                return
            size = len(qdata)
            if size == frames:
                wdata = qdata[:frames]
            elif size > frames:
                wdata = qdata[:frames]
                self.buffer = qdata[frames:]
            else:
                if CallbackSettingsFlag.FILL_ZEROS in self.flag:
                    wdata = np.vstack([ qdata, np.zeros((frames - size, self.channels), dtype=outdata.dtype) ], dtype=outdata.dtype)
                else:
                    self.buffer = qdata.copy()
                    return
        outdata[:] = wdata
    
    def is_busy(self) -> bool:
        return self.queue.qsize() >= 1
    
    def reconfigure(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        *,
        restore_state: bool=True
    ) -> None:
        super().reconfigure(samplerate, channels, dtype)
        state = self.state
        if StreamerState.RUNNING in self.state:
            self.stop()
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback__
        )
        self.buffer = None
        if restore_state and (StreamerState.RUNNING in state):
            self.start()
    
    @deprecated("NOT IMPLEMENTED")
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
            except ValueError: pass
            self.stream.stop()
    
    def abort(self):
        self.state |= StreamerState.LOCKED
        try: self.queue.task_done()
        except ValueError: pass
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
        device: Optional[int]=None,
        precallback: Optional[Callable[[int], Any]]=None,
        flag: Optional[CallbackSettingsFlag]=None
    ):
        super().__init__(samplerate, channels, dtype, closefd, loop, device)
        self.queue: AsyncQueue[ndarray] = AsyncQueue(1)
        self.buffer: Optional[ndarray] = None
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback__
        )
        self.precallback = precallback if (precallback is not None) else (lambda frames: None)
        self.flag = flag if (flag is not None) else CallbackSettingsFlag(0)
    
    def __callback__(self, outdata: ndarray, frames: int, time, status: CallbackFlags):
        if self.buffer is not None:
            if len(self.buffer) == frames:
                wdata = self.buffer.copy()
                self.buffer = None
            elif len(self.buffer) > frames:
                wdata = self.buffer[:frames]
                self.buffer = self.buffer[frames:]
            else:
                self.precallback(frames - len(self.buffer))
                try:
                    qdata = self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                size = len(qdata) + len(self.buffer)
                if size > frames:
                    wdata = np.vstack( [self.buffer, qdata[:frames]], dtype=outdata.dtype )
                    self.buffer = qdata[frames:]
                elif size == frames:
                    wdata = np.vstack( [self.buffer, qdata], dtype=outdata.dtype )
                    self.buffer = None
                else:
                    if CallbackSettingsFlag.FILL_ZEROS in self.flag:
                        wdata = np.vstack([ self.buffer, qdata, np.zeros((frames - size, self.channels), dtype=outdata.dtype) ], dtype=outdata.dtype)
                        self.buffer = None
                    else:
                        self.buffer = np.vstack( [self.buffer, qdata], dtype=outdata.dtype )
                        return
        else:
            self.precallback(frames)
            try:
                qdata = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            size = len(qdata)
            if size == frames:
                wdata = qdata.copy()
            if size > frames:
                wdata = qdata[:frames]
                self.buffer = qdata[frames:]
            else:
                if CallbackSettingsFlag.FILL_ZEROS in self.flag:
                    wdata = np.vstack([ qdata, np.zeros((frames - size, self.channels), dtype=outdata.dtype) ], dtype=outdata.dtype)
                else:
                    self.buffer = qdata.copy()
                    return
        outdata[:] = wdata
    
    def is_busy(self) -> bool:
        return self.queue.qsize() >= self.queue.maxsize
    
    def reconfigure(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        *,
        restore_state: bool=True
    ) -> None:
        super().reconfigure(samplerate, channels, dtype)
        state = self.state
        if StreamerState.RUNNING in self.state:
            asyncio.run_coroutine_threadsafe(self.stop(), self.loop).result()
        self.stream = OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self.__callback__
        )
        self.buffer = None
        if restore_state and (StreamerState.RUNNING in state):
            asyncio.run_coroutine_threadsafe(self.start(), self.loop).result()
    
    @deprecated("NOT IMPLEMENTED")
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
            try: self.queue.task_done()
            except ValueError: pass
            self.stream.stop()
    
    async def abort(self):
        self.state |= StreamerState.LOCKED
        try: self.queue.task_done()
        except ValueError: pass
        self.stream.abort()
        self.state &= ~StreamerState.LOCKED
    
    async def send(self, data: ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            await self.queue.put(data)
            return True
        return False