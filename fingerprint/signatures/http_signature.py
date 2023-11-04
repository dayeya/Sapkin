class HTTP_sig:

    def __init__(self, version = "all", headers = [], no_headers = [], desc = "") -> None:
        #http sig = version | headers | no-headers | desc
        self.version = version
        self.headers = headers
        self.no_headers = no_headers
        self.desc = desc