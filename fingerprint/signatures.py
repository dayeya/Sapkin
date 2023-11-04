
class TCP_sig:

    def __init__(self, version = "all", ttl = 128, op_len = 0, mss = 0, win_size = 0, scale = 0, options = [], flags = [], payload = ""):
        #tcp sig  = version | ttl | options-len | mss | window-size, scale | options | flags | payload
        self.version = version
        self.ttl = ttl
        self.op_len = op_len
        self.mss = mss
        self.win_size = win_size
        self.scale = scale
        if op_len > 0:
            self.options = options
        else:
            self.options = []
        self.flags = flags
        self.payload = payload

class MTU_sig:

    def __init__(self, link = "Ethernet", mtu = 0):
        #mtu sig  = link | mtu
        self.link = link
        self.mtu = mtu

class HTTP_sig:

    def __init__(self, version = "all", headers = [], no_headers = [], desc = ""):
        #http sig = version | headers | no-headers | desc
        self.version = version
        self.headers = headers
        self.no_headers = no_headers
        self.desc = desc