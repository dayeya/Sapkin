from typing import TypeVar, List

MTUSig = TypeVar("MTUSig", bound='MTUSignature')

class MTUSignature:

    def __init__(self, link: str="", mtu: List[int]=[]) -> None:
        """
        MTUSignature object.

        Args:
            link (str): Link of connection e.g 'Ethernet, Wi-Fi'...
            mtu (int): MSS field of the corresponding packet.
        """
        self.link = link
        self.mtu = mtu

    def format(self) -> str:
        """
        Will format self into a specific str.

        Returns:
            str: ver:ittl:op_len:mss:win_size,scale:options:flags:payload_size
        """
        return f'{self.link}:{self.mtu}'
        
    def raw(self) -> str:
        """
        Will format self into a specific str.
        Returns:
            str: link:mtu
        """
        return f'{self.link}:{self.mtu}'
    
    @staticmethod
    def from_sig(sig: dict[str: List[int]]) -> MTUSig:
        """
        Builds a MTUSignature from sig.

        Args:
            sig (str): db entry.

        Returns:
            TCPSignature: A new MTUSignature.
        """
        # Unpack the signature.
        link, mtu = sig
        return MTUSig(
            link,
            mtu
        )
    
    def __eq__(self, other) -> bool:
        """
        Args:
            other: mtu db signature.

        Returns:
            bool: is self equal to sig.
        """
        if isinstance(other, MTUSignature): 
            return self.link == other.link and self.mtu == other.mtu
        return False
        
    def __str__(self) -> str:
        """
        Returns:
            str: String representation of self
        """
        return f"Link: {self.link}:" \
               f"MTUs: {self.mtu}"