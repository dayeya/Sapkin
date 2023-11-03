from loaders.loader import Loader

class HTTPLoader(Loader):
    
    def __init__(self) -> None:
        """
        HTTPLoader to load http data.
        """
        super().__init__("http.json")