from typing import Union

from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.all import Packet as ScapyPacket
from scapy.layers.http import HTTPRequest, HTTPResponse

from ..signatures import TCPSignature, TCPOptions, Flags
from ..signatures import MTUSignature
from ..signatures import HTTPSignature

UTF = 'utf-8'
Signature = Union[TCPSignature, MTUSignature, HTTPSignature]

HEXA: dict[str: bytes] = {
        Flags.DF_SET                      : 0x00000002, 
        Flags.DF_SET_NON_ZERO_ID          : 0x00000004, 
        Flags.DF_NOT_SET_ID_ZERO          : 0x00000008, 
        Flags.ECN                         : 0x00000001, 
        Flags.MZERO                       : 0x00000010, 
        Flags.NON_ZERO_FLOW_ID            : 0x00000020,
        
        Flags.ZERO_SEQ                    : 0x00001000, 
        Flags.NON_ZERO_POSITIVE_ACK       : 0x00002000, 
        Flags.ACK_ZERO_FLAG_SET           : 0x00004000, 
        Flags.NON_ZERO_URG_NOT_SET        : 0x00008000, 
        Flags.URG_FLAG_SET                : 0x00010000, 
        Flags.PUSH_FLAG_SET               : 0x00020000,
            
        Flags.ZERO_OWN_TIMESTAMP          : 0x0100000, 
        Flags.NON_ZERO_TIMESTAMP_INIT_SYN : 0x0200000,  
        Flags.NON_ZERO_DATA               : 0x0400000, 
        Flags.EXCESSIVE_WSCALE            : 0x0800000, 
        Flags.MALFORMED_OP                : 0x1000000
}

class PacketWrapper:
    
    def __init__(self, p: ScapyPacket) -> None:
        """
        PacketWrapper object, wraps p with special functions.

        Args:
            p (ScapyPacket): packet we sniffed.
        """
        self._packet = p.copy()

    def check_tcp(self) -> bool:
        """
        Returns:
            bool: Has a TCP layer.
        """
        return bool(self._packet._packet.haslayer(TCP))
    
    def check_http(self) -> bool:
        """
        Checks if self _packet.is a valid HTTP packet.

        Returns:
            bool: has HTTP layer.
        """
        return bool(self._packet.haslayer[HTTPRequest] or self._packet.haslayer[HTTPResponse])
    
    def _tcp_options(self) -> dict:
        """
        Gets the options from self
        
        Returns:
            dict: TCP options.
        """
        
        if not self.check_tcp():
            raise Exception(f"{self}_packet. doesnt have a TCP layer.")
        
        op = self._packet[TCP].getfield_and_val('options')
        tcp_options = {option: val for option, val in op}
        return tcp_options
        
    def _guess_ittl(self) -> int:
        """
        Checks the most possible ittl of a packet.

        Returns:
            int: guess of ittl of self._packet.
        """
        cur_ttl = self._packet[IP].ttl
        if cur_ttl <= 32: return 32
        if cur_ttl <= 64: return 64
        if cur_ttl <= 128: return 128
        
        # last OS default is 255.
        return 255
    
    def _get_special_flags(self) -> List[str]:
        """
        Scan the packet and identifies its special flags (IP, TCP) headers.

        Returns:
            List[str]: list of special flags, specified in tcp_signature.py
        """
        special_flags: List[str] = []
        ip_layer  = self._packet.getlayer(cls=IP)
        tcp_layer = self._packet.getlayer(cls=TCP)
        
        if ip_layer.flags & HEXA[Flags.DF_SET]:
            special_flags.append(Flags.DF_SET)
        
        if ip_layer.flags & HEXA[Flags.DF_SET] and ip_layer.id:
            special_flags.append(Flags.DF_SET_NON_ZERO_ID)  
            
        if ~(ip_layer.flags & HEXA[Flags.DF_SET]) and ~ip_layer.id:
            special_flags.append(Flags.DF_NOT_SET_ID_ZERO)
            
        if tcp_layer.flags & (Flags.CWR | Flags.ECE): 
            special_flags.append(Flags.ECN)
        
        if ~(ip_layer.flags & HEXA[Flags.MZERO]):
            special_flags.append(Flags.MZERO)
            
        # Will not add flow as p0f doesnt utilize this in this context.
        if ip_layer.version != 4:
            if ip_layer.version & 0xFFFF:
                special_flags.append(Flags.NON_ZERO_FLOW_ID)
        
        # Sequence number isnt 0.
        if not tcp_layer.seq:
            special_flags.append(Flags.ZERO_SEQ)
        
        # ACK check.
        if tcp_layer.flags & Flags.ACK:
            special_flags.append(Flags.ACK_ZERO_FLAG_SET)
           
        else:
            special_flags.append(Flags.NON_ZERO_POSITIVE_ACK)
        
        # URG check.    
        if tcp_layer.flags & Flags.URG:
            special_flags.append(Flags.URG_FLAG_SET)
        
        else:
            special_flags.append(Flags.NON_ZERO_URG_NOT_SET)
        
        # PSH check.    
        if tcp_layer.flags & Flags.PSH:
            special_flags.append(Flags.PUSH_FLAG_SET)
        
        tcp_options = self._packet._tcp_options()
        scale = tcp_options.get(TCPOptions.WINDOW_SCALE, TCPSignature.WINDOW_SCALE_DEFAULT)
        if scale > 14:
            special_flags.append(Flags.EXCESSIVE_WSCALE)
            
        # Add consideration for last 4 missing special flags (not urgent)! #
        
        return special_flags
        
    def _create_tcp_signature(self) -> TCPSignature:
        """
        Creates a TCP signature from self

        Returns:
            TCPSignature: TCPSignature.
        """
        ip_layer  = self._packet.getlayer(cls=IP)
        tcp_layer = self._packet.getlayer(cls=TCP)
        
        version = ip_layer.version
        ittl = self._packet._guess_ittl()
        
        # Handle options.
        tcp_options = self._packet._tcp_options()
        olen = len(tcp_options)
        
        # tcp options fields.
        mss = tcp_options.get(TCPOptions.MSS, TCPSignature.MSS_DEFAULT)
        scale = tcp_options.get(TCPOptions.WINDOW_SCALE, TCPSignature.WINDOW_SCALE_DEFAULT)
        window_size = tcp_layer.window
        
        options_layout = ':'.join([option for option in tcp_options.keys()])
        special_flags = ':'.join(self._packet._get_special_flags()) # QUIRKS in p0f
        
        payload_size = len(tcp_layer.payload)
        
        return TCPSignature(
            version,
            ittl,
            olen,
            mss,
            window_size,
            scale,
            options_layout,
            special_flags,
            payload_size
        )
        
    def __str__(self) -> str:
        """
        Constructs a PacketWrapper string representation.

        Returns:
            str: String of self._packet.
        """
        return self._packet.summary()
