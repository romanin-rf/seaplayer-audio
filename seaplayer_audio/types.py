from typing_extensions import TypeAlias, Literal, Union, Generator, Any

# ! Spetific Types

ErrorTextType: TypeAlias            = Generator[str, Any, None]

# ! Audio Types

SamplerateType: TypeAlias           = Literal[8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000]
"""A type with all possible `samplerate` options."""
SAMPLERATE_VALUES                   = (8000, 11025, 16000, 22050, 32000, 44100, 48000, 96000, 192000)
"""A constant with the listed possible `samplerate` options."""

LiteralIntDType: TypeAlias          = Literal['int8', 'int16', 'int32', 'int64', 'int128', 'int256']
"""Literals of possible `dtype` values for `int`."""
LiteralFloatDType: TypeAlias        = Literal['float16', 'float32', 'float64', 'float80', 'float96', 'float128', 'float256']
"""Literals of possible `dtype` values for `float`."""
DType: TypeAlias                    = Union[LiteralIntDType, LiteralFloatDType]
"""Literals of possible `dtype` values."""
DTYPE_INT_VALUES                    = ('int8', 'int16', 'int32', 'int64', 'int128', 'int256')
DTYPE_FLOAT_VALUES                  = ('float16', 'float32', 'float64', 'float80', 'float96', 'float128', 'float256')
DTYPE_VALUES                        = (*DTYPE_INT_VALUES, *DTYPE_FLOAT_VALUES)