# seaplayer-audio
## Description
The SeaPlayer library for async/sync playback audio.

> ***The module is still under DEVELOPMENT, so I do not recommend using it in your projects.***

## Supported formats

- ✅ - fully supported
- ❌ - not supported
- 🌗 - partial support (supported, but with nuances)

> It is based on the [sounddevice](https://github.com/spatialaudio/python-sounddevice) and [soundfile](https://github.com/bastibe/python-soundfile) module. 
>> **soundfile**, in turn, is a wrapper of the C/C++ library **libsndfile**, which has limitations in file reading formats. [More info...](http://www.mega-nerd.com/libsndfile/)

| Formats | Support |
|:-------:|:-------:|
| Microsoft WAV | ✅ |
| SGI / Apple AIFF / AIFC | ✅ |
| Sun / DEC / NeXT AU / SND | ✅ |
| Headerless RAW | ✅ |
| Paris Audio File (PAF) | 🌗 |
| Commodore Amiga IFF / SVX | 🌗 |
| Sphere Nist WAV | 🌗 |
| IRCAM SF | 🌗 |
| Creative VOC | 🌗 |
| Sound forge (W64) | ✅ |
| GNU Octave 2.0 (MAT4) | ✅ |
| GNU Octave 2.1 (MAT5) | ✅ |
| Portable Voice Format (PVF) | 🌗 |
| Fasttracker 2 XI | ❌ |
| Apple CAF | ✅ |
| Sound Designer II (SD2) | 🌗 |
| Free Lossless Audio Codec FLAC | 🌗 |

## Usage

#### Through context manager
```python
import time
from seaplayer_audio import CallbackSoundDeviceStreamer, FileAudioSource


def main():
    with FileAudioSource('example.mp3') as source:
        with CallbackSoundDeviceStreamer() as streamer:
            while len(data := source.readline(1)) > 0:
                streamer.send( data )
                time.sleep(0.01)


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
        time.sleep(0.01)
    streamer.stop()
    file.close()


if __name__ == '__main__':
    main()
```