from module import Module

class Client:
    
    def __init__(self, mod):
        self.module = mod

    def start(self):
        
        """
        Boots up the client.
        """
        
        # start communication.
        self.module.send_data()

if __name__ == "__main__":
    module = Module()
    client = Client(module)
    
    # Boot the client.
    client.start()