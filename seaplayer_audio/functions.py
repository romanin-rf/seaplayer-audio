import mutagen
import asyncio
import inspect
from typing_extensions import (
    Dict,
    Optional, Union,
    Awaitable, Callable, Coroutine
)
from .types import ResultType

# ! File Works Methods

def get_mutagen_info(filepath: str) -> Optional[mutagen.FileType]:
    try: return mutagen.File(filepath)
    except: return

# ! Formatiing Methods

def check_string(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if (len(value.replace(' ', '')) == 0):
            return None
    return value

# ! Async Wrrapper

def run_awaitable(
    method: Awaitable[ResultType],
    kwargs: Dict[str, object], *args
) -> ResultType:
    """Await the awaitable."""
    async def do_work() -> ResultType:
        return await method
    return asyncio.run(do_work())

def run_coroutine(
    method: Callable[..., Coroutine[None, None, ResultType]],
    kwargs: Dict[str, object], *args
) -> ResultType:
    """Await coroutine."""
    return run_awaitable(method(*args, **kwargs))

def run_callable(
    method: Callable[..., ResultType],
    kwargs: Dict[str, object], *args
) -> ResultType:
    """Call the callable."""
    return method(*args, **kwargs)

async def aiorun(
    loop: asyncio.AbstractEventLoop,
    method: Union[
        Awaitable[ResultType],
        Callable[..., Coroutine[None, None, ResultType]],
        Callable[..., ResultType]
    ],
    *args, **kwargs
) -> ResultType:
    if inspect.iscoroutinefunction(method):
        runner = run_coroutine
    elif callable(method):
        runner = run_callable
    elif inspect.isawaitable(method):
        runner = run_awaitable
    else:
        raise RuntimeError
    assert loop is not None
    return await loop.run_in_executor(None, runner, method, kwargs, *args)