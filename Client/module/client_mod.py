import os
import sys
import pickle
from socket import *

try: 
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(parent_dir)
    from common import Document
    
except ModuleNotFoundError as e:
    raise Exception("Check project dir as common was not found.")

ADDRESS = ('localhost', 60000)


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
        Client Module object.
        """
        
        # Server sock, sends requests to the SERVER.
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.connect(ADDRESS)
        
        # Socket for regular communication.
        self.client_sock = socket(AF_INET, SOCK_STREAM)

    def receive(self) -> Document:
        """
        Receives data from the server.
        :return: Document.
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
        Handles the clients' communication with the server.
        :return: None
        """
        
        print("[+] Connected to server!\n")
        while True:
            request = ''
            client_msg = input("Type: ").upper()

            if client_msg == "STOP":
                break

            elif client_msg == "ALL_USERS":
                request = "ALL_USERS"

            elif client_msg == "SCAN":
                request = "SCAN"

            elif client_msg.startswith("FP"):
                request, client_msg = client_msg.split(' ')
            else:
                request = "MSG"

            encoded_req: bytes = Document(request, client_msg).serialize()
            self.server_sock.send(encoded_req)
            
            data = self.receive()
            print(f"[+] {data.payload}")

    @staticmethod
    def encode(data: str) -> bytes:
        """
        Encodes data into bytes
        :param data:
        :return: bytes representation of data.
        """
        return data.encode(Module.UTF)



            
    


        

