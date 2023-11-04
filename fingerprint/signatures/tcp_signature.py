
class TCP_sig:

    def __init__(self, version = "all", ttl = 128, op_len = 0, mss = 0, win_size = 0, scale = 0, options = [], flags = {}, payload = "") -> None:
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
