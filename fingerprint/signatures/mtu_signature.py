class MTUSignature:

    def __init__(self, link: str, mtu: int) -> None:
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
        
    def __str__(self) -> str:
        """
        Returns:
            str: String representation of self
        """
        return f"MTUSignature: " \
               f"{self.link}:" \
               f"{self.mtu}"