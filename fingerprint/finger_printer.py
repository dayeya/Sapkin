import re
import psutil
from scapy.all import *
from scapy.layers import TCP
from scapy.layers.inet import IP, IPv6
from signatures import TCPSignature
from signatures import MTUSignature
from signatures import HTTPSignature
from packet_wrapper import PacketWrapper

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

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

#These patterns can be used to distinguish between HTTP response and request patterns.
HTTP_request_pattern = re.compile(r'^([A-Z]+)\s+/\S+\s+HTTP/\d+\.\d+', re.MULTILINE)
HTTP_response_pattern = re.compile(r'^HTTP/\d+\.\d+\s+(\d+) .+', re.MULTILINE)

def create_packet_sig(packet):
    """
    recieves a packet and returns it's signature
    """            
    #add consideration for inbbound and outbound packets
    is_TCP = False
    if IP in packet:
        ip_header = packet[IP]
        if ip_header.proto == 6:
            is_TCP = True
    elif IPv6 in packet:
        ip_header = packet[IPv6]
        if ip_header.nh == 6:
            is_TCP = True
    if is_TCP:
        #means that this is a tcp packet (almost every HTTP packet is transmitted using TCP/IP).

        #common HTTP methods that are present in HTTP packets
        methods = 'GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE'

        packet_data = str(packet[TCP].payload, 'utf-8', 'ignore')
        if re.search(methods, packet_data):
            #means that this is an HTTP packet since it's data contains HTTP methods
            print("this is an HTTP packet")

            payload = packet[Raw].load
            if re.search(HTTP_request_pattern, payload):
                #this is a request packet
                p_type = "req"
            elif re.search(HTTP_response_pattern, payload):
                #this is a response packet
                p_type = "resp"

            #we are seperating the packet data into two parts, HTTP headers and HTTP message content, the first occurance of the '\r\n\r\n' string seperates the headers and the content
            headers, content = packet_data.split('\r\n\r\n', 1)

            #http sig = version | headers | no-headers | desc
            #WE NEED TO DETERMINE WHAT NEEDS TO BE PUT IN THE NO-HEADERS ATTRIBUTE AND THE DESC ATTRIBUTE.
            protocol_sig = HTTPSignature("all", headers, None, p_type)
        else:
            #means that this is a regular TCP packet
            print("this is a regular TCP packet")

            #checks what type of ip address does the packet have so that we can get the TTL attribute correctly
            if IP in packet:
                ttl = packet[IP].ttl
            elif IPv6 in packet:
                ttl = packet[IPv6].hlim

            #checks if the packet has the options attribute
            tcp_header = packet[TCP]
            if 'options' in tcp_header.fields:
                options = tcp_header.options
                op_len = len(options)
            else:
                options = None
                op_len = 0
            
            #checks if the packet has the mss attrubute
            if 'mss' in tcp_header.fields:
                mss = tcp_header.mss
            else:
                mss = None
            
       
            window_size = tcp_header.window
            scale = tcp_header.ws

            flags = tcp_header.flags
            syn_flag = False
            ack_flag = False
            fin_flag = False
            #we are using the AND bitwise operator to check which flags are raised, if the expression isn't equal to 0, it means that the flag that we checked is turned on.
            if flags & SYN:
                syn_flag = True
            if flags & ACK:
                ack_flag = True
            if flags & FIN:
                fin_flag = True
            flags = {"syn":syn_flag, "ack":ack_flag, "fin":fin_flag}
            payload = packet.payload
            #tcp sig  = version | ttl | options-len | mss | window-size, scale | options | flags | payload
            protocol_sig = TCPSignature("all", ttl, op_len, mss, window_size, scale, options, flags, payload)

        #MTU signature
        
        #determines if the packet was transmitted over ethernet or wifi
        link = packet.sniffed_on
        
        #finds out the mtu value
        try:
            mtu_val = psutil.net_if_stats()[link].mtu
        except Exception as e:
            mtu_val = None
            print(e, " has occured")
        #mtu sig  = link | mtu
        mtu_sig = MTUSignature(link, mtu_val)

        sig = {"Protocol":protocol_sig, "MTU_sig":mtu_sig}
        return sig
        

