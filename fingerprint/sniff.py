import pydivert

class Sniffer:
    
    def __init__(self, filtr: str="true") -> None:
        """
        Sniffer Object

        Args:
            f (str, optional): Filter for the WinDivert. Defaults to None.
        """
        self._w = pydivert.WinDivert(filtr)

    def sniff_packets(self) -> None:
        """
        Sniffs packets.
        """
        
        print("Sniffing...")
        with self._w as packet_driver:
            for packet in packet_driver:
                print(packet)



