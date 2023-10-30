from Model.server_mod import Module


class Server(Module):
    
    def __init__(self) -> None:
        """
        Creates Server object.
        """
            
        # init module.
        super().__init__()


if __name__ == "__main__":
    server = Server()
    
    # run the server.
    server.start()