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
class DriverBase:
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
    def samplerate(self) -> SamplerateType:
        return self.__samplerate
    
    @property
    def dtype(self) -> DType:
        return self.__dtype
    
    @property
    def running(self) -> bool:
        return False
    
    # ! Initialization
    
    def __driver_loop__(self) -> None:
        pass
    
    # ! Functions
    
    def start(self) -> None:
        raise NotImplementedError()
    
    def stop(self) -> None:
        raise NotImplementedError()
    
    def send(self, *args, **kwargs) -> None:
        raise NotImplementedError()
    
    # ! Spetific functions
    # ...