import os
import sys
import pickle
from ast import List
from socket import *
from threading import Thread, Lock
from session_handler import SessionHandler

try: 
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(parent_dir)
    from common import Document
    
except ModuleNotFoundError as e:
    raise Exception("Check project dir as common was not found.")

ADDRESS = ('localhost', 60000)

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
        self._main_sock = socket(AF_INET, SOCK_STREAM)
        
        self.sessions_handler = SessionHandler()
        
    def start(self) -> None:
        """
        Starts the server, listening to clients.
        """
        self._main_sock.bind(ADDRESS)
        self._main_sock.listen(Module.ONLINE_CLIENT_BOUND)
        print(f"[+] Server is up!")
        
        self.sessions_handler.start()
        
        while True:
            fp_server_sock, addr = self._main_sock.accept()
            
            # connection with the SERVER_SOCK of the client.
            self.add_client(addr)
            fp_server_sock_connection = Thread(target=self.handle_fp_client, args=(fp_server_sock, addr))
            fp_server_sock_connection.start()
    
    def close(self) -> None:
        """
        Closes the server.
        """
        self._main_sock.close()

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
            if req.type.upper() == "ALL_USERS":
                response = Document("USERS", self.clients).serialize()
                fp_client_sock.send(response)

            elif req.type.upper() == "SCAN":
                addr = fp_client_sock.getsockname()
                client_open_ports = self._scan_client_ports(addr, initial_port=1, last_port=Module.MAX_PORTS)
                response = Document("PORTS", client_open_ports).serialize()
                fp_client_sock.send(response)

            elif req.type.upper() == "FP":
                print(f'[+] Passive finger printing of: {req.payload}.')

            else:
                response = Document("ECHO", f"Echoed! {req.payload}").serialize()
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
    def _check_port(ports_lock: Lock, ports_list: list, addr: tuple) -> None:
        """
        Checks if a port is open.
        :param ports_list:
        :param addr:
        :param ports_lock:
        :return: a bool that indicates if a specific client's  certain port is open
        """
        port = addr[1]
        scan_sock = socket(AF_INET, SOCK_STREAM)
        scan_sock.settimeout(0.5)
        
        # Access LOCK
        with ports_lock:
            try:
                scan_sock.connect(addr)
                ports_list.append(port)
                scan_sock.close()
            except (Exception, ConnectionRefusedError) as e:
                print(f'[!] Port {port} is closed')

    def _scan_client_ports(self, client_addr, initial_port=1, last_port=MAX_PORTS) -> list:
        """
        Scan the clients open ports from initial_port ot end.
        :param client_addr:
        :param initial_port:
        :param last_port:
        :return: A list of all open ports between initial_port and last_port
        """
        ip = client_addr[0]
        ports_lock = Lock()
        threads: List[Thread] = []
        open_ports: List[int] = []
        popular_ports = [
            (21, "FTP"), 
            (22, "SSH"), 
            (25, "SMTP"), 
            (80, "HTTP"), 
            (443, "HTTPS"), 
            (110, "POP3"), 
            (143, "IMAP"),
            (3306, "MySQL"), 
            (5432, "PostgreSQL"), 
            (27017, "MongoDB")
        ]
        
        for port in popular_ports:
            addr = ip, port[0]
            thread = Thread(target=self._check_port, args=(ports_lock, open_ports, addr))
            threads.append(thread)

        # Start scanning each port.
        for thread in threads:
            thread.start()

        # join with main thread.
        for thread in threads:
            thread.join()

        return open_ports
