from socket import *



class Client_Model:
    """server ip address and port
    """
    UTF = "utf-8"
    HOST = '192.168.1.147'
    PORT = 60000
    BUFFER_SIZE = 1024

    def __init__(self)->None:
        """creates the client-server socket and the client-client socket
        """
        self.server_sock = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect((Client_Model.HOST, Client_Model.PORT))
        
        
        self.client_sock = socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_data(self):
        """recieves and interprets the data recieved from the server/client
        """
        info = b''
        while True:
            try:
                if info != b'':
                    #recv is a stopping function so if no data is receievd we just get stuck
                    #CHECK IF NECESSARY
                    self.server_sock.settimeout(1)
                try:
                    chunk = self.server_sock.recv(Client_Model.BUFFER_SIZE)
                except socket.timeout:
                    chunk = b''
            except ConnectionAbortedError:
                print("Connection abruptly disconnected")
                return info
            if len(chunk) <= 0:
                return info
            info += chunk
        return info
    
    def send_data(self):
        """responsible for sending data to the server"""
        while True:
            #from_server = self.get_data().decode(Client_Model.UTF)
            send = input("send something to the server")
            if send != "stop":
                self.server_sock.send(send.encode(Client_Model.UTF))
            else:
                break



            
    


        

