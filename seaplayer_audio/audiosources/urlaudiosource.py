from numpy import ndarray
from soundfile import SoundFile
from typing_extensions import Optional
from .._types import AudioSamplerate, AudioChannels, AudioSubType, AudioFormat, AudioEndians, AudioDType
from ..base import AudioSourceBase
from ..functions import get_mutagen_info, get_audio_metadata
from .urlio import URLIO

# ! URL Audio Source Class
class URLAudioSource(AudioSourceBase):
    __repr_attrs__ = ('name', ('metadata', True), 'samplerate', 'channels', 'subtype', 'endian', 'format', 'bitrate')
    
    def __init__(
        self,
        url: str,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        subtype:  Optional[AudioSubType]=None,
        endian: Optional[AudioEndians]=None,
        format: Optional[AudioFormat]=None,
        closefd: bool=True
    ):
        self.name = None
        self.url = url
        self.urlio = URLIO(url, closefd=closefd)
        self.sfio = SoundFile(self.urlio, 'r', samplerate, channels, subtype, endian, format, closefd=closefd)
        self.minfo = get_mutagen_info(self.name)
        self.metadata = get_audio_metadata(self.sfio, self.minfo)
    
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
        try:    return self.minfo.info.bitrate
        except: return None
    
    @property
    def closed(self) -> bool:
        return self.sfio.closed
    
    # ^ IO Check Methods
    
    def seekable(self) -> bool:
        return self.sfio.seekable() and not self.closed
    
    def readable(self) -> bool:
        return not self.closed
    
    # ^ IO Check Methods
    
    def read(
        self,
        frames: int=-1,
        dtype: AudioDType='float32',
        always_2d: bool=False,
        **extra: object
    ) -> ndarray:
        """Read from the file and return data as NumPy array.

        Args:
            frames (int, optional): The number of frames to read. If `frames < 0`, the whole rest of the file is read. Defaults to `-1`.
            dtype ({'int16', 'int32', 'float32', 'float64'}, optional): Data type of the returned array. Defaults to `'int16'`.
            always_2d (bool, optional): With `always_2d=True`, audio data is always returned as a two-dimensional array, even if the audio file has only one channel. Defaults to `False`.
        
        Raises:
            ValueError: The `dtype` value is incorrect.

        Returns:
            ndarray: If out is specified, the data is written into the given array instead of creating a new array. In this case, the arguments *dtype* and *always_2d* are silently ignored! If *frames* is not given, it is obtained from the length of out.
        """
        return self.sfio.read(frames, dtype, always_2d, **extra)
    
    def readline(self, seconds: float=-1.0, dtype: AudioDType='float32', always_2d: bool=False, **extra: object):
        """Read from the file and return data (*1 second*) as NumPy array.

        Args:
            seconds (int, optional): The second of to read. Defaults to `-1`.

        Returns:
            ndarray: If out is specified, the data is written into the given array instead of creating a new array. In this case, the arguments *dtype* and *always_2d* are silently ignored! If *frames* is not given, it is obtained from the length of out.
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