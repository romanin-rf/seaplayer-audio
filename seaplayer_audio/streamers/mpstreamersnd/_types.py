from numpy import ndarray
from enum import IntEnum
# > Typing
from typing_extensions import (
    Literal,
    NamedTuple, TypedDict,
    Generic, TypeVar, TypeAlias
)
# > Local Imports
from seaplayer_audio._types import AudioSamplerate, AudioChannels, AudioDType

# ! Types

class PacketType(IntEnum):
    OK = 0
    ERROR = 1
    STOP = 2
    INIT = 3
    AUDIO = 4

DT = TypeVar('DT')
T = TypeVar('T')

class Packet(NamedTuple, Generic[T, DT]):
    type: T
    data: DT = None

class InitData(TypedDict):
    samplerate: AudioSamplerate
    channels: AudioChannels
    dtype: AudioDType
    device: int | None

PacketTypes: TypeAlias = \
    Packet[Literal[PacketType.OK], None] | \
    Packet[Literal[PacketType.ERROR], Exception] | \
    Packet[Literal[PacketType.STOP], None] | \
    Packet[Literal[PacketType.INIT], InitData] | \
    Packet[Literal[PacketType.AUDIO], bytes]