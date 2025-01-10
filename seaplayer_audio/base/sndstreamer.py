from asyncio import AbstractEventLoop
# > Local Imports
from seaplayer_audio._types import AudioSamplerate, AudioChannels, AudioDType
from seaplayer_audio.base.streamer import StreamerBase, AsyncStreamerBase

# ^ SoundDevice Streamer Base

class SoundDeviceStreamerBase(StreamerBase):
    __steamer_type__: str = 'sounddevice-base'
    
    def __init__(
        self,
        samplerate: AudioSamplerate | None = None,
        channels: AudioChannels | None = None,
        dtype: AudioDType | None = None,
        closefd: bool = True,
        device: int | None = None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd)
        self.device = device
    
    def reconfigure(self,
        samplerate: AudioSamplerate | None = None,
        channels: AudioChannels | None = None,
        dtype: AudioDType | None = None,
        device: int | None = None
    ) -> None:
        super().reconfigure(samplerate, channels, dtype)
        self.device = device if (device is not None) else self.device

# ^ Async SoundDevice Streamer Base

class AsyncSoundDeviceStreamerBase(AsyncStreamerBase):
    __steamer_type__: str = 'async-sounddevice-base'
    
    def __init__(
        self,
        samplerate: AudioSamplerate | None = None,
        channels: AudioChannels | None = None,
        dtype: AudioDType | None = None,
        closefd: bool = True,
        loop: AbstractEventLoop | None = None,
        device: int | None = None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, loop)
        self.device = device
    
    def reconfigure(self,
        samplerate: AudioSamplerate | None = None,
        channels: AudioChannels | None = None,
        dtype: AudioDType | None = None,
        device: int | None = None
    ) -> None:
        super().reconfigure(samplerate, channels, dtype)
        self.device = device if (device is not None) else self.device