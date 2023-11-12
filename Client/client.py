from gui import View
from module import Module, SynHandler

import sys
from threading import Thread

class Client:
    
    def __init__(self) -> None:
        """
        Client object.
        :param mod:
        """
        self.gui = View()
        self._main_thread = Module()
        self._syn_thread = SynHandler() 
        
    def start_syn(self) -> None:
        """
        Starts the SynHandler.
        """
        self._syn_thread.start()
            
    def stop_syn(self) -> None:
        """
        Stops sending syn packets to the server.
        """
        self._syn_thread.join()  

    def start_main(self) -> None:
        """
        Communication with the server.
        """ 
        self._main_thread.start()
        
    def stop_main(self) -> None: 
        """
        Stops main thread.
        """
        self._main_thread.join()
        
        
    def terminate(self) -> None: 
        """
        Terminates the application.
        """
        self._main_thread.join()
        
        # Close GUI.
        self.gui.destroy()
        

if __name__ == "__main__":
    client = Client()
    
    client.start_main()
    # client.start_syn()
    
    sys.exit(client.gui.mainloop())