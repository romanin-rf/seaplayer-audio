import os
import asyncio
import mutagen
import dateutil.parser
import numpy as np
import soundfile as sf
from PIL import Image
from io import BytesIO
# * Typing
#from enum import Flag, auto
from types import TracebackType
from typing_extensions import Optional, Type
# * Local Imports
from ..base import AsyncAudioSourceBase, AudioSourceBase, AudioSourceMetadata
from ..types import (
    FilePathType,
    SeekWhenceType,
    AudioDType, AudioSamplerate, AudioChannels, AudioFormat, AudioSubType, AudioEndians
)
from ..functions import check_string, aiorun

# ^ File Audio Source (sync)

class FileAudioSource(AudioSourceBase):
    __repr_attrs__ = ('name', 'samplerate', 'channels', 'subtype', 'endian', 'format')
    
    @staticmethod
    def _get_mutagen_info(__filepath: str) -> Optional[mutagen.FileType]:
        try: return mutagen.File(__filepath)
        except: return
    
    @staticmethod
    def _get_image(__filepath: str) -> Optional[Image.Image]:
        file = FileAudioSource._get_mutagen_info(__filepath)
        if file is None:
            return
        apic = file.get('APIC:', None) or file.get('APIC', None)
        if apic is None:
            return
        return Image.open(BytesIO(apic.data))
    
    @staticmethod
    def _get_info(__io: sf.SoundFile) -> AudioSourceMetadata:
        metadata = __io.copy_metadata()
        year = check_string(metadata.get('date', None))
        try:
            date = dateutil.parser.parse(year) if (year is not None) else None
        except:
            date = None
        return AudioSourceMetadata(
            title=check_string(metadata.get('title', None)),
            artist=check_string(metadata.get('artist', None)),
            album=check_string(metadata.get('album', None)),
            tracknumber=check_string(metadata.get('tracknumber', None)),
            date=date,
            genre=check_string(metadata.get('genre', None)),
            copyright=check_string(metadata.get('copyright', None)),
            software=check_string(metadata.get('software', None)),
            icon=FileAudioSource._get_image(__io.name)
        )
    
    def __init__(
        self,
        filepath: FilePathType,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        subtype:  Optional[AudioSubType]=None,
        endian: Optional[AudioEndians]=None,
        format: Optional[AudioFormat]=None,
        closefd: bool=False
    ) -> None:
        self.closefd = closefd
        self.name = os.path.abspath(str(filepath))
        self._io = sf.SoundFile(self.name, 'r', samplerate, channels, subtype, endian, format)
        self.info = self._get_info(self._io)
    
    # ^ Magic Methods
    
    def __enter__(self):
        return self
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        if self.closefd:
            self.close()
    
    def __del__(self) -> None:
        self.close()
    
    # ^ Propertyes
    
    @property
    def samplerate(self) -> AudioSamplerate:
        return self._io.samplerate
    
    @property
    def channels(self) -> AudioChannels:
        return self._io.channels
    
    @property
    def subtype(self) -> AudioSubType:
        return self._io.subtype
    
    @property
    def endian(self) -> AudioEndians:
        return self._io.endian
    
    @property
    def format(self) -> AudioFormat:
        return self._io.format
    
    @property
    def closed(self) -> bool:
        return self._io.closed
    
    # ^ IO Methods Tests
    
    def seekable(self) -> bool:
        return self._io.seekable() and not self.closed
    
    def readable(self) -> bool:
        return not self.closed
    
    # ^ IO Methods Action
    
    def read(
        self,
        frames: int=-1,
        dtype: AudioDType='int16',
        always_2d: bool=False,
        **extra: object
    ) -> np.ndarray:
        """Read from the file and return data as NumPy array.

        Args:
            frames (int, optional): The number of frames to read. If `frames < 0`, the whole rest of the file is read. Defaults to `-1`.
            dtype ({'int16', 'int32', 'float32', 'float64'}, optional): Data type of the returned array. Defaults to `'int16'`.
            always_2d (bool, optional): With `always_2d=True`, audio data is always returned as a two-dimensional array, even if the audio file has only one channel. Defaults to `False`.
        
        Raises:
            ValueError: The `dtype` value is incorrect.

        Returns:
            np.ndarray: If out is specified, the data is written into the given array instead of creating a new array. In this case, the arguments *dtype* and *always_2d* are silently ignored! If *frames* is not given, it is obtained from the length of out.
        """
        if dtype not in AudioDType.__args__:
            raise ValueError(f"Bad value: {dtype=}.")
        return self._io.read(frames, dtype, always_2d, **extra)
    
    def seek(self, frames: int, whence: SeekWhenceType=0) -> int:
        """Set the read position.

        Args:
            frames (int): The frame index or offset to seek.
            whence ({0, 1, 2}, optional): `0` - SET, `1` - CURRENT, `2` - END. Defaults to `0`.

        Raises:
            ValueError: Invalid `whence` argument is specified.

        Returns:
            int: The new absolute read position in frames.
        """
        if whence not in SeekWhenceType.__args__:
            raise ValueError(f"Bad value: {whence=}.")
        return self._io.seek(frames, whence)
    
    def tell(self) -> int:
        """Return the current read position.

        Returns:
            int: Current position.
        """
        return self._io.tell()
    
    def close(self) -> None:
        """Close the file. Can be called multiple times."""
        return self._io.close()


class AsyncFileAudioSource(AsyncAudioSourceBase, FileAudioSource):
    def __init__(
        self,
        filepath: FilePathType,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        subtype:  Optional[AudioSubType]=None,
        endian: Optional[AudioEndians]=None,
        format: Optional[AudioFormat]=None,
        closefd: bool=False,
        loop: Optional[asyncio.AbstractEventLoop]=None
    ) -> None:
        self.closefd = closefd
        self.loop = loop or asyncio.get_running_loop()
        self.name = os.path.abspath(str(filepath))
        self._io = sf.SoundFile(self.name, 'r', samplerate, channels, subtype, endian, format)
        self.info = self._get_info(self._io)
    
    def __del__(self) -> None:
        super().close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        if self.closefd:
            await self.close()

    async def seekable(self):
        return super().seekable()
    
    async def readable(self):
        return not self.closed

    async def read(
        self,
        frames: int=-1,
        dtype: AudioDType='int16',
        always_2d: bool=False,
        **extra: object
    ) -> np.ndarray:
        return await aiorun(self.loop, super().read, frames, dtype, always_2d, **extra)

    async def seek(self, frames: int, whence: SeekWhenceType=0) -> int:
        return await aiorun(self.loop, super().seek, frames, whence)
    
    async def tell(self) -> int:
        return await aiorun(self.loop, super().tell)
    
    async def close(self):
        return await aiorun(self.loop, super().close)