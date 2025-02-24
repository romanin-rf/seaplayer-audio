import asyncio
from asyncio import AbstractEventLoop
from enum import Flag, auto
from types import TracebackType
from typing_extensions import Optional, Type
from .._types import AudioSamplerate, AudioChannels, AudioDType, Reprable

# ^ Streamer State Class

class StreamerState(Flag):
    RUNNING = auto()
    STARTED = auto()
    LOCKED = auto()
    WAITING = auto()

# ^ Streamer Base Class

class StreamerBase(Reprable):
    __steamer_type__: str  = 'base'
    
    __repr_attrs__          = ('samplerate', 'channels', 'dtype', 'state', 'closefd')
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True
    ) -> None:
        self.samplerate = samplerate or 44100
        self.channels = channels or 2
        self.dtype = dtype or 'float32'
        self.closefd = closefd
        self.state = StreamerState(0)
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ):
        if self.closefd:
            self.set_lock(True)
            self.abort()
            self.stop()
    
    def set_lock(self, __value: bool) -> None:
        if __value:
            self.state |= StreamerState.LOCKED
        else:
            self.state &= ~StreamerState.LOCKED
    
    def is_busy(self) -> bool:
        return False
    
    def reconfigure(self, 
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
    ) -> None:
        self.samplerate = samplerate if (samplerate is not None) else self.samplerate
        self.channels = channels if (channels is not None) else self.channels
        self.dtype = dtype if (dtype is not None) else self.dtype
    
    def run(self) -> None:
        raise NotImplementedError
    
    def abort(self) -> None:
        raise NotImplementedError
    
    def start(self) -> None:
        raise NotImplementedError
    
    def stop(self) -> None:
        raise NotImplementedError
    
    def send(self, data) -> bool:
        if StreamerState.LOCKED in self.state:
            return False
        return False

# ^ Async Streamer Base Class

class AsyncStreamerBase(StreamerBase):
    __steamer_type__: str = 'async-base'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        loop: Optional[AbstractEventLoop]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd)
        if loop is not None:
            self.loop = loop
        else:
            self.loop = asyncio.get_running_loop()
    
    def __enter__(self):
        raise NotImplementedError
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ):
        raise NotImplementedError
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ):
        if self.closefd:
            await self.set_lock(True)
            await self.abort()
            await self.stop()
    
    def set_lock(self, __value: bool) -> None:
        if __value:
            self.state |= StreamerState.LOCKED
        else:
            self.state &= ~StreamerState.LOCKED
    
    def is_busy(self) -> bool:
        return False
    
    def run(self) -> None:
        raise NotImplementedError
    
    async def abort(self) -> None:
        raise NotImplementedError
    
    async def start(self) -> None:
        raise NotImplementedError
    
    async def stop(self) -> None:
        raise NotImplementedError
    
    async def send(self, data) -> bool:
        if StreamerState.LOCKED in self.state:
            return False
        return False