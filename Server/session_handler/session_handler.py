from scapy.all import *
from scapy.layers.inet import TCP, IP, IPv6
from scapy.all import Packet as ScapyPacket

from threading import Thread
from fingerprint import PacketWrapper

DST_PORT = 60000
PACKET_AT_A_TIME = 1
FILTER = f"tcp"

class SessionHandler:
    
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
        while self._running:
            self._packets = sniff(count=PACKET_AT_A_TIME, filter=FILTER, prn=self.packet_handler)
    
    def packet_handler(self, p: ScapyPacket) -> None:
        print(f'Captured packet: {p.summary()}')
        

