"""
contains information about different identifiers of operating systems
The plan is to copy the dict into a new dict before using it, and then remove
keys that their identifiers don't match the info that we received from the clients
until we are only left with one operating system.
"""
OS_INFO = {}


class OS_dict:

    def __init__(self, OS_type: str, TTL: int) -> None:
        """
        creates a dictionary with info about different params of operating systems that are useful for fingerprinting
        Args:
            OS_type:
            TTL:
        """
        info = {"os_type": OS_type, "TTL": TTL}
        self.info = info


def initialize_os_info():
    TCP_list = []
    ICMP_list = []

    """
    TCP identifiers
    """
    TCP_list.append(OS_dict("Windows 10", 128))
    TCP_list.append(OS_dict("Linux", 64))
    TCP_list.append(OS_dict("Mac OS", 64))
    """
    ICMP identifiers
    """
    ICMP_list.append("Windows 10", 255)
    ICMP_list.append("Linux", 255)
    ICMP_list.append("Mac OS", 255)

    OS_INFO["TCP"] = TCP_list
    OS_INFO["ICMP"] = ICMP_list
