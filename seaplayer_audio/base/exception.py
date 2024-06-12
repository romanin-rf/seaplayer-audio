from typing_extensions import Tuple, Dict
from ..types import ErrorTextType

# ! Error Base Class
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