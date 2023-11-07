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

IFACE = "Software Loopback Interface 1"
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
        print("[+] Handler is listening!")
        
        while self._running:
            self._packets = sniff(count=PACKET_AT_A_TIME, filter="tcp", iface=IFACE, prn=self.packet_handler)
     
    def packet_handler(self, packet: ScapyPacket) -> None:
        """
        Add packet handling.
        """
        wrapper = PacketWrapper(packet)
        if self._should_discover(wrapper):
            print(f"[+] Found SYN or SYN_ACK src: {wrapper.packet[IP].src}, to: {wrapper.packet[TCP].dport}")
            signature = wrapper.create_tcp_signature()
            print(f'[+] {signature.format()}')
                
    def _should_discover(self, wrapper: PacketWrapper) -> bool:
        """
        Check if a packet should be fingerprinted.

        Args:
            wrapper (PacketWrapper): packet wrapper

        Returns:
            bool: packet inside wrapper is SYN or SYN_ACK.
        """
        if not wrapper.check_tcp():
            return False
        
        # if p has synor syn + ack on.
        tcp_layer = wrapper.packet.getlayer(cls=TCP)
        return (tcp_layer.flags & Flags.SYN) or (tcp_layer.flags & Flags.SYN 
                                             and tcp_layer.flags & Flags.ACK)