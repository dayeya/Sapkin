import pickle
from socket import *
from threading import Thread

from common import Document


class Module:
    
    UTF = "utf-8"
    BUFSIZE = 1024
    ONLINE_CLIENT_BOUND = 5
    ADDRESS = ('192.168.1.218', 60000)
    
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
                
            else:
                fp_client_sock.send(self.encode(f"Echoed - {req}"))
            
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
