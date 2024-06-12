import datetime
from PIL import Image
from dataclasses import dataclass
from typing_extensions import Optional
from .driver import DriverBase

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
class TrackBase:
    # ! Initialization
    
    def __init__(self, driver: DriverBase, *args, **kwargs) -> None:
        pass
    
    # ! Magic methods
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ! Propertyes
    @property
    def name(self) -> Optional[str]:
        return None
    
    @property
    def info(self) -> TrackInfo:
        return TrackInfo()
    
    # ! Private methods
    
    # ! Track initializiton methods
    
    # ! Track methods
    