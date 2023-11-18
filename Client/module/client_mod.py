import os
import sys
import pickle
from socket import *
from .syn import SynHandler
from threading import Thread

try: 
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(parent_dir)
    from common import Document
    
except ModuleNotFoundError as e:
    raise Exception("Check project dir as common was not found.")

ADDRESS = ('localhost', 60000)

class Module(Thread):
    
    UTF = "utf-8"
    BUFSIZE = 1024

    def __init__(self, controller, name: str) -> None:
        """
        Client Module object.
        """
        self._name = name
        self._controller = controller
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.connect(ADDRESS)
        
        # Register the name into the server.
        self._login()
        super().__init__(target=self.receive)
        
    def end(self) -> None:
        """
        Terminates the Module.
        """
        self.server_sock.close()
        sys.exit(self.join())
        
    def get_os(self, name) -> str:
        encoded_req: bytes = Document('FP_USER', self._name).serialize()
        self.server_sock.send(encoded_req)
        
    def _login(self) -> None: 
        """
        Updates the server with the name.
        Raises:
            Exception: Login was not successfull.
        """
        encoded_req: bytes = Document('LOG_IN', self._name).serialize()
        self.server_sock.send(encoded_req)
        
        data = self._recv()
        if data.type != 'ACK':
            raise Exception("[!] Unable to login.")
    
    def _recv(self) -> Document:
        """
        Receivs a Document.
        Returns:
            Document: Document.
        """
        data = self.server_sock.recv(Module.BUFSIZE)
        if not data:
            raise Exception("[!] Connection with the server has timed out.")
        
        # More data to receive.
        if len(data) == Module.BUFSIZE:
            while True:
                try: 
                    data += self.server_sock.recv(Module.BUFSIZE)
                except: 
                    break
        
        data = pickle.loads(data)
        if not isinstance(data, Document):
            raise Exception("[!] Wasn't given a document, please try again!")
        
        return data
    
    def receive(self) -> None:
        """
        Receives data from the server.
        :return: Document.
        """
        while True:
            self._handle_reponse(self._recv())
        
    def _handle_reponse(self, data: Document) -> None:
        payload = data.payload
        msg = data.type
        print(f'msg: {msg}, payload: {payload}')
        
        if msg == 'NEW_USER':
            self._controller.log_user(name=payload[0], ip=payload[1])
        