class MTU_sig:

    def __init__(self, link = "Ethernet", mtu = 0) -> None:
        #mtu sig  = link | mtu
        self.link = link
        self.mtu = mtu