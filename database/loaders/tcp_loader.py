from loaders.loader import Loader

class TCPLoader(Loader):
    
    def __init__(self) -> None:
        """
        TCPLoader to load TCP data.
        """
        super().__init__(r"tcp.json")