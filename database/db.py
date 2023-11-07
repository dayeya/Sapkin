from typing import Iterator
from .loaders import TCPLoader, MTULoader, HTTPLoader

class Database:
    
    def __init__(self) -> None:
        """
        Database object, will handle all data.
        """
        self._tcp_loader  = TCPLoader()
        self._mtu_loader  = MTULoader()
        self._http_loader = HTTPLoader()
        
    def iter_tcp(self) -> Iterator:
        """
        Return:
            Iterator: Iterator object of all os-tcp signatures
        """
        return iter(self._tcp_loader
                    .load()
                    .items()
                    )
            
    def iter_mtu(self) -> Iterator:
        """
        Return:
            Iterator: Iterator object of all os-tcp signatures
        """
        return iter(self._mtu_loader
                    .load()
                    .items()
                    )
            
    def iter_http(self) -> Iterator:
        """
        Return:
            Iterator: Iterator object of all os-tcp signatures
        """
        return iter(self._http_loader
                    .load()
                    .items()
                    )
        
OSF_DATABASE = Database()