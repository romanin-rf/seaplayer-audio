from .threadstreamersnd import ThreadSoundDeviceStreamer, AsyncThreadSoundDeviceStreamer
from .callbackstreamersnd import CallbackSoundDeviceStreamer, AsyncCallbackSoundDeviceStreamer, CallbackSettingsFlag
try:
    from .mpstreamersnd import MPSoundDeviceStreamer
    StreamerLike = ThreadSoundDeviceStreamer | CallbackSoundDeviceStreamer | MPSoundDeviceStreamer
except ImportError:
    StreamerLike = ThreadSoundDeviceStreamer | CallbackSoundDeviceStreamer

AsyncStreamerLike = AsyncThreadSoundDeviceStreamer | AsyncCallbackSoundDeviceStreamer

__all__ = [
    'ThreadSoundDeviceStreamer', 'AsyncThreadSoundDeviceStreamer',
    'CallbackSoundDeviceStreamer', 'AsyncCallbackSoundDeviceStreamer', 'CallbackSettingsFlag',
    'MPSoundDeviceStreamer'
]