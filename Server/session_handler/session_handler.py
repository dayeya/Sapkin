from scapy.all import *
from scapy.layers.inet import TCP, IP
from scapy.all import Packet as ScapyPacket
from threading import Thread

try: 
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(parent_dir)
    from fingerprint import PacketWrapper
    
except ModuleNotFoundError as e:
    raise Exception("Check project dir as fingerprint was not found.")

FILTER = f"tcp"
DST_PORT = 60000
PACKET_AT_A_TIME = 1
ADDRESS = ('localhost', 60000)

class SessionHandler(Thread):
    
    def __init__(self) -> None:
        """
        TCPListener object, listens to TCP connections with the server.
        """
        self._running = False
        self._packets = None
        
    def _is_listening(self) -> bool:
        """
        Checks if self is running.

        Returns:
            bool: Indicates the state of self
        """
        return self._running
    
    def _reboot(self) -> None:
        """
        Reboots the listener.
        """
        self._running = True
        self.listen()
    
    def listen(self) -> None:
        """
        Listens to packet,targets TCP Hanhshakes, SYN, SYN+ACK packets.
        """
        
        self._running = True
        print("Handler is listening!")
        
        while self._running:
            self._packets = sniff(count=PACKET_AT_A_TIME, filter=FILTER, prn=self.packet_handler)
    
    def packet_handler(self, p: ScapyPacket) -> None:
        print(f'Captured packet: {p.summary()}')
        

