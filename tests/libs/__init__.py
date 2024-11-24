import logging
from rich.logging import RichHandler
from .timing import Timer
from .units import LOCAL_DIRPATH, SAMPLES_DIRPATH, SAMPLES_FILEPATHS


logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            markup=True,
            rich_tracebacks=True,
            tracebacks_word_wrap=True,
            tracebacks_show_locals=True
        )
    ]
)
logger = logging.getLogger("rich")