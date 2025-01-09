import time
import numpy
import queue
import pickle
from threading import Thread
from multiprocessing import Process, Pipe
# > Typing
from typing_extensions import (
    Any,
    Optional,
    Callable,
    Self,
    deprecated
)
# > Local Imports
from seaplayer_audio.base import SoundDeviceStreamerBase, StreamerState
from seaplayer_audio._types import AudioSamplerate, AudioChannels, AudioDType
from seaplayer_audio.streamers.mpstreamersnd.process import __process__
from seaplayer_audio.streamers.mpstreamersnd._types import Packet, PacketType, PacketTypes, StreamerAPI

# ! Multiprocessing SoundDevice Streamer Class

class MPSoundDeviceStreamer(SoundDeviceStreamerBase):
    __steamer_type__ = 'multiprocessing-sounddevice'
    
    def __init__(self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None,
        *,
        run_loop: Optional[Callable[[Self, StreamerAPI], Any]]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.run_loop = run_loop if (run_loop is not None) else self.run
        self.parent_pipe, self.child_pipe = Pipe()
        self.queue: queue.Queue[PacketTypes] = queue.Queue(1)
        self.api = StreamerAPI(self.parent_pipe)
        self.thread = Thread(target=self.run_loop, args=(self, self.api,))
        self.process = Process(name=f'<{self.__class__.__name__} from {hex(id(self))}>', target=__process__, args=(self.child_pipe,))

    def is_busy(self) -> bool:
        return self.queue.qsize() >= self.queue.maxsize
    
    @staticmethod
    def run(self: 'MPSoundDeviceStreamer', api: StreamerAPI):
        api.s_init({'samplerate': self.samplerate, 'channels': self.channels, 'dtype': self.dtype, 'device': self.device})
        self.state |= StreamerState.STARTED
        while StreamerState.RUNNING in self.state:
            try:
                packet = self.queue.get(timeout=3.0)
                if packet.type == PacketType.INIT:
                    api.s_init(packet.data)
                elif packet.type == PacketType.AUDIO:
                    api.s_audio(packet.data)
            except queue.Empty:
                pass
        api.s_stop()
        self.state &= ~StreamerState.STARTED
    
    def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.process.start()
            self.thread.start()
            while StreamerState.STARTED not in self.state:
                time.sleep(0.01)
            self.state &= ~StreamerState.LOCKED
    
    def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.process.join()
            self.thread.join()
            while StreamerState.STARTED in self.state:
                time.sleep(0.01)
            self.state |= StreamerState.LOCKED
    
    @deprecated("NOT IMPLEMENTED")
    def abort(self):
        pass
    
    def reconfigure(self, 
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        device: Optional[int]=None,
    ) -> None:
        super().reconfigure(samplerate, channels, dtype, device)
        if StreamerState.RUNNING in self.state:
            self.set_lock(True)
            self.parent_pipe.send(
                Packet(
                    PacketType.INIT,
                    {'samplerate': self.samplerate, 'channels': self.channels, 'dtype': self.dtype, 'device': self.device}
                )
            )
            packet: PacketTypes = self.parent_pipe.recv()
            if packet.type == PacketType.ERROR:
                raise packet.data
            self.set_lock(False)
    
    def send(self, data: numpy.ndarray) -> bool:
        if StreamerState.LOCKED not in self.state:
            self.queue.put(Packet(PacketType.AUDIO, pickle.dumps(data)))
            return True
        return False