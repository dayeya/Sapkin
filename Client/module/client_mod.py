import os
import sys
import pickle
from socket import *
from .syn import SynHandler

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

    def __init__(self) -> None:
        """
        Client Module object.
        """
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.connect(ADDRESS)
        self._syn_handler = SynHandler()
        
        # Socket for regular communication.
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        
    def _stop_syn(self) -> None:
        """
        Stops sending syn packets to the server.
        """
        self._syn_handler.join()
    
    def receive(self) -> Document:
        """
        Receives data from the server.
        :return: Document.
        """
        data = self.server_sock.recv(Module.BUFSIZE)
        if not data:
            raise Exception("Connection with the server has timed out.")
        
        # More data to receive.
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