import os
import asyncio
import mutagen
import dateutil.parser
import numpy as np
import soundfile as sf
from PIL import Image
from io import BytesIO, IOBase
from tempfile import TemporaryFile
from httpx import Client, AsyncClient
from typing_extensions import (
    Iterable,
    Literal,
    Self, NoReturn, deprecated
)

# ! URL IO Class
class URLIO(IOBase):
    # ^ Hidden init methods
    
    def __open_buffer(self, buffer_mode: Literal['temp', 'mem']):
        if buffer_mode == 'mem':
            return BytesIO()
        elif buffer_mode == 'temp':
            return TemporaryFile('rb+')
        raise ValueError(buffer_mode)
    
    # ^ Init Method
    
    def __init__(
        self,
        url: str,
        buffer_mode: Literal['temp', 'mem']='temp',
        closefd: bool=True
    ) -> None:
        self.__url = url
        self.__buffer_mode = buffer_mode
        self.__closefd = closefd
        # * IO Attrs
        self.__tell = 0
        self.__closed = False
        # * URL IO Attrs
        self.__buffer = self.__open_buffer(self.__buffer_mode)
        self.__full = False
    
    # ^ Magic Methods
    
    def __iter__(self) -> NoReturn:
        raise NotImplementedError
    
    def __next__(self) -> NoReturn:
        raise NotImplementedError
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, *args) -> None:
        if self.closefd and (not self.closed):
            self.close()
    
    # ^ Main Propertyes
    
    @property
    def name(self) -> str:
        return self.__url
    
    @property
    def closed(self) -> bool:
        return self.__closed
    
    @property
    def closefd(self) -> bool:
        return self.__closefd
    
    # ^ URL IO Propertyes
    
    @property
    def buffer_mode(self) -> Literal['temp', 'mem']:
        return self.__buffer_mode
    
    @property
    def full(self) -> bool:
        return self.__full
    
    # ^ Check Methods
    
    def seekable(self) -> bool:
        return not self.closed
    
    def readable(self) -> bool:
        return not self.closed
    
    def writable(self) -> bool:
        return False
    
    # ^ IO Methods
    
    def tell(self) -> int:
        return self.__tell
    
    def close(self) -> None:
        pass
    
    # ^ IO Methods (NOT IMPLEMENTED)
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def write(self):
        raise OSError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def writelines(self, lines: Iterable[bytes], /):
        raise OSError
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def fileno(self):
        raise OSError
    
    
    #def __iter__(self) -> Iterator[bytes]: ...
    #def __next__(self) -> bytes: ...
    #def __enter__(self) -> Self: ...
    #def __exit__(
    #    self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    #) -> None: ...
    #def close(self) -> None: ...
    #def fileno(self) -> int: ...
    #def flush(self) -> None: ...
    #def isatty(self) -> bool: ...
    #def readable(self) -> bool: ...
    #read: Callable[..., Any]
    #def readlines(self, hint: int = -1, /) -> list[bytes]: ...
    #def seek(self, offset: int, whence: int = ..., /) -> int: ...
    #def seekable(self) -> bool: ...
    #def tell(self) -> int: ...
    #def truncate(self, size: int | None = ..., /) -> int: ...
    #def writable(self) -> bool: ...
    #write: Callable[..., Any]
    #def writelines(self, lines: Iterable[ReadableBuffer], /) -> None: ...
    #def readline(self, size: int | None = -1, /) -> bytes: ...
    #def __del__(self) -> None: ...
    #@property
    #def closed(self) -> bool: ...
    #def _checkClosed(self) -> None: ...  # undocumented