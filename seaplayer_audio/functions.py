import mutagen
import asyncio
import inspect
import dateutil.parser
from PIL import Image
from pathlib import Path
from soundfile import SoundFile
from io import BufferedReader, BufferedRandom, BytesIO
from typing_extensions import (
    Dict,
    Optional, Union,
    Awaitable, Callable, Coroutine
)
from ._types import ResultType, MethodType
from .base import AudioSourceMetadata

# ! File Works Methods

def get_mutagen_info(
    file: Union[str, Path, BufferedReader, BufferedRandom]
) -> Optional[mutagen.FileType]:
    try: return mutagen.File(file)
    except: return

def get_audio_image(file: Optional[mutagen.FileType]) -> Optional[Image.Image]:
    if file is None:
        return None
    apic = file.get('APIC:', None) or file.get('APIC', None)
    if apic is None:
        return None
    return Image.open(BytesIO(apic.data))

def get_audio_metadata(io: SoundFile, file: Optional[mutagen.FileType]) -> AudioSourceMetadata:
    metadata = io.copy_metadata()
    year = check_string(metadata.get('date', None))
    if file is not None:
        icon = get_audio_image(file)
    else:
        icon = None
    try: date = dateutil.parser.parse(year) if (year is not None) else None
    except: date = None
    return AudioSourceMetadata(
        title=check_string(metadata.get('title', None)),
        artist=check_string(metadata.get('artist', None)),
        album=check_string(metadata.get('album', None)),
        tracknumber=check_string(metadata.get('tracknumber', None)),
        date=date,
        genre=check_string(metadata.get('genre', None)),
        copyright=check_string(metadata.get('copyright', None)),
        software=check_string(metadata.get('software', None)),
        icon=icon
    )

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