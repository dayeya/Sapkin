from loaders.loader import Loader

class MTULoader(Loader):
    
    def __init__(self) -> None:
        """
        MTULoader to load mtu data.
        """
        super().__init__("mtu.json")