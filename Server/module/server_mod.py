from ast import List
import pickle
import socket
from socket import *
from typing import List
from typing import List
from commands import *
from common import Document
from threading import Thread, Lock

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

            print(f'[+] Received: {req}')
            if req.type.upper() == ALL_USERS:
                response = Document(USERS, self.clients).serialize()
                fp_client_sock.send(response)

            elif req.type.upper() == SCAN:
                addr = fp_client_sock.getsockname()
                client_open_ports = self.scan_client_ports(addr, initial_port=49152, last_port=49252)
                response = Document(PORTS, client_open_ports).serialize()
                fp_client_sock.send(response)

            elif req.type.upper() == FP:
                print(f'[+] Passive finger printing of: {req.payload}.')

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
    def check_port(ports_lock: Lock, ports_list: list, addr: tuple):
        """
        Checks if a port is open.
        :param ports_list:
        :param addr:
        :param ports_lock:
        :return: a bool that indicates if a specific client's  certain port is open
        """
        port = addr[1]
        scan_sock = socket(AF_INET, SOCK_STREAM)
        with ports_lock:
            try:
                scan_sock.connect(addr)
                ports_list.append(port)
                scan_sock.close()
            except (Exception, ConnectionRefusedError) as e:
                print(f'[!] Port {port} is closed')

    def scan_client_ports(self, client_addr, initial_port=1, last_port=MAX_PORTS) -> list:
        """
        Scan the clients open ports from initial_port ot end.
        :param client_addr:
        :param initial_port:
        :param last_port:
        :return: A list of all open ports between initial_port and last_port
        """
        ip = client_addr[0]
        threads: List[Thread] = []
        open_ports: List[int] = []
        ports_lock: Lock = Lock()

        for port in range(initial_port, last_port + 1):
            addr = ip, port
            thread = Thread(target=self.check_port, args=(ports_lock, open_ports, addr))
            threads.append(thread)

        # Start scanning each port.
        for thread in threads:
            thread.start()

        # join with main thread.
        for thread in threads:
            thread.join()

        return open_ports
