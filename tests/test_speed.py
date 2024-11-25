import pytest
# * Required Imports
import asyncio
# * Local Imports (for tests)
from .libs import *
# * Main Imports (tested)
from seaplayer_audio import AsyncFileAudioSource

# ! Methods for Tests
async def main_test_speed0():
    with Timer() as init_timer:
        sfile = AsyncFileAudioSource(SAMPLES_FILEPATHS['sample0'])
    
    with Timer() as read_timer:
        data = await sfile.read(always_2d=True)
    
    logger.debug(f"Init Time: {init_timer.timing:.3f} second(s)", with_new_line=True)
    logger.debug(f"Read Time: {read_timer.timing:.3f} second(s)")
    logger.debug(f"Frames Count: {len(data)} frames")
    logger.debug(f"Object: {sfile}")
    
    return 0

# ! Tests
def test_speed0():
    assert asyncio.run(main_test_speed0()) == 0