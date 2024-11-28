import mutagen
import asyncio
import inspect
from typing_extensions import (
    Dict,
    Optional,
    Awaitable, Callable, Coroutine
)
from ._types import ResultType, MethodType

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

def _aiorun_awaitable(
    method: Awaitable[ResultType],
    kwargs: Dict[str, object], *args
) -> ResultType:
    """Await the awaitable."""
    async def do_work() -> ResultType:
        return await method
    return asyncio.run(do_work())

def _aiorun_coroutine(
    method: Callable[..., Coroutine[None, None, ResultType]],
    kwargs: Dict[str, object], *args
) -> ResultType:
    """Await coroutine."""
    return _aiorun_awaitable(method(*args, **kwargs))

def _aiorun_callable(
    method: Callable[..., ResultType],
    kwargs: Dict[str, object], *args
) -> ResultType:
    """Call the callable."""
    return method(*args, **kwargs)

def aiowrap(loop: asyncio.AbstractEventLoop, method: MethodType):
    if inspect.iscoroutinefunction(method):
        runner = _aiorun_coroutine
    elif inspect.isawaitable(method):
        runner = _aiorun_awaitable
    elif callable(method):
        runner = _aiorun_callable
    else:
        raise RuntimeError
    async def wrapped(*args, **kwargs):
        return await loop.run_in_executor(None, runner, method, kwargs, *args)
    return wrapped

async def aiorun(
    loop: asyncio.AbstractEventLoop,
    method: MethodType,
    *args, **kwargs
) -> ResultType:
    if inspect.iscoroutinefunction(method):
        runner = _aiorun_coroutine
    elif inspect.isawaitable(method):
        runner = _aiorun_awaitable
    elif callable(method):
        runner = _aiorun_callable
    else:
        raise RuntimeError
    assert loop is not None
    return await loop.run_in_executor(None, runner, method, kwargs, *args)