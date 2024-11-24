import datetime
from PIL import Image
from io import IOBase
from dataclasses import dataclass
from typing_extensions import Tuple, Any, Iterable, Optional, NoReturn, deprecated

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
    
    __repr_attrs__: Tuple[str, ...] = ()
    
    def __str__(self) -> str:
        attrs = ', '.join([f"{attrname}={getattr(self, attrname)!r}" for attrname in self.__repr_attrs__])
        return f"{self.__class__.__name__}({attrs})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
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
        raise NotImplementedError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def writelines(self, lines: Iterable[Any]) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
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
        raise NotImplementedError

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
        raise NotImplementedError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    async def writelines(self, lines: Iterable[Any]) -> NoReturn:
        """!!! NOT IMPLEMENTED !!!"""
        raise NotImplementedError
    
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
        raise NotImplementedError