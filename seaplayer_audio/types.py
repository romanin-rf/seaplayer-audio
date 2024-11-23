from pathlib import Path
from typing_extensions import (
    Literal, Union,
    TypeAlias
)

# ! IO Types

FilePathType: TypeAlias     = Union[str, Path]
SeekWhenceType: TypeAlias   = Literal[0, 1, 2]

# ! Audio Settings Types

Channels: TypeAlias         = Literal[1, 2]
Samplerate: TypeAlias       = Literal[8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000]
DType: TypeAlias            = Literal['int8', 'int16', 'int32', 'int64', 'int128', 'int256', 'float16', 'float32', 'float64', 'float80', 'float96', 'float128', 'float256']

SupportsDType: TypeAlias   = Literal['int16', 'int32', 'float32', 'float64']