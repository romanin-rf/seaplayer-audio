import os
import multiprocessing as mp
import seaplayer_audio as seapa
from rich.console import Console

# ! Variables

VOLUME = 0.25
PATH = os.path.join(os.path.dirname(__file__), 'tests', 'samples', 'sample0.mp3')

console = Console()

# ! Main
def main():
    readed = 0
    with seapa.FileAudioSource(PATH) as source:
        with seapa.MPSoundDeviceStreamer() as streamer:
            while len(data := source.readline(1)) > 0:
                console.rule(f"SEGMENT {readed}-{readed+len(data)}")
                console.print(data)
                readed += len(data)
                streamer.send(data * VOLUME)

# ! Start
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red]Aborted![/red]")
    except:
        console.print_exception(word_wrap=True, show_locals=True)
