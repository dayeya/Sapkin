from socket import *

ADDRESS = ('192.168.1.218', 60000)

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

    def recieve(self) -> str:
        """
        Recieves data from the server.

        Returns:
            bytes: bytes representation of the sent data.
        """
        data: bytes = b''
        
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
        
        return data.decode(Module.UTF)
    
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
            encoded_msg: bytes = self.encode(client_msg)
            self.server_sock.send(encoded_msg)
            
            data = self.recieve()
            print(f"[+] {data}")
            
    def encode(self, str) -> bytes:
        """
        Returns an encoded representation of str.

        Args:
            str (_type_): str to encode.

        Returns:
            bytes: encoded bytes from str.
        """
             
        return str.encode(Module.UTF)   



            
    


        

