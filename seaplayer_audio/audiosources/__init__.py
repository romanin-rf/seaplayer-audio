from .fileaudiosource import FileAudioSource, AsyncFileAudioSource
from .urlaudiosource import URLAudioSource
from .urlio import URLIO

AudioSourceLike = FileAudioSource | URLAudioSource
AsyncAudioSourceLike = AsyncFileAudioSource

__all__ = [
    'FileAudioSource', 'AsyncFileAudioSource',
    'URLAudioSource', 'URLIO'
]