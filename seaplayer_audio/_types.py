import numpy as np
from numpy import ndarray
from io import BufferedReader
from email.message import Message
from http.client import HTTPResponse
from pathlib import Path, PurePath, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath
# > Typing
from typing_extensions import (
    Any, Tuple,
    Literal,
    TypeVar, TypeAlias
)

# ! Async Types

ResultType = TypeVar('ResultType')
#MethodType: TypeAlias = Awaitable[ResultType] | Callable[..., Coroutine[None, None, ResultType]] | Callable[..., ResultType]

# ! Types

DType: TypeAlias = Literal[
    'int8', 'int16', 'int32', 'int64', 'int128', 'int256', 'float16',
    'float32', 'float64', 'float80', 'float96', 'float128', 'float256'
]

# ! Numpy Types

SupportNDArray: TypeAlias = ndarray[Any, np.int16 | np.int32 | np.float32 | np.float64]

# ! IO Types

FilePathType: TypeAlias = str | bytes | Path | PurePath | PosixPath | PurePosixPath | PureWindowsPath | WindowsPath

# ! Audio Types

AudioChannels: TypeAlias        = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
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

SoundDeviceStreamerLatency: TypeAlias = Literal['high', 'low'] | float

# ! Class Types

class Reprable:
    __repr_attrs__: Tuple[str | Tuple[str, bool], ...] = ()
    
    def __str__(self) -> str:
        attrs = []
        for attrdata in self.__repr_attrs__:
            if isinstance(attrdata, str):
                attrs.append(f"{attrdata}={repr(getattr(self, attrdata))}")
            else:
                attrvalue = getattr(self, attrdata[0], None)
                attrvalue = '...' if ((attrvalue is not None) and attrdata[1]) else repr(attrvalue)
                attrs.append(f"{attrdata[0]}={attrvalue}")
        return "{}({})".format(self.__class__.__name__, ', '.join(attrs))
    
    def __repr__(self) -> str:
        return self.__str__()

# ! URL Open Types

class URLOpenRetType:
    code: Any | None
    status: Any | None
    headers: Message
    file: BufferedReader
    fp: BufferedReader
    
    def getcode(self) -> Any | None: ...
    def geturl(self) -> str: ...
    def info(self) -> Message: ...

class URLOpenRetFile(BufferedReader, URLOpenRetType):
    pass

class URLOpenRetHTTP(HTTPResponse, URLOpenRetFile):
    pass

URLOpenRet: TypeAlias = URLOpenRetFile | URLOpenRetHTTP