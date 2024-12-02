import os
import asyncio
import mutagen
import dateutil.parser
import numpy as np
import soundfile as sf
from PIL import Image
from io import BytesIO
# * Typing
from types import TracebackType
from typing_extensions import Optional, Type
# * Local Imports
from ..base import AsyncAudioSourceBase, AudioSourceBase, AudioSourceMetadata
from .._types import (
    FilePathType,
    AudioDType, AudioSamplerate, AudioChannels, AudioFormat, AudioSubType, AudioEndians
)
from ..functions import check_string, aiorun

# ^ File Audio Source (sync)

class FileAudioSource(AudioSourceBase):
    __repr_attrs__ = ('name', ('metadata', True), 'samplerate', 'channels', 'subtype', 'endian', 'format', 'bitrate')
    
    @staticmethod
    def _get_mutagen_info(__filepath: str) -> Optional[mutagen.FileType]:
        try: return mutagen.File(__filepath)
        except: return None
    
    @staticmethod
    def _get_image(__file: mutagen.FileType) -> Optional[Image.Image]:
        if __file is None:
            return None
        apic = __file.get('APIC:', None) or __file.get('APIC', None)
        if apic is None:
            return None
        return Image.open(BytesIO(apic.data))
    
    @staticmethod
    def _get_info(__io: sf.SoundFile, __file: Optional[mutagen.FileType]) -> AudioSourceMetadata:
        if __file is not None:
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
                icon=FileAudioSource._get_image(__file)
            )
        return AudioSourceMetadata()
    
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
        self.name = os.path.abspath(str(filepath))
        self.sfio = sf.SoundFile(self.name, 'r', samplerate, channels, subtype, endian, format)
        self.minfo = self._get_mutagen_info(self.name)
        self.metadata = self._get_info(self.sfio, self.minfo)
        self.closefd = closefd
    
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
        return self.sfio.samplerate
    
    @property
    def channels(self) -> AudioChannels:
        return self.sfio.channels
    
    @property
    def subtype(self) -> AudioSubType:
        return self.sfio.subtype
    
    @property
    def endian(self) -> AudioEndians:
        return self.sfio.endian
    
    @property
    def format(self) -> AudioFormat:
        return self.sfio.format
    
    @property
    def bitrate(self) -> Optional[int]:
        if self.minfo is not None:
            if self.minfo.info is not None:
                return self.minfo.info.bitrate
        return None
    
    @property
    def closed(self) -> bool:
        return self.sfio.closed
    
    # ^ IO Methods Tests
    
    def seekable(self) -> bool:
        return self.sfio.seekable() and not self.closed
    
    def readable(self) -> bool:
        return not self.closed
    
    # ^ IO Methods Action
    
    def read(
        self,
        frames: int=-1,
        dtype: AudioDType='float32',
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
        return self.sfio.read(frames, dtype, always_2d, **extra)
    
    def readline(self, seconds: float=-1.0, dtype: AudioDType='float32', always_2d: bool=False, **extra: object):
        """Read from the file and return data (*1 second*) as NumPy array.

        Args:
            seconds (int, optional): The second of to read. Defaults to `-1`.

        Returns:
            np.ndarray: If out is specified, the data is written into the given array instead of creating a new array. In this case, the arguments *dtype* and *always_2d* are silently ignored! If *frames* is not given, it is obtained from the length of out.
        """
        return self.sfio.read(int(seconds * self.sfio.samplerate), dtype, always_2d, **extra)
    
    def seek(self, frames: int, whence=0) -> int:
        """Set the read position.

        Args:
            frames (int): The frame index or offset to seek.
            whence ({0, 1, 2}, optional): `0` - SET, `1` - CURRENT, `2` - END. Defaults to `0`.

        Raises:
            ValueError: Invalid `whence` argument is specified.

        Returns:
            int: The new absolute read position in frames.
        """
        return self.sfio.seek(frames, whence)
    
    def tell(self) -> int:
        """Return the current read position.

        Returns:
            int: Current position.
        """
        return self.sfio.tell()
    
    def close(self) -> None:
        """Close the file. Can be called multiple times."""
        return self.sfio.close()


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
        super().__init__(filepath, samplerate, channels, subtype, endian, format, closefd)
        if loop is not None:
            self.loop = loop
        else:
            self.loop = asyncio.get_running_loop()
    
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
        dtype: AudioDType='float32',
        always_2d: bool=False,
        **extra: object
    ) -> np.ndarray:
        return await aiorun(self.loop, super().read, frames, dtype, always_2d, **extra)
    
    async def readline(self, seconds: float=-1.0, dtype: AudioDType='float32', always_2d: bool=False, **extra):
        return await aiorun(self.loop, super().readline, seconds, dtype, always_2d, **extra)

    async def seek(self, frames: int, whence=0) -> int:
        return await aiorun(self.loop, super().seek, frames, whence)
    
    async def tell(self) -> int:
        return await aiorun(self.loop, super().tell)
    
    async def close(self) -> None:
        return await aiorun(self.loop, super().close)