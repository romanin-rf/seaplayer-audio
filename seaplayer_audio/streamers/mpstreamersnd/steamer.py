import time
import numpy
import queue
import pickle
from threading import Thread
from multiprocessing import Process, Pipe
# > Typing
from typing_extensions import (
    Optional,
    deprecated
)
# > Local Imports
from seaplayer_audio.base import SoundDeviceStreamerBase, StreamerState
from seaplayer_audio._types import AudioSamplerate, AudioChannels, AudioDType
from seaplayer_audio.streamers.mpstreamersnd.process import __process__
from seaplayer_audio.streamers.mpstreamersnd._types import Packet, PacketType, PacketTypes

# ! Multiprocessing SoundDevice Streamer Class

class MPSoundDeviceStreamer(SoundDeviceStreamerBase):
    __steamer_type__ = 'multiprocessing-sounddevice'
    
    def __init__(self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd: bool=True,
        device: Optional[int]=None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.parent_pipe, self.child_pipe = Pipe()
        self.queue = queue.Queue(1)
        self.thread = Thread(target=self.run)
        self.process = Process(name=f'<{self.__class__.__name__} from {id(self)}>', target=__process__, args=(self.child_pipe,))
    
    def is_busy(self) -> bool:
        return self.queue.qsize() >= self.queue.maxsize
    
    def run(self):
        self.parent_pipe.send(
            Packet(
                PacketType.INIT,
                {'samplerate': self.samplerate, 'channels': self.channels, 'dtype': self.dtype, 'device': self.device}
            )
        )
        packet: PacketTypes = self.parent_pipe.recv()
        if packet.type == PacketType.ERROR:
            raise packet.data
        self.state |= StreamerState.STARTED
        while StreamerState.RUNNING in self.state:
            packet: PacketTypes = self.queue.get()
            if packet.type == PacketType.INIT:
                self.parent_pipe.send(packet)
                packet: PacketTypes = self.parent_pipe.recv()
                if packet.type == PacketType.ERROR:
                    raise packet.data
            elif packet.type == PacketType.AUDIO:
                self.parent_pipe.send(packet)
                self.parent_pipe.recv()
        self.parent_pipe.send(Packet(PacketType.STOP, None))
        self.parent_pipe.recv()
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