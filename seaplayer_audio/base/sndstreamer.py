from asyncio import AbstractEventLoop
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
    
    def reconfigure(self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        device: Optional[int]=None,
    ) -> None:
        super().reconfigure(samplerate, channels, dtype)
        self.device = device if (device is not None) else self.device

# ^ Async SoundDevice Streamer Base

class AsyncSoundDeviceStreamerBase(AsyncStreamerBase):
    __steamer_type__: str = 'async-sounddevice-base'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        loop: Optional[AbstractEventLoop]=None,
        device: Optional[int]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, loop)
        self.device = device
    
    def reconfigure(self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        device: Optional[int]=None,
    ) -> None:
        super().reconfigure(samplerate, channels, dtype)
        self.device = device if (device is not None) else self.device