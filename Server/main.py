from Model.server_mod import Module


class Server(Module):
    
    def __init__(self) -> None:
        """
        Creates Server object, initializes its module.
        """
        super().__init__()

    def clone_server(self) -> None:
        """
        Closes the server.
        """
        self.main_sock.close()

if __name__ == "__main__":
    server = Server()
    
    # run the server.
    server.start()