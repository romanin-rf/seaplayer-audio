from abc import ABC, abstractmethod
from typing_extensions import Generic
from ..types import SamplerateType, DType, SAMPLERATE_VALUES, DTYPE_VALUES, T
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