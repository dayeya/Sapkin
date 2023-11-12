import time
from scapy.all import *
from scapy.all import conf
from scapy.layers.inet import IP, TCP
from threading import Thread
from .tests import WindowsTest

IFACE  = f"Software Loopback Interface 1"

class SynHandler(Thread):
    
    def __init__(self, src: str="localhost", dst: str="localhost") -> None:
        """
        SynHandler object.
        """
        self._src_ip = src
        self._dst_ip = dst
        self.sock = conf.L3socket(iface=IFACE)
        
        # Start sending syn packets.
        super().__init__(target=self.register_syn_per_interval)
        
    @property
    def src_ip(self) -> str:
        """
        Returns:
            str: src_ip
        """
        return self._src_ip
    
    @property
    def dst_ip(self) -> str:
        """
        Returns:
            str: dst_ip
        """
        return self._dst_ip
    
    def register_syn_per_interval(self, interval: int=30) -> None:
        """
        Sends syn packets to the server every 'interval' seconds.

        Args:
            interval (int, optional): Interval of sending. Defaults to 30.
        """
        def current_time() -> float:
            return time.time()
        
        last_registered = current_time()
        while True:
            ct = current_time()
            if ct - last_registered >= interval:
                last_registered = ct
                self._send_syn()

    def _send_syn(self) -> None:
        """
        Sends a single syn packet.
        """
        syn = 'S'
        ip  = IP(src=self.src_ip, dst=self.dst_ip)
        tcp = TCP(dport=60000, flags=syn)

        syn_packet = ip / tcp
        self.sock.send(syn_packet)
        print('[+] Syn sent!')