from pathlib import Path
from typing_extensions import (
    Coroutine, Awaitable, Callable,
    Literal, Union,
    TypeVar, TypeAlias
)

# ! Async Types

ResultType = TypeVar('ResultType')
MethodType: TypeAlias = Union[
    Awaitable[ResultType],
    Callable[..., Coroutine[None, None, ResultType]],
    Callable[..., ResultType]
]

# ! Types

DType: TypeAlias = Literal[
    'int8', 'int16', 'int32', 'int64', 'int128', 'int256', 'float16',
    'float32', 'float64', 'float80', 'float96', 'float128', 'float256'
]

# ! IO Types

FilePathType: TypeAlias     = Union[str, Path]
SeekWhenceType: TypeAlias   = Literal[0, 1, 2]

# ! Audio Types

AudioChannels: TypeAlias        = Literal[1, 2]
AudioSamplerate: TypeAlias      = Literal[
    8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000
]
AudioFormat: TypeAlias          = Literal[
    'WAV', 'AIFF', 'AU', 'RAW', 'PAF','SVX', 'NIST', 'VOC', 'IRCAM', 'W64',
    'MAT4', 'MAT5', 'PVF', 'XI', 'HTK', 'SDS', 'FLAC', 'CAF', 'WVE', 'OGG',
    'MPC2K', 'RF64', 'MP3'
]
AudioSubType: TypeAlias         = Literal[
    'PCM_S8', 'PCM_16', 'PCM_24', 'PCM_32', 'PCM_U8', 'FLOAT', 'DOUBLE',
    'ULAW', 'ALAW', 'IMA_ADPCM', 'MS_ADPCM', 'GSM610', 'VOX_ADPCM',
    'NMS_ADPCM_16', 'NMS_ADPCM_24', 'NMS_ADPCM_32', 'G721_32', 'G723_24',
    'G723_40', 'DWVW_12', 'DWVW_16', 'DWVW_24', 'DWVW_N', 'DPCM_8', 'DPCM_16',
    'VORBIS', 'OPUS', 'ALAC_16', 'ALAC_20', 'ALAC_24', 'ALAC_32',
    'MPEG_LAYER_I', 'MPEG_LAYER_II', 'MPEG_LAYER_III'
]
AudioDType: TypeAlias           = Literal[
    'int16', 'int32', 'float32', 'float64'
]
AudioEndians: TypeAlias         = Literal[
    'FILE', 'LITTLE', 'BIG', 'CPU'
]