import pydivert

class Sniffer:

    """
    the sniffer catches the packets that are transmitted during the communication process
    """

    def __init__(self, f: str = None) -> None:
        """
        Sniffer Object

        Args:
            f (str, optional): Filter for the WinDivert. Defaults to None.
        """
        if f is not None:
            self._w = pydivert.WinDivert(f)
        else:
            self._w = pydivert.WinDivert()

    def sniff_packets(self):
        print("Sniffing started")
        with self._w as w:
            for packet in w:
                print(packet)



