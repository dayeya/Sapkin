from typing import TypeVar

# HTTP version can be 1.0, 1.1, 2.0, or ALL.
Version = TypeVar("HTTP_Version", str)

class HTTPSignature:

    def __init__(self, 
                 version: Version="ALL", 
                 headers=[], 
                 no_headers=[], 
                 desc=""
            ) -> None:
        """
        HTTPSignature object. 

        Args:
            version    (str, optional): version, 1.0 / 1.1 or any. Defaults to "ALL"
            headers    (list, optional): headers of the corresponding packet. Defaults to []
            no_headers (list, optional): absent headers from the corresponding packet. Defaults to []
            desc       (str, optional): 'User-Agent' or 'Server'. Defaults to ""
        """
        self.version = version
        self.headers = headers
        self.no_headers = no_headers
        self.desc = desc
        
    def __str__(self) -> str:
        """
        Returns:
            str: String representation of self
        """
        return f"HTTPSignature: 
                {self.version}:
                {self.headers}:
                {self.no_headers}:
                {self.desc}"
