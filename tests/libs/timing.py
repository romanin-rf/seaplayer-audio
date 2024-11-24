import time
from typing import Any, Optional, Callable

# ! Types
class Timer:
    def __init__(self) -> None:
        self.__start_time: float = 0.0
        self.__end_time: float = 0.0
    
    def __enter__(self):
        self.__start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.__end_time = time.perf_counter()
    
    @property
    def timing(self) -> float:
        return self.__end_time - self.__start_time
    
    def start(self) -> None:
        self.__start_time = time.perf_counter()
    
    def end(self) -> None:
        self.__end_time = time.perf_counter()
    
    def abort(self) -> None:
        self.__start_time, self.__end_time = 0.0, 0.0
    
    def wrap(self, method: Optional[Callable[..., Any]]=None):
        if method is not None:
            def wrapped(*args, **kwargs) -> None:
                self.__start_time = time.perf_counter()
                result = method(*args, **kwargs)
                self.__end_time = time.perf_counter()
                return result
            return wrapped
        def wrapper(method: Callable[..., Any]) -> None:
            def wrapped(*args, **kwargs) -> None:
                self.__start_time = time.perf_counter()
                result = method(*args, **kwargs)
                self.__end_time = time.perf_counter()
                return result
            return wrapped
        return wrapper