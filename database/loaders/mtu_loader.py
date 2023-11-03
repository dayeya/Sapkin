from loaders.loader import Loader, craft_json_path

class MTULoader(Loader):
    
    def __init__(self) -> None:
        """
        MTULoader to load mtu data.
        """
        super().__init__(craft_json_path("mtu.json"))