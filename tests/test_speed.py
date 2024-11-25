import pytest
# * Required Imports
import asyncio
# * Local Imports (for tests)
from .libs import *
# * Main Imports (tested)
from seaplayer_audio import FileAudioSource, AsyncFileAudioSource

# ! Methods for Tests
async def main_test_async_speed0():
    loop = asyncio.get_running_loop()
    with Timer() as init_timer:
        sfile = AsyncFileAudioSource(SAMPLES_FILEPATHS['sample0'], loop=loop)
    
    with Timer() as s1_read_timer:
        s1data = await sfile.readline(1)
    
    with Timer() as read_timer:
        other = await sfile.read(always_2d=True)
    
    logger.rule("START speed test (async)")
    logger.debug(f"Init Time (async): {init_timer.timing:.3f} second(s)", with_new_line=True)
    logger.debug(f"Read Time (async): {read_timer.timing:.3f} second(s)")
    logger.debug(f"1S Read Time (async): {s1_read_timer.timing:.3f} second(s)")
    logger.debug(f"Frames Count: {len(s1data)+len(other)} frames")
    logger.debug(f"Object: {sfile}")
    logger.rule("END speed test (async)")
    return sfile

def main_test_sync_speed0():
    with Timer() as init_timer:
        sfile = FileAudioSource(SAMPLES_FILEPATHS['sample0'])
    
    with Timer() as s1_read_timer:
        s1data = sfile.readline(1)
    
    with Timer() as read_timer:
        other = sfile.read(always_2d=True)
    
    logger.rule("START speed test (sync)")
    logger.debug(f"Init Time (sync): {init_timer.timing:.3f} second(s)", with_new_line=True)
    logger.debug(f"Read Time (sync): {read_timer.timing:.3f} second(s)")
    logger.debug(f"1S Read Time (sync): {s1_read_timer.timing:.3f} second(s)")
    logger.debug(f"Frames Count: {len(s1data)+len(other)} frames")
    logger.debug(f"Object: {sfile}")
    logger.rule("END speed test (sync)")
    
    return sfile

# ! Tests
def test_async_speed0():
    assert isinstance(asyncio.run(main_test_async_speed0()), AsyncFileAudioSource)

def test_sync_speed0():
    assert isinstance(main_test_sync_speed0(), FileAudioSource)