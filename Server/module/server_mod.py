import pickle
from socket import *
from threading import Thread

from Sapkin_Finger_Printer.common import *


class Module:
    
    UTF = "utf-8"
    BUFSIZE = 1024
    ONLINE_CLIENT_BOUND = 5
    ADDRESS = ('192.168.1.147', 60000)
    
    def __init__(self) -> None:
        """
        Server module Object.
        """
        self.clients = []
        self.main_sock = socket(AF_INET, SOCK_STREAM)
        
    def start(self) -> None:
        """
        Starts the server, listening to clients.
        """
        self.main_sock.bind(Module.ADDRESS)
        self.main_sock.listen(Module.ONLINE_CLIENT_BOUND)
        
        print(f"[+] Server is up!")
        while True:
            
            # SERVER_SOCK of client.
            fp_server_sock, addr = self.main_sock.accept()
            
            # connection with the SERVER_SOCK of the client.
            self.add_client(addr)
            fp_server_sock_connection = Thread(target=self.handle_fp_client, args=(fp_server_sock, addr))
            fp_server_sock_connection.start()

    def handle_fp_client(self, fp_client_sock: socket, addr: tuple) -> None:
        """
        Handles FingerPrinter client, 
        
        Args:
            fp_client_sock (socket): Clients socket for requests.
            addr (tuple): Clients sock address.
        """
        
        print(f'[+] New client at: {addr}')
        while True:
            
            req = pickle.loads(fp_client_sock.recv(Module.BUFSIZE))
            if not req or not isinstance(req, Document):
                break
            
            # Document asks for all online FP clients.
            if req.type == "ALL USERS":
                response = Document("USERS", self.clients)
                print(f'[+] Crafted Document: {response}')
                
                fp_client_sock.send(response.serialize())
            elif req.type.upper() == "SCAN":
                client_address = str(fp_client_sock.getsockname()[0])
                print(client_address)
                open_ports = self.scan_client_ports(client_address, 1, 60000)
                print(open_ports)
                fp_client_sock.send(Document("Ports", open_ports)).serialize()
            else:
                fp_client_sock.send(Document(f"Echoed - {req}").serialize())
            
        fp_client_sock.close()
    
    def add_client(self, client_addr: tuple) -> None:
        """
        Adds client_addr to online clients.

        Args:
            client_addr (tuple): clients address.
        """
        self.clients.append(client_addr)
    
    def encode(self, data: str) -> bytes:
        """
        Returns an encoded representation of data.

        Args:
            data (str) to encode.

        Returns:
            bytes: encoded bytes from data.
        """
        
        return str.encode(Module.UTF)

    def is_port_open(self, client_addr, port_num, sock) -> bool:
        """

        Args:
            client_addr, port, sock:

        Returns:
            a bool that indicates if a specific client's  certain port is open
        """
        try:
            sock.connect(client_addr, port_num)
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

    def scan_client_ports(self, client_addr, start, end) -> list:
        """

        Args:
            client_addr, start, end:

        Returns:
            a list of all the open ports of a specific client between port numbers "start" and "end"
        """
        open_ports = []
        scan_sock = socket(AF_INET, SOCK_STREAM)
        for i in range(start, end + 1):
            if self.is_port_open(client_addr, i, scan_sock):
                open_ports.append(i)
        scan_sock.close()
        return open_ports
