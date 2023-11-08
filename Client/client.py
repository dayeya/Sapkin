from module import Module


class Client:
    
    def __init__(self) -> None:
        """
        Client object.
        :param mod:
        """
        self.module = Module()

    def start(self) -> None:
        """
        Connects a client into the server.
        :return: None
        """
        self.module.send_data()


if __name__ == "__main__":
    client = Client()
    client.start()

