# seaplayer-audio
## Description
The SeaPlayer library for async/sync playback audio.

> ***The module is still under DEVELOPMENT, so I do not recommend using it in your projects.***

## Supported formats

It is based on the [sounddevice](https://github.com/spatialaudio/python-sounddevice) and [soundfile](https://github.com/bastibe/python-soundfile) module. 

[soundfile](https://github.com/bastibe/python-soundfile), in turn, is a wrapper of the C library [libsndfile](https://github.com/libsndfile/libsndfile), which has limitations in file reading formats. [More info...](https://libsndfile.github.io/libsndfile/formats.html)

## Usage (synchronously)

#### Through context manager
```python
import time
from seaplayer_audio import CallbackSoundDeviceStreamer, FileAudioSource


def main():
    with FileAudioSource('example.mp3') as source:
        with CallbackSoundDeviceStreamer() as streamer:
            while len(data := source.readline(1)) > 0:
                streamer.send( data )
                time.sleep(0.01) # Optional


if __name__ == '__main__':
    main()
```

#### Through cycle
```python
import time
from seaplayer_audio import CallbackSoundDeviceStreamer, FileAudioSource


def main():
    file = FileAudioSource('example.mp3')
    streamer = CallbackSoundDeviceStreamer()
    streamer.start()
    while len(data := source.readline(1)) > 0:
        streamer.send( data )
        time.sleep(0.01) # Optional
    streamer.stop()
    file.close()


if __name__ == '__main__':
    main()
```

## Usage (asynchronously)

#### Through context manager
```python
import asyncio
from seaplayer_audio import AsyncCallbackSoundDeviceStreamer, AsyncFileAudioSource


async def main():
    async with AsyncFileAudioSource('example.mp3') as source:
        async with AsyncCallbackSoundDeviceStreamer() as streamer:
            while len(data := await source.readline(1)) > 0:
                await streamer.send( data )
                await asyncio.sleep(0.01) # Optional


if __name__ == '__main__':
    asyncio.run(main())
```

#### Through cycle
```python
import asyncio
from seaplayer_audio import AsyncCallbackSoundDeviceStreamer, AsyncFileAudioSource


async def main():
    file = FileAudioSource('example.mp3')
    streamer = CallbackSoundDeviceStreamer()
    await streamer.start()
    while len(data := await source.readline(1)) > 0:
        await streamer.send( data )
        await asyncio.sleep(0.01) # Optional
    await streamer.stop()
    await file.close()


if __name__ == '__main__':
    asyncio.run(main())
```