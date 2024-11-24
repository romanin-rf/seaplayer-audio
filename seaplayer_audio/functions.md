# Roadmap `"Async Wrapping"`

### Examples
- **Async-threaded method**
```python
import asyncio
import inspect
from typing_extensions import (
    Union,
    Awaitable, Callable, Coroutine,
    TypeVar
)

ResultType = TypeVar('ResultType')
MethodType: TypeAlias = Union[
    Awaitable[ResultType],
    Callable[[], Coroutine[None, None, ResultType]],
    Callable[[], ResultType]
]

def run_awaitable(method: Awaitable[ResultType]) -> ResultType:
    """Await the awaitable."""
    async def do_work() -> ResultType:
        return await work
    return asyncio.run(do_work())

def run_coroutine(
    method: Callable[[], Coroutine[None, None, ResultType]],
) -> ResultType:
    """Await coroutine."""
    return run_awaitable(work())

def run_callable(method: Callable[[], ResultType]) -> ResultType:
    """Call the callable."""
    return work()


async def aiorun(method: MethodType):
    if inspect.iscoroutinefunction(method):
        runner = run_coroutine
    elif inspect.isawaitable(method):
        runner = run_awaitable
    elif callable(method):
        runner = run_callable
    else:
        raise RuntimeError
    loop = asyncio.get_running_loop()
    assert loop is not None
    return await loop.run_in_executor(None, runner, method)
```