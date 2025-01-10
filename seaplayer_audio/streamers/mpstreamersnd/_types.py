from enum import IntEnum
from multiprocessing.connection import PipeConnection
# > Typing
from typing_extensions import (
    Any,
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


class StreamerAPI:
    def __init__(self, connection: PipeConnection) -> None:
        self.connection = connection
    
    def send(self, type: PacketType, data: Any, *, verify: bool=True) -> None:
        self.connection.send(Packet(type, data))
        if verify:
            answer = self.connection.recv()
            if answer.type == PacketType.ERROR:
                raise answer.data
    
    def recv(self) -> PacketTypes:
        return self.connection.recv()
    
    def s_error(self, data: Exception, /) -> None:
        self.send(PacketType.ERROR, data, verify=False)
    
    def s_ok(self) -> None:
        self.send(PacketType.OK, None, verify=False)
    
    def s_init(self, data: InitData, /) -> None:
        self.send(PacketType.INIT, data, verify=True)
    
    def s_stop(self) -> None:
        self.send(PacketType.STOP, None, verify=True)
    
    def s_audio(self, data: bytes, /) -> None:
        self.send(PacketType.AUDIO, data, verify=True)