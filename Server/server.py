from module import Module

class Server:
    
    def __init__(self) -> None:
        """
        Creates Server object.
        """
        self.server_handler = Module()
        
    def run(self) -> None:
        """
        Starts the server.
        """
        self.server_handler.start()

    def close_server(self) -> None:
        """
        Closes the server.
        :return: None
        """
        self.main_sock.close()

if __name__ == "__main__":
    server = Server()
    server.run()
