from typing import List, TypeVar

# version fields can be 4, 6 or ALL.
IP_Version = TypeVar("IP_Version", int, str)
TCPSig = TypeVar("TCPSig", bound='TCPSignature')

class Flags:
    # Core TCP flags.
    FIN = 0x01
    SYN = 0x02
    RST = 0x04
    PSH = 0x08
    ACK = 0x10
    URG = 0x20
    ECE = 0x40
    CWR = 0x80
    
    # Special Flags - p0f
    DF_SET = "df"
    DF_SET_NON_ZERO_ID = "id+"
    DF_NOT_SET_ID_ZERO = "id-"
    ECN = "ecn"
    MZERO = "0+"
    NON_ZERO_FLOW_ID = "flow"
    ZERO_SEQ = "seq-"
    NON_ZERO_POSITIVE_ACK = "ack+"
    ACK_ZERO_FLAG_SET = "ack-"
    NON_ZERO_URG_NOT_SET = "uptr+"
    URG_FLAG_SET = "urgf+"
    PUSH_FLAG_SET = "pushf+"
    ZERO_OWN_TIMESTAMP = "ts1-"
    NON_ZERO_TIMESTAMP_INIT_SYN = "ts2+" 
    NON_ZERO_DATA = "opt+"
    EXCESSIVE_WSCALE = "exws"
    MALFORMED_OP = "bad"

class TCPOptions:
    MSS = "MSS"
    NOP = "NOP"
    WINDOW_SCALE = "WScale"
    SOK = "SAckOK"
    SACK = "SAck"
    TIMESTAMP = "TS"
    
    FORMATS = {
        "MSS": "mss",
        "NOP": "nop",
        "WScale": "ws",
        "SAckOK": "sok",
        "SAck": "sack",
        "TS": "ts"
    }
    
    @staticmethod
    def convert(option: str) -> str:
        """
        Converts an option string into p0f signature format.

        Args:
            option (str): one of the TCPOption fields.

        Returns:
            str: p0f syntax of option.
        """
        return TCPOptions.FORMATS[option]

class TCPSignature:
    
    MSS_DEFAULT = str(0)
    WINDOW_SCALE_DEFAULT = str(0)

    def __init__(self, 
                 version: IP_Version="ALL", 
                 ttl=128, 
                 op_len=0, 
                 mss=0, 
                 win_size=0, 
                 scale=0, 
                 options_layout: List[str]=None, 
                 special_flags: dict=None, 
                 payload_size=0
            ) -> None:
        """
        TCPSignature object.

        Args:
            version (str, optional): IPv4 / IPv6 or. Defaults to "ALL".
            ttl (int, optional): Initial TTL of the corresponsing packet. Defaults to 128, we just picked it.
            op_len (int, optional): Options field length at IP layer. Defaults to 0.
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
        self.options = options_layout if options_layout else []
        self.flags = special_flags if special_flags else {}
        self.payload_size = payload_size
    
    def raw(self) -> str:
        """
        Will format self into a specific str.

        Returns:
            str: ver:ittl:op_len:mss:win_size,scale:options:flags:payload_size
        """
        return f'{self.version}:{self.ttl}:{self.op_len}:{self.mss}:' \
               f'{self.win_size},{self.scale}:{self.options}:{self.flags}:{self.payload_size}'
               
    def fields(self) -> str:
        """
        Returns:
            str: ver:ittl:op_len:mss:win_size,scale:options:flags:payload_size
        """
        return self.version, self.ttl, self.op_len, self.mss, \
               self.win_size, self.scale, self.options, self.flags, self.payload_size
               
    def __eq__(self, other) -> bool:
        """
        Args:
            other (str): tcp db signature.

        Returns:
            bool: is self equal to sig.
        """
        if isinstance(other, TCPSignature): 
            return (
                (self.version == other.version or other.version == 'ALL') and
                (self.mss == other.mss or other.mss == 'ALL') and
                self.ttl == other.ttl and
                self.op_len == other.op_len and
                self.win_size == other.win_size and
                self.scale == other.scale and
                self.options == other.options and 
                self.flags == other.flags and
                self.payload_size == other.payload_size
            )
        return False
    
    @staticmethod
    def from_str(sig: str) -> TCPSig:
        """
        Builds a TCPSignature from sig.

        Args:
            sig (str): db entry.

        Returns:
            TCPSignature: A new TCPSignature.
        """
        # Unpack the signature.
        version, ittl, op_len, mss, ws_pair, \
        options_layout, special_flags, payload_size = tuple(sig.split(":"))
        win_size, scale = ws_pair.split(',')
        
        return TCPSignature(
            version,
            ittl,
            op_len,
            mss,
            win_size,
            scale,
            options_layout,
            special_flags,
            payload_size
        )
        
    def __str__(self) -> str:
        """
        Returns:
            str: String representation of self
        """
        return f"version: {self.version}, " \
               f"ttl: {self.ttl}, " \
               f"op_len: {self.op_len}, " \
               f"mss: {self.mss}, " \
               f"win_size: {self.win_size}, " \
               f"scale: {self.scale}, " \
               f"options: {self.options}, " \
               f"flags: {self.flags}, " \
               f"payload_size: {self.payload_size}"
