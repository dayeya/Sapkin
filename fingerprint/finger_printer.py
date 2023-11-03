import pydivert

class Sniffer:

    """
    the sniffer catches the packets that are transmitted during the communication process
    """

    def __init__(self, f: str = None) -> None:
        """

        Args:
            f: filter for the sniffer
        """
        if f is not None:
            self.w = pydivert.WinDivert(f)
        else:
            self.w = pydivert.WinDivert()

    def sniff_packets(self):
        print("Sniffing started")
        with self.w as w:
            for packet in w:
                print(packet)



