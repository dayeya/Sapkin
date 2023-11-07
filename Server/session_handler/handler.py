import os
import sys
from scapy.all import *
from scapy.all import conf
from threading import Thread

from scapy.layers.inet import IP, TCP
from scapy.all import Packet as ScapyPacket

try: 
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(parent_dir)
    
    from fingerprint import Flags
    from fingerprint import PacketWrapper
    
except ModuleNotFoundError as e:
    raise Exception("Check project dir as fingerprint was not found.")

conf.verbose = 0
conf.sniff_promisc = 0

DST_PORT = 60000
PACKET_AT_A_TIME = 1

class SessionHandler(Thread):
    
    def __init__(self) -> None:
        """
        TCPListener object, listens to TCP connections with the server.
        """
        self._running = False
        
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
        Listens to packet, targets TCP Hanhshakes, SYN, SYN_ACK packets.
        """
        
        self._running = True
        print("Handler is listening!")
        
        while self._running:
            self._packets = sniff(count=PACKET_AT_A_TIME, filter="tcp", prn=self.packet_handler)
     
    def packet_handler(self, p: ScapyPacket) -> None:
        
        """
        Add packet handling.
        """
        pass
                
    def _should_discover(self, p: PacketWrapper) -> bool:
        """
        Check if p should be fingerprinted.

        Args:
            p (PacketWrapper): packet wrapper

        Returns:
            bool: p is SYN or SYN_ACK.
        """
        if not p.check_tcp():
            raise Exception("Sniffed wrong packet!")
        
        # if p has synor syn + ack on.
        tcp_layer = p.getlayer(TCP)
        return (tcp_layer.flags & Flags.SYN) or (tcp_layer.flags & Flags.SYN 
                                                 and tcp_layer.flags & Flags.ACK)