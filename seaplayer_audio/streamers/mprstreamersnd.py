from multiprocessing import Process, Pipe
from multiprocessing.connection import PipeConnection
from typing_extensions import Optional
from ._mprutils import Packet
from .._types import AudioSamplerate, AudioChannels, AudioDType
from ..base import SoundDeviceStreamerBase, StreamerState

# ! Main Class
class MultiprocessSoundDeviceStreamer(SoundDeviceStreamerBase):
    __steamer_type__ = 'multi-sounddevice'
    
    def __init__(
        self,
        samplerate: Optional[AudioSamplerate]=None,
        channels: Optional[AudioChannels]=None,
        dtype: Optional[AudioDType]=None,
        closefd = True,
        device = None
    ) -> None:
        super().__init__(samplerate, channels, dtype, closefd, device)
        self.external_pipe, self.interal_pipe = Pipe()
        self.process = Process(target=self.run, args=(self.interal_pipe,))
    
    def is_busy(self) -> bool:
        return StreamerState.LOCKED in self.state
    
    @staticmethod
    def run(pipe: PipeConnection) -> None:
        """Process method.
        
        #### States:
            0b00000001 - started state      (init)
            0b00000010 - stop signal        (ending-runtime)
            0b00000100 - abort signal       (runtime)
            0b00001000 - init data          (init)
            0b00010000 - audio data         (runtime)
            0b10000000 - handlered state    (verify-runtime)
        
        Args:
            pipe (PipeConnection): The pipe is double-sided.
        """
        import numpy
        from queue import PriorityQueue
        from ._mprutils import Packet, OutputStream
        from typing_extensions import Dict, Any, Optional, Union, Literal
        init_respone: Packet[Literal[0b00001000], Dict[str, Any]] = pipe.recv()
        if init_respone.code == 0b00001000:
            extra = init_respone.data
        else:
            pipe.send(Packet(0b00000001, False))
        queue: PriorityQueue[numpy.ndarray] = PriorityQueue(1)
        stream = OutputStream(**extra)
        stream.start()
        pipe.send(Packet(0b00000001, True))
        # ? ---> CYCLE START <---
        running = True
        while running:
            runtime_resp: Union[
                Packet[Literal[0b00010000], numpy.ndarray],
                Packet[Literal[0b00000010], None],
                Packet[Literal[0b00000100], None],
            ] = pipe.recv()
            if runtime_resp.code == 0b00010000:     # ! audio data      (runtime)
                queue.put(runtime_resp.data)
                pipe.send(Packet(0b10000000, True))
                continue
            elif runtime_resp.code == 0b00000010:   # ! stop signal     (ending-runtime)
                queue.task_done()
                stream.abort()
                stream.stop()
                running = False
                continue
            elif runtime_resp.code == 0b00000100:   # ! abort signal    (runtime)
                queue.task_done()
                stream.abort()
                pipe.send(Packet(0b10000000, True))
                continue
            else:
                queue.task_done()
                stream.abort()
                stream.stop()
                running = False
                return pipe.send(Packet(0b10000000, False))
        # ? --->  CYCLE END  <---
        pipe.send(Packet(0b00000001, False))
    
    def start(self) -> None:
        if StreamerState.RUNNING not in self.state:
            self.state |= StreamerState.RUNNING
            self.process.start()
            self.interal_pipe.send(
                Packet(
                    0b00001000,
                    {
                        "samplerate": self.samplerate,
                        "channels": self.channels,
                        "dtype": self.dtype,
                        "device": self.device
                    }
                )
            )
            respone: Packet[bool] = self.interal_pipe.recv()
            if (respone.code == 0b00000001) and respone.data:
                self.state |= StreamerState.STARTED
            else:
                raise RuntimeError('Unknown critical startup error.')
            self.state &= ~StreamerState.LOCKED
    
    def stop(self) -> None:
        if StreamerState.RUNNING in self.state:
            self.state &= ~StreamerState.RUNNING
            self.state |= StreamerState.LOCKED
            self.interal_pipe.send(Packet(0b00000001, None))
            respone: Packet[bool] = self.interal_pipe.recv()
            if (respone.code == 0b00000001) and (not respone.data):
                self.state &= ~StreamerState.STARTED
            else:
                raise RuntimeError('Unknown critical stoping error.')