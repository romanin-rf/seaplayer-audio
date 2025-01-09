from multiprocessing.connection import PipeConnection

# ! Main Process Loop

def __process__(pipe: PipeConnection):
    import pickle
    import numpy # NOTE: This is needed for pickle work
    from sounddevice import OutputStream
    from seaplayer_audio.streamers.mpstreamersnd._types import Packet, PacketType, PacketTypes
    
    INIT_DATA_PACKET_TYPE_ERROR = RuntimeError(f"A packet with the `PacketType.INIT` type was expected.")
    
    packet: PacketTypes = pipe.recv()
    if packet.type != PacketType.INIT:
        pipe.send(Packet(PacketType.ERROR, INIT_DATA_PACKET_TYPE_ERROR))
        return
    
    try:
        streamer = OutputStream(**packet.data)
    except Exception as e:
        pipe.send(Packet(PacketType.ERROR, e))
        return
    streamer.start()
    pipe.send(Packet(PacketType.OK))
    
    while True:
        packet: PacketTypes = pipe.recv()
        if packet.type == PacketType.STOP:
            break
        elif packet.type == PacketType.INIT:
            streamer.stop()
            try:
                streamer = OutputStream(**packet.data)
            except Exception as e:
                pipe.send(Packet(PacketType.ERROR, e))
                return
            streamer.start()
            pipe.send(Packet(PacketType.OK))
        elif packet.type == PacketType.AUDIO:
            streamer.write(pickle.loads(packet.data))
            pipe.send(Packet(PacketType.OK))
    
    streamer.stop()
    pipe.send(Packet(PacketType.OK))