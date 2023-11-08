from .loader import Loader, craft_json_path

class HTTPLoader(Loader):
    
    def __init__(self) -> None:
        """
        HTTPLoader to load http data.
        """
        super().__init__(craft_json_path("http.json"))