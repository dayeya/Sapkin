import pydivert
import re
import psutil
from signatures.tcp_signature import *
from signatures.http_signature import *
from signatures.mtu_signature import *

class Sniffer:
    
    def __init__(self, filtr: str="true") -> None:
        """
        Sniffer Object

        Args:
            f (str, optional): Filter for the WinDivert. Defaults to None.
        """
        self._w = pydivert.WinDivert(filtr)

    def sniff_packets(self) -> None:
        """
        Sniffs packets.
        """
        
        print("Sniffing...")
        with self._w as packet_driver:
            for packet in packet_driver:
                print(packet)


def create_packet_sig(packet):
    """
    recieves a packet and returns it's signature
    """            
    #add consideration for inbbound and outbound packets
    ip_header = packet.ip
    if ip_header.protocol == 6:
        #means that this is a tcp packet (almost every HTTP packet is transmitted using TCP/IP).

        #common HTTP methods that are present in HTTP packets
        methods = 'GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE'

        packet_data = packet.tcp.payload.decode('utf-8','ignore')
        if re.search(methods, packet_data):
            #means that this is an HTTP packet since it's data contains HTTP methods
            print("this is an HTTP packet")

            #we are seperating the packet data into two parts, HTTP headers and HTTP message content, the first occurance of the '\r\n\r\n' string seperates the headers and the content
            headers, content = packet_data.split('\r\n\r\n', 1)

            #http sig = version | headers | no-headers | desc
            #WE NEED TO DETERMINE WHAT NEEDS TO BE PUT IN THE NO-HEADERS ATTRIBUTE AND THE DESC ATTRIBUTE.
            protocol_sig = HTTP_sig("all", headers, None, "")
        else:
            #means that this is a regular TCP packet
            print("this is a regular TCP packet")

            #checks what type of ip address does the packet have so that we can get the TTL attribute correctly
            if packet.is_ipv4:
                ttl = packet.ipv4.ttl
            else:
                ttl = packet.ipv6.hop_limit

            #checks if the packet has the options attribute
            if hasattr(packet.tcp, 'options'):
                options = packet.tcp.options
                op_len = len(options)
            else:
                options = None
                op_len = 0
            
            #checks if the packet has the mss attrubute
            if hasattr(packet.tcp, 'mss'):
                mss = packet.tcp.mss
            else:
                mss = None
            
            window_size = packet.tcp.window_size
            scale = packet.tcp.window_scale

            flags = packet.tcp.flags
            syn_flag = False
            ack_flag = False
            fin_flag = False
            #we are using the AND bitwise operator to check which flags are raised, if the expression isn't equal to 0, it means that the flag that we checked is turned on.
            if flags & pydivert.TCP_FLAG_SYN:
                syn_flag = True
            if flags & pydivert.TCP_FLAG_ACK:
                ack_flag = True
            if flags & pydivert.TCP_FLAG_FIN:
                fin_flag = True
            flags = {"syn":syn_flag, "ack":ack_flag, "fin":fin_flag}
            payload = packet.payload
            #tcp sig  = version | ttl | options-len | mss | window-size, scale | options | flags | payload
            protocol_sig = TCP_sig("all", ttl, op_len, mss, window_size, scale, options, flags, payload)

        #MTU signature
        
        #determines if the packet was transmitted over ethernet or wifi
        #WE NEED TO ADD OTHER TYPES OF LINKS
        link = packet.adapter_name
        
        #finds out the mtu value
        try:
            mtu_val = psutil.net_if_stats()[link].mtu
        except Exception as e:
            mtu_val = None
            print(e, " has occured")
        #mtu sig  = link | mtu
        mtu_sig = MTU_sig(link, mtu_val)

        sig = {"Protocol":protocol_sig, "MTU_sig":mtu_sig}
        return sig
        




