from module import Module

class Server:
    def __init__(self) -> None:
        self.server_handler = Module()
        
    def run(self) -> None:
        self.server_handler.start()

    def close_server(self) -> None:
        self.server_handler.close()

if __name__ == "__main__":
    server = Server()
    server.run()
