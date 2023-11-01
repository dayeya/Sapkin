from module import Module


class Client:
    
    def __init__(self, mod) -> None:
        """
        Client object.
        :param mod:
        """
        self.module = mod

    def start(self) -> None:
        """
        Connects a client into the server.
        :return: None
        """
        self.module.send_data()


if __name__ == "__main__":
    module = Module()
    client = Client(module)
    client.start()

