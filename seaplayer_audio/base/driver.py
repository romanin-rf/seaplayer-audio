from abc import ABC, abstractmethod
from ..types import SamplerateType, DType, SAMPLERATE_VALUES, DTYPE_VALUES
from .exception import ErrorBase, ErrorTextType

# ! Exception
class DriverIsStoppedError(ErrorBase):
    def __error_text__(self, *args: object, **kwargs: object) -> ErrorTextType:
        yield "The driver has already been stopped!"

class DriverIsStartedError(ErrorBase):
    def __error_text__(self, *args: object, **kwargs: object) -> ErrorTextType:
        yield "The driver is already running!"

class DriverIsNotRunningError(ErrorBase):
    def __error_text__(self, *args: object, **kwargs: object) -> ErrorTextType:
        yield "The driver is not running!"

# ! Driver Base Class
class DriverBase(ABC):
    __driver_name__: str        = 'base'
    __driver_version__: str     = '1.0.0'
    
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
        pass
    
    @abstractmethod
    def stop(self) -> None:
        pass
    
    @abstractmethod
    def send(self, *args, **kwargs) -> None:
        pass
    
    # ! Spetific functions
    # ...