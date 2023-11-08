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
    
    from fingerprint import MTUSignature, TCPSignature, Flags
    from fingerprint import PacketWrapper
    from database import OSF_DATABASE
    
except ModuleNotFoundError as e:
    raise e

conf.verbose = 0
conf.sniff_promisc = 0

DST_PORT = 60000
PACKET_AT_A_TIME = 1
FILTER = f"tcp and dst port {DST_PORT}"
IFACE  = f"Software Loopback Interface 1"

class SessionHandler:
    
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
            self._packets = sniff(count=PACKET_AT_A_TIME, filter=FILTER, iface=IFACE, prn=self.packet_handler)
     
    def packet_handler(self, packet: ScapyPacket) -> None:
        wrapper = PacketWrapper(packet)
        if self._should_try(wrapper):
            os = self.osf(wrapper)
            print(f'[+] {os}')
                
    def _should_try(self, wrapper: PacketWrapper) -> bool:
        """
        Check if a packet should be fingerprinted.

        Args:
            wrapper (PacketWrapper): packet wrapper

        Returns:
            bool: packet inside wrapper is SYN or SYN_ACK.
        """
        if not wrapper.check_tcp():
            return False
        
        # if p has syn or syn + ack on.
        tcp_layer = wrapper.packet.getlayer(cls=TCP)
        syn = tcp_layer.flags & Flags.SYN
        ack = tcp_layer.flags & Flags.ACK
        
        return syn or (syn and ack)
        
    def osf(self, wrapper: PacketWrapper) -> str:
        """
        OS fingerprinting.

        Args:
            wrapper (PacketWrapper): PacketWrapper

        Returns:
            str: OS of the host inside wrapper.
        """
        signature = wrapper.to_sig()
        print(f'[+] Crafted a TCP signature: {signature.raw()}')

        for os, signatures in OSF_DATABASE.iter_tcp():
            for db_signature in map(lambda s: TCPSignature.from_str(s), signatures):
                if signature == db_signature:
                    return os
        return "Anonymous OS"
