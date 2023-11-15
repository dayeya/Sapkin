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
        self.gui = MainView(name)
        self.gui.protocol("WM_DELETE_WINDOW", self.terminate)
        
        # Threads.
        self._main_thread = Module(name)
        self._syn_thread = SynHandler()
        self._main_thread.start()
        # self._syn_thread.start()
        
        self.gui.mainloop()
        
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