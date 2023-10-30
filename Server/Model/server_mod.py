from socket import *
from threading import Thread

class Server:
    
    UTF = "utf-8"
    BUFSIZE = 1024
    ONLINE_CLIENT_BOUND = 5
    ADDRESS = ("192.168.1.218", 60000)
    
    def __init__(self) -> None:
        """
        Server Object.
        """
        self.main_sock = socket(AF_INET, SOCK_STREAM)
        
    def start(self) -> None:
        """
        Starts the server, listening to Sapkin clients.
        """
        self.main_sock.bind(Server.ADDRESS)
        self.main_sock.listen(Server.ONLINE_CLIENT_BOUND)
        
        while True:
            
            # SERVER_SOCK of client.
            fp_server_sock, addr = self.main_sock.accept()
            
            # connection with the SERVER_SOCK of the client.
            fp_server_sock_connection = Thread(target=self.handle_fp_client, args=(fp_server_sock, addr))
            fp_server_sock_connection.start()
            

    def handle_fp_client(self, fp_client_sock: socket, addr: tuple) -> None:
        """

        Handles FingerPrinter client, 
        
        Args:
            fp_client_sock (socket): Clients socket for requests.
            addr (tuple): Clients sock address.
        """
        while True:
            
            req = fp_client_sock.recv(Server.BUFSIZE).decode(Server.UTF)
            if not req:
                break
            
            fp_client_sock.send(self.encode(f"Echoed - {req}"))
            
        fp_client_sock.close()
        
        
    def encode(self, str) -> bytes:
        """
        
        Returns an encoded representation of str.

        Args:
            str (_type_): str to encode.

        Returns:
            bytes: encoded bytes from str.
        """
             
        return str.encode(Server.UTF)    
