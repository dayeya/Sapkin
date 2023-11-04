from typing import List, TypeVar

# version fields can be 4, 6 or ALL.
Version = TypeVar("IP_Version", int, str)

class TCPSignature:

    def __init__(self, 
                 version: Version="ALL", 
                 ttl=128, 
                 op_len=0, 
                 mss=0, 
                 win_size=0, 
                 scale=0, 
                 options: List[str]=None, 
                 flags: dict=None, 
                 payload_size=0
            ) -> None:
        """
        TCPSignature object.

        Args:
            version (str, optional): IPv4 / IPv6 or. Defaults to "all".
            ttl (int, optional): Initial TTL of the corresponsing packet. Defaults to 128, we just picked it.
            op_len (int, optional): Options fields length. Defaults to 0.
            mss (int, optional): MSS field of the corresponsing packet. Defaults to 0.
            win_size (int, optional): Window size. Defaults to 0.
            scale (int, optional): Window scale. Defaults to 0.
            options (list, optional): Actual option fields. Defaults to [].
            flags (dict, optional): All flags of the IP and TCP headers. Defaults to {}.
            payload_size (str, optional): Payload size. Defaults to 0.
        """
        self.version = version
        self.ttl = ttl
        self.op_len = op_len
        self.mss = mss
        self.win_size = win_size
        self.scale = scale
        self.options = options if op_len > 0 else []
        self.flags = flags if flags else {}
        self.payload_size = payload_size
    
    def __str__(self) -> str:
        """
        Returns:
            str: String representation of self
        """
        return f"TCPSignature: 
                {self.version}:
                {self.ttl}:
                {self.op_len}:
                {self.mss}:
                {self.win_size}:
                {self.scale}:
                {self.options}:
                {self.flags}:
                {self.payload_size}"
