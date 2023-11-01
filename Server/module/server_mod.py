import pickle
import socket
from socket import *
from commands import *
from common import Document
from threading import Thread

ADDRESS = ('192.168.1.218', 60000)


class Module:
    
    UTF = "utf-8"
    BUFSIZE = 1024
    MAX_PORTS = 65535
    ONLINE_CLIENT_BOUND = 5
    
    def __init__(self) -> None:
        """
        Server Modules object.
        """
        self.clients = []
        self.main_sock = socket(AF_INET, SOCK_STREAM)
        
    def start(self) -> None:
        """
        Starts the server, listening to clients.
        """
        self.main_sock.bind(ADDRESS)
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
        Handles the connections of a client.
        :param fp_client_sock:
        :param addr:
        :return: None
        """
        response: bytes = b''
        while True:
            req = pickle.loads(fp_client_sock.recv(Module.BUFSIZE))
            if not req or not isinstance(req, Document):
                break

            if req.type.upper() == ALL_USERS:
                response = Document(USERS, self.clients).serialize()
                fp_client_sock.send(response)

            elif req.type.upper() == SCAN:
                addr = str(fp_client_sock.getsockname()[0])
                client_open_ports = self.scan_client_ports(addr)
                response = Document(PORTS, client_open_ports).serialize()
                fp_client_sock.send(response)

            else:
                response = Document(ECHO, f"Echoed! {req.payload}").serialize()
                fp_client_sock.send(response)
            
        fp_client_sock.close()
    
    def add_client(self, client_addr: tuple) -> None:
        """
        Adds clients into online_clients.
        :param client_addr:
        :return: None
        """
        self.clients.append(client_addr)

    @staticmethod
    def check_port(client_addr, port, sock) -> bool:
        """
        Checks if a port is open.
        :param client_addr:
        :param port:
        :param sock:
        :return: a bool that indicates if a specific client's  certain port is open
        """
        try:
            addr = client_addr, port
            sock.connect(addr)
            return True
        except (Exception, ConnectionRefusedError) as e:
            print(f'[!] Error: {e}')
            return False

    def scan_client_ports(self, client_addr, initial_port=1, last_port=MAX_PORTS) -> list:
        """
        Scan the clients open ports from initial_port ot end.
        :param client_addr:
        :param initial_port:
        :param last_port:
        :return: A list of all open ports between initial_port and last_port
        """
        open_ports = []
        scan_sock = socket(AF_INET, SOCK_STREAM)
        for port in range(initial_port, last_port + 1):
            if self.check_port(client_addr, port, scan_sock):
                open_ports.append(port)

        scan_sock.close()
        return open_ports
