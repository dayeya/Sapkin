from loaders.loader import Loader, craft_json_path

class TCPLoader(Loader):
    
    def __init__(self) -> None:
        """
        TCPLoader to load TCP data.
        """
        super().__init__(craft_json_path("tcp.json"))