from scapy.all import *
from scapy.all import Packet as ScapyPacket
from threading import Thread

DST_PORT = 60000
PACKET_AT_A_TIME = 1
FILTER = f"localhost and dst port {DST_PORT}"

class TCPListener():
    
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
        
    def listen(self):
        
        while self._running:
            
            self._packets = sniff(count=PACKET_AT_A_TIME, prn=self.single_packet)
            
    def single_packet(self, packet: ScapyPacket) -> None:
        print(f'Captured packet: \n{packet.summer()}')

            

