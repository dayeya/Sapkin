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
        self._socks = []
        self._clients = {}
        self.main_sock = socket(AF_INET, SOCK_STREAM)

        # Thread for handling user threads and data.
        self.sessions_handler = SessionHandler()
        
    def start(self) -> None:
        """
        Starts the server, listening to clients.
        """
        self.main_sock.bind(ADDRESS)
        self.main_sock.listen(Module.ONLINE_CLIENT_BOUND)
        print(f"[+] Server is up!")

        self.sessions_handler.start()
        
        while True:
            fp_server_sock, addr = self.main_sock.accept()
            fp_server_sock_connection = Thread(target=self._handle_client, args=(fp_server_sock, addr))
            fp_server_sock_connection.start()

    def _handle_client(self, client_sock: socket, addr: tuple) -> None:
        """
        Handles the connections of a client.
        :param fp_client_sock:
        :param addr:
        :return: None
        """
        while True:
            try:
                req = pickle.loads(client_sock.recv(Module.BUFSIZE))
                if not req or not isinstance(req, Document):
                    break
                self._handle_doc(req, client_sock, addr)
            except ConnectionAbortedError:
                print("[!] Connection aborted! closing session with client.")
                break   
            
        client_sock.close()
        
    def _handle_doc(self, req: Document, sock: socket, addr: tuple) -> None:
        """
        Handles all requests.
        Args:
            req (Document): Document.
            sock (socket): Clients socket.
            addr (tuple): Address.
        """
        if req.type.upper() == 'LOG_IN':
            response = Document('ACK').serialize()
            sock.send(response)
            
            # Add client to db.
            with req as name:
                self._clients[name] = addr
                self._socks.append(sock)
                self._broadcast_user(name)
    
        elif req.type.upper() == 'ALL_USERS':
            response = Document('USERS', self._clients).serialize()
            sock.send(response)

        elif req.type.upper() == 'SCAN':
            client_open_ports = self._scan_client_ports(addr, initial_port=1, last_port=Module.MAX_PORTS)
            response = Document('PORTS', client_open_ports).serialize()
            sock.send(response)

        elif req.type.upper() == 'FP_USER':
            pass
    
    def _broadcast_user(self, name) -> None:
        """
        Updates all users.

        Args:
            name (str): Name of the new user.
        """
        doc: bytes = Document('NEW_USER', (name, self._clients[name][0])).serialize()
        for sock in self._socks:
            sock.send(doc)

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
        threads: list = []
        open_ports: list = []
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