from sounddevice import OutputStream
from dataclasses import dataclass
from .._types import AudioSamplerate, AudioChannels, AudioDType

# ! Packet Class
@dataclass(frozen=True)
class Packet[CL, DT]:
    code: CL
    data: DT

# ! Alls
__all__ = ['Packet', 'OutputStream', 'AudioSamplerate', 'AudioChannels', 'AudioDType']