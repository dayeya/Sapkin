from scapy.all import *

class TCPListener():
    
    def __init__(self) -> None:
        
        self._packets = sniff()