from gui import MainView, View
from module import Module, SynHandler

import sys
from threading import Thread

class Client:
    
    def __init__(self, name: str) -> None:
        """
        Client object.
        :param mod:
        """
        self.gui = MainView(self, name)
        self.gui.protocol("WM_DELETE_WINDOW", self.terminate)
        
        # Threads.
        self._main_thread = Module(self, name)
        self._syn_thread = SynHandler()
        
        self._main_thread.start()
        self.gui.mainloop()
    
    def get_os_by_name(self, name) -> None:
        print(self._main_thread.get_os(name))
    
    def log_user(self, name, ip) -> None:
        self.gui.log_user(name, ip) 
    
    def terminate(self) -> None:
        """
        Closes the client completely.
        """
        self.gui.destroy()
        
def sign_up() -> str:
    """
    Opens the sign up window.
    """
    gui = View()
    gui.mainloop()
    return gui.name

if __name__ == "__main__":
    name = sign_up()
    if name:
        client = Client(name)
        
    # No input was given.
    pass