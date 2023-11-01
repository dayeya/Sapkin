from module import Module


class Server(Module):
    
    def __init__(self) -> None:
        """
        Creates Server object.
        """
        super().__init__()

    def close_server(self) -> None:
        """
        Closes the server.
        :return: None
        """
        self.main_sock.close()


if __name__ == "__main__":
    server = Server()
    server.start()
