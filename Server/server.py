from module import Module
from session_handler import SessionHandler

class Server:
    
    def __init__(self) -> None:
        """
        Creates Server object.
        """
        self.server_handler = Module()
        self.sessions_handler = SessionHandler()

    def close_server(self) -> None:
        """
        Closes the server.
        :return: None
        """
        self.main_sock.close()


if __name__ == "__main__":
    server = Server()
    server.start()
