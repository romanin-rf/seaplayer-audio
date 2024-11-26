from typing_extensions import Optional
from .._types import AudioSamplerate, AudioChannels, AudioDType
from .streamer import StreamerBase, AsyncStreamerBase

# ^ SoundDevice Streamer Base

class SoundDeviceStreamerBase(StreamerBase):
    __steamer_type__: str = 'sounddevice-base'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd)
        self.device = device

# ^ Async SoundDevice Streamer Base

class AsyncSoundDeviceStreamerBase(AsyncStreamerBase):
    __steamer_type__: str = 'async-sounddevice-base'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd)
        self.device = device