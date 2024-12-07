import datetime
from PIL import Image
from io import IOBase
from dataclasses import dataclass
from typing_extensions import Any, Iterable, Optional, NoReturn, deprecated
from .._types import (
    AudioSamplerate, AudioChannels, AudioSubType, AudioEndians, AudioFormat,
    Reprable
)

# ! Audio Source Types

@dataclass(frozen=True)
class AudioSourceMetadata:
    title: Optional[str]=None
    artist: Optional[str]=None
    album: Optional[str]=None
    tracknumber: Optional[str]=None
    date: Optional[datetime.datetime]=None
    genre: Optional[str]=None
    copyright: Optional[str]=None
    software: Optional[str]=None
    icon: Optional[Image.Image]=None

# ! Audio Source Class (sync)

class AudioSourceBase(IOBase, Reprable):
    """Base class for working with audio sources (sync)."""
    
    __slots__ = ('samplerate', 'channels', 'subtype', 'endian', 'format', 'frames')
    
    # ^ Variables
    
    samplerate: AudioSamplerate
    channels: AudioChannels
    subtype: AudioSubType
    endian: AudioEndians
    format: AudioFormat
    
    frames: int
    
    # ^ Methods
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def __iter__(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def __next__(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    def writable(self) -> bool:
        return False
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def write(self, *args, **kwargs) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise OSError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def writelines(self, lines: Iterable[Any]) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise OSError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def truncate(self, size: Optional[int]=None) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    def isatty(self) -> bool:
        return False
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def flush(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def fileno(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise OSError

# ! Audio Source Class (async)

class AsyncAudioSourceBase(AudioSourceBase):
    """Base class for working with audio sources (async)."""
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def __aiter__(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def __anext__(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    async def writable(self) -> bool:
        return False
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def write(self, *args, **kwargs) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise OSError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def writelines(self, lines: Iterable[Any]) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise OSError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def truncate(self, size = ...) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    async def isatty(self) -> bool:
        return False
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def flush(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def fileno(self) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise OSError