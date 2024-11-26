import os
import seaplayer_audio as seapa

PATH = "D:\\Users\\Romanin\\Music\\Frizk_-_Oh_Yeah.mp3"

with seapa.FileAudioSource(PATH) as audiofile:
    with seapa.ThreadSoundDeviceStreamer() as streamer:
        input("Press <ENTER> for start...")
        try:
            while True:
                streamer.send(audiofile.readline(1))
        except KeyboardInterrupt:
            streamer.stop()
            print("Aborted!!!")