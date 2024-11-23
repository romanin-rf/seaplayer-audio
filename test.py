import datetime
from PIL import Image
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing_extensions import (
    TypeVar, TypeAlias, Generic,
    Literal, Union, Optional, Generator,
    Dict, Tuple, Any
)

# ! Type Vars

T = TypeVar('T')

# ! Types

ErrorTextType: TypeAlias            = Generator[str, Any, None]

# ! Audio Types

SamplerateType: TypeAlias           = Literal[8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000]
"""A type with all possible `samplerate` options."""
SAMPLERATE_VALUES                   = (8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000)
"""A constant with the listed possible `samplerate` options."""

LiteralIntDType: TypeAlias          = Literal['int8', 'int16', 'int32', 'int64', 'int128', 'int256']
"""Literals of possible `dtype` values for `int`."""
LiteralFloatDType: TypeAlias        = Literal['float16', 'float32', 'float64', 'float80', 'float96', 'float128', 'float256']
"""Literals of possible `dtype` values for `float`."""
DType: TypeAlias                    = Union[LiteralIntDType, LiteralFloatDType]
"""Literals of possible `dtype` values."""
DTYPE_INT_VALUES                    = ('int8', 'int16', 'int32', 'int64', 'int128', 'int256')
DTYPE_FLOAT_VALUES                  = ('float16', 'float32', 'float64', 'float80', 'float96', 'float128', 'float256')
DTYPE_VALUES                        = (*DTYPE_INT_VALUES, *DTYPE_FLOAT_VALUES)

# ! Exception Base

class ErrorBase(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__()
        self.__error_init__()
        self.args = tuple(text for text in self.__error_text__())
        self.arguments: Tuple[object, ...] = args
        self.kwarguments: Dict[str, object] = kwargs
    
    def __error_init__(self, *args: object, **kwargs: object) -> None:
        pass
    
    def __error_text__(self, *args: object, **kwargs: object) -> ErrorTextType:
        yield "The text of the base error."

# ! Driver Base

class DriverBase(ABC, Generic[T]):
    __driver_name__: str        = 'base'
    __driver_version__: str     = '0.1.0'
    
    def __init__(
        self,
        samplerate: SamplerateType=44100,
        dtype: DType='float32',
        *args, **kwargs
    ) -> None:
        assert samplerate in SAMPLERATE_VALUES
        assert dtype in DTYPE_VALUES
        self.__samplerate = samplerate
        self.__dtype = dtype
    
    # ! Propertyes
    
    @property
    @abstractmethod
    def samplerate(self) -> SamplerateType:
        return self.__samplerate
    
    @property
    @abstractmethod
    def dtype(self) -> DType:
        return self.__dtype
    
    @property
    @abstractmethod
    def running(self) -> bool:
        return False
    
    # ! Initialization
    
    @abstractmethod
    def __driver_loop__(self) -> None:
        pass
    
    # ! Functions
    
    @abstractmethod
    def start(self) -> None:
        """Starting the driver."""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stopping the driver operation."""
        pass
    
    @abstractmethod
    def send(self, data: T, *args, **kwargs) -> None:
        """Sending data (the entire implementation will be in a class inherited from this class).

        Args:
            data (T): It can be either bytes or an array of values
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clearing (the entire implementation will be in a class inherited from this class)."""
        pass
    
    # ! Spetific functions
    # ...

# ! Track Base

# ! Track Info Base Class
@dataclass
class TrackInfo:
    title: Optional[str]=None
    artist: Optional[str]=None
    album: Optional[str]=None
    tracknumber: Optional[str]=None
    date: Optional[datetime.datetime]=None
    genre: Optional[str]=None
    copyright: Optional[str]=None
    software: Optional[str]=None
    icon: Optional[Image.Image]=None

# ! Track Base Class
class TrackBase(ABC):
    __track_format__: str = "base"
    __repr_attrs__: Tuple[str, ...] = ('name', 'info', 'dtype', 'samplerate', 'bitrate', 'duration')
    
    # ! Initialization
    
    def __init__(self, driver: DriverBase, *args: object, **kwargs: object) -> None:
        self._driver = driver
        self.args, self.kwargs = args, kwargs
        self._name, self._info, self._dtype, self._samplerate, self._bitrate, self._duration, self._playing, self._paused = [...]
    
    # ! Magic methods
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{attr_name}={repr(getattr(self,attr_name))}' for attr_name in self.__repr_attrs__])})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ! Propertyes
    
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        return self._name
    
    @property
    @abstractmethod
    def info(self) -> TrackInfo:
        return self._info
    
    @property
    @abstractmethod
    def dtype(self) -> Optional[DType]:
        return self._dtype
    
    @property
    @abstractmethod
    def samplerate(self) -> Optional[SamplerateType]:
        return self._samplerate
    
    @property
    @abstractmethod
    def bitrate(self) -> Optional[int]:
        return self._bitrate
    
    @property
    @abstractmethod
    def duration(self) -> float:
        return self._duration
    
    @property
    @abstractmethod
    def playing(self) -> bool:
        return False
    
    @property
    @abstractmethod
    def paused(self) -> bool:
        return False
    
    # ! Private methods
    
    # ! Track initializiton methods
    
    @abstractmethod
    def is_filepath_track_format(self) -> bool:
        return False
    
    # ! Track methods
    
    @abstractmethod
    def play(self) -> None:
        pass
    
    @abstractmethod
    def pause(self) -> None:
        pass
    
    @abstractmethod
    def unpause(self) -> None:
        pass

# ! MP3 Track

class MP3Track(TrackBase):
    __track_format__ = 'mpeg'
    
    def __init__(self, driver: DriverBase) -> None:
        super().__init__(driver)