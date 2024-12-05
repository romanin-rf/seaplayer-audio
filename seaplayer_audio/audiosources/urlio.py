from urllib.request import urlopen
from tempfile import TemporaryFile
from io import IOBase, BufferedReader, BytesIO, DEFAULT_BUFFER_SIZE
from typing_extensions import (
    Iterable,
    Self,
    Literal, Optional, 
    NoReturn, deprecated
)
from .._types import URLOpenRet

# ! URL IO Class
class URLIO(BufferedReader):
    # ^ Hidden init methods
    
    def __open_buffer(self, buffer_type: Literal['temp', 'mem']) -> BufferedReader:
        if buffer_type == 'mem':
            return BytesIO()
        elif buffer_type == 'temp':
            return TemporaryFile('wb+')
        raise ValueError(buffer_type)
    
    def __getsize(self) -> int:
        ct = self.tell()
        size = self.__buffer.seek(0, 2)
        self.__buffer.seek(ct)
        return size
    
    def __topload(self, size: int) -> None:
        if not self.__full:
            ct = self.__buffer.tell()
            data = self.__stream.read(size)
            if len(data) != size:
                self.__full = True
                self.__stream.close()
            self.__buffer.seek(0, 2)
            self.__buffer.write(data)
            self.__buffer.seek(ct)
    
    def __fullload(self) -> None:
        if not self.__full:
            ct = self.__buffer.tell()
            self.__buffer.seek(0, 2)
            while len(data := self.__stream.read(DEFAULT_BUFFER_SIZE)) > 0:
                self.__buffer.write(data)
            self.__stream.close()
            self.__full = True
            self.__buffer.seek(ct)
    
    def __read_preparation(self, size: int) -> None:
        if not self.__full:
            if size > 0:
                s = size - (self.__getsize() - self.__buffer.tell())
                if s > 0:
                    self.__topload(s)
            elif size <= 0:
                self.__fullload()
    
    def __seek_preparation(self, offset: int, whence: int) -> None:
        if (not self.__full) and (offset > 0):
            if whence == 0:
                s = self.__getsize() - offset
                if s > 0:
                    self.__topload(s)
            elif whence == 1:
                s = offset - (self.__getsize() - self.__buffer.tell())
                if s > 0:
                    self.__topload(s)
            elif whence == 2:
                if (self.length is not None) and (self.length != 0):
                    s = self.length - self.__getsize() - offset
                    if s > 0:
                        self.__topload(s)
                    else:
                        self.__fullload()
                else:
                    self.__fullload()
    
    # ^ Init Method
    
    def __init__(
        self,
        url: str,
        buffer_type: Literal['temp', 'mem']='temp',
        closefd: bool=True
    ) -> None:
        self.__url = url
        self.__buffer_type = buffer_type
        self.__closefd = closefd
        # * URL IO Attrs
        self.__stream: URLOpenRet = urlopen(self.__url)
        self.__buffer = self.__open_buffer(self.__buffer_type)
        self.__full = False
        print(f"[  DIR ]: {dir(self)}")
    
    # ^ Magic Methods
    
    def __getattribute__(self, item: str):
        __class_name__ = super().__getattribute__('__class__').__name__
        print(f'[ CALL ]: {__class_name__}.{item}')
        return super().__getattribute__(item)
    
    def __del__(self) -> None:
        if self.closefd and (not self.closed):
            self.close()
    
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
    def name(self) -> Optional[str]:
        return None
    
    @property
    def mode(self) -> str:
        return 'r'
    
    @property
    def closed(self) -> bool:
        return self.__buffer.closed
    
    @property
    def closefd(self) -> bool:
        return self.__closefd
    
    # ^ URL Open Propertyes
    
    @property
    def length(self) -> Optional[int]:
        if hasattr(self.__stream):
            if isinstance(self.__stream.length, int):
                return self.__stream.length
        return None
    
    # ^ URL IO Propertyes
    
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def downloaded(self) -> int:
        return self.__getsize()
    
    @property
    def buffer_type(self) -> Literal['temp', 'mem']:
        return self.__buffer_type
    
    @property
    def full(self) -> bool:
        return self.__full
    
    # ^ URL IO Methods
    
    def fulling(self) -> None:
        return self.__fullload()
    
    # ^ IO Check Methods
    
    def seekable(self) -> bool:
        return not self.closed
    
    def readable(self) -> bool:
        return not self.closed
    
    def writable(self) -> bool:
        return False
    
    # ^ IO Methods
    
    def isatty(self) -> bool:
        return False
    
    def tell(self) -> int:
        return self.__buffer.tell()
    
    def close(self) -> None:
        if not self.full:
            self.__stream.close()
            self.__buffer.close()
    
    def read(self, size: int=-1, /) -> bytes:
        self.__read_preparation(size)
        return self.__buffer.read(size)
    
    def read1(self, size: int=-1, /) -> bytes:
        self.__read_preparation(size)
        return self.__buffer.read1(size)
    
    def readinto(self, b: bytearray, /) -> int:
        size = len(b)
        if size > 0:
            self.__read_preparation(size)
            return self.__buffer.readinto(b)
        return 0
    
    def readinto1(self, b: bytearray, /) -> int:
        size = len(b)
        if size > 0:
            self.__read_preparation(size)
            return self.__buffer.readinto1(b)
        return 0
    
    def seek(self, offset: int, whence: int=0, /) -> int:
        self.__seek_preparation(offset, whence)
        return self.__buffer.seek(offset, whence)
    
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
    
    @deprecated('!!! NOT IMPLEMENTED !!!')
    def flush(self):
        raise NotImplementedError