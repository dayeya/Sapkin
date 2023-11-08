from scapy.all import *
from scapy.all import conf
from scapy.layers.inet import IP, TCP

IFACE  = f"Software Loopback Interface 1"

class WindowsTest:
    
    def __init__(self, ittl: int, seq: bytes, options: list) -> None:
        """
        WindowsTest object.

        Args:
            ittl (int): ittl to test.
            seq (bytes): seq number to test.
            options (list): options to test.
        """
        self.src_ip = 'localhost'
        self.dst_ip = 'localhost'
        self.sock = conf.L3socket(iface=IFACE)
        
        # Test arguments.
        self.ittl = ittl
        self.seq = seq
        self.options = options
    
    def send_fuzzy_syn(self) -> None:
        """
        Sends a fuzzy syn packet with custom fields to test Sapkin.
        """
        ip  = IP(src=self.src_ip, dst=self.dst_ip, ttl=self.ittl, id=12345, flags='DF')
        tcp = TCP(dport=60000, flags='S', seq=self.seq, options=self.options)
        
        syn_packet = ip / tcp
        self.sock.send(syn_packet)
        
    def test(self) -> None:
        """
        Sends a single syn packet.
        """
        tests: List[WindowsTest] = [
            WindowsTest(ittl=128, seq=0x12345678, options=[('MSS', 1460), ('NOP', None), ('NOP', None), ('SAckOK', '')]),
            WindowsTest(ittl=128, seq=0x12345678, options=[('MSS', 1460), ('NOP', None), ('WScale', 2), ('NOP', None), ('NOP', None), ('SAckOK', '')]),
            WindowsTest(ittl=128, seq=0x12345678, options=[('MSS', 1460), ('NOP', None), ('WScale', 8), ('NOP', None), ('NOP', None), ('SAckOK', '')]),
            WindowsTest(ittl=128, seq=0x12345678, options=[('MSS', 1460), ('NOP', None), ('WScale', 2), ('SAckOK', ''), ('Timestamp', (100000, 0))])
        ]
        
        for t in tests:
            t.send_fuzzy_syn()
        print('[+] Sent all fuzzy syn packets!')
