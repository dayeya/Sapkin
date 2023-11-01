import pickle
from Sapkin_Finger_Printer.common import *
from socket import *

ADDRESS = ('192.168.1.147', 60000)

class Module:
    
    """
    Client Module, defines the logic of the client.

    Returns:
        Client_Module: Modules part of MVC, logic
    """
    
    UTF = "utf-8"
    BUFSIZE = 1024

    def __init__(self) -> None:
        """
        Client_Module Object.
        """
        
        # Server sock, sends requests to the SERVER.
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.connect(ADDRESS)
        
        # Socket for regular communication.
        self.client_sock = socket(AF_INET, SOCK_STREAM)

    def receive(self) -> Document:
        """
        Receives data from the server.

        Returns:
            bytes: bytes representation of the received data.
        """
        
        data = self.server_sock.recv(Module.BUFSIZE)
        if not data:
            raise Exception("Connection with the server has timed out.")
        
        # if data was bigger than BUFFER_SIZE
        if len(data) == Module.BUFSIZE:
            while True:
                try: 
                    data += self.server_sock.recv(Module.BUFSIZE)
                except: 
                    break

        data = pickle.loads(data)
        if not isinstance(data, Document):
            raise Exception("Wasn't given a document, please try again!")

        return data
    
    def send_data(self) -> None:
        """
        Send requests to the server.
        """
        
        print("[+] Connected to server!\n")
        while True:
            client_msg = input("Type: ")
            
            # Stop program when typing STOP / stop.
            if client_msg.upper() == "STOP":
                break
            
            # Send encoded request.
            encoded_msg: bytes = Document(client_msg).serialize()
            self.server_sock.send(encoded_msg)
            
            data = self.receive()
            print(f"[+] {data}")

    @staticmethod
    def encode(data: str) -> bytes:
        """
        Returns an encoded representation of data.

        Args:
            data (str): data to encode.

        Returns:
            bytes: encoded bytes from str.
        """
             
        return data.encode(Module.UTF)



            
    


        

