import datetime
from PIL import Image
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing_extensions import Optional, Tuple
from .driver import DriverBase
from ..types import DType, SamplerateType

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
    
    # ! Magic methods
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{attr_name}={repr(getattr(self,attr_name))}' for attr_name in self.__repr_attrs__])})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ! Propertyes
    
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        return None
    
    @property
    @abstractmethod
    def info(self) -> TrackInfo:
        return TrackInfo()
    
    @property
    @abstractmethod
    def dtype(self) -> Optional[DType]:
        return None
    
    @property
    @abstractmethod
    def samplerate(self) -> Optional[SamplerateType]:
        return None
    
    @property
    @abstractmethod
    def bitrate(self) -> Optional[int]:
        return None
    
    @property
    @abstractmethod
    def duration(self) -> float:
        return 0.0
    
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