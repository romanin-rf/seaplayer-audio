import datetime
from PIL import Image
from io import IOBase
from dataclasses import dataclass
from typing_extensions import Optional, NoReturn, deprecated

# ! Audio Source Types

@dataclass
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

class AudioSourceBase(IOBase):
    """Base class for working with audio sources (sync)."""
    
    @deprecated('NOT IMPLEMENTED')
    def __iter__(self) -> NoReturn:
        raise NotImplementedError
    
    @deprecated('NOT IMPLEMENTED')
    def __next__(self) -> NoReturn:
        raise NotImplementedError
    
    def writable(self) -> bool:
        return False
    
    @deprecated('NOT IMPLEMENTED')
    def write(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError

# ! Audio Source Class (async)

class AsyncAudioSourceBase(AudioSourceBase):
    """Base class for working with audio sources (async)."""
    
    @deprecated('NOT IMPLEMENTED')
    async def __aiter__(self) -> NoReturn:
        raise NotImplementedError
    
    @deprecated('NOT IMPLEMENTED')
    async def __anext__(self) -> NoReturn:
        raise NotImplementedError
    
    async def writable(self) -> bool:
        return False
    
    @deprecated('NOT IMPLEMENTED')
    async def write(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError