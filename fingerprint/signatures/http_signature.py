from typing import TypeVar

# HTTP version can be 1.0, 1.1, 2.0, or ALL.
Version = TypeVar("Version", str, None)
req_common_headers = {
    "Host",
    "User-Agent",
    "Connection",
    "Accept",
    "Accept-Encoding",
    "Accept-Language",
    "Accept-Charset",
    "Keep-Alive"
}
resp_common_headers = {
    "Content-Type",
    "Connection",
    "Keep-Alive",
    "Accept-Ranges",
    "Date"
}

class HTTPSignature:

    def __init__(self, 
                 version: Version="ALL", 
                 headers="", 
                 desc="",
                 type = ""
            ) -> None:
        """
        HTTPSignature object. 

        Args:
            version    (str, optional): version, 1.0 / 1.1 or any. Defaults to "ALL"
            headers    (str, optional): headers of the corresponding packet. Defaults to ""
            desc       (str, optional): 'User-Agent' or 'Server'. Defaults to ""
            type       (str, optional): 'resp' or 'req'. Defaults to "".
        """
        self.version = version
        self.headers = headers
        self.desc = desc
        self.type = type

        missing = []
        if type == 'req':
            for h in req_common_headers:
                if h not in headers:
                    missing.append(h)
        elif type == 'resp':
            for h in resp_common_headers:
                if h not in headers:
                    missing.append(h)
        """
          no_headers (list): absent headers from the corresponding packet.
        """
        self.no_headers = missing
                    
        
    def __str__(self) -> str:
        """
        Returns:
            str: String representation of self
        """
        return f"HTTPSignature: " \
               f"{self.version}: " \
               f"{self.headers}: " \
               f"{self.no_headers}: " \
               f"{self.desc}"\
               f"{self.type}"
