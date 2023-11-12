import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont

class ScrollableClients(ctk.CTkScrollableFrame):
    
    def __init__(self, master, **kwargs) -> None:
        """
        Scrollable Clients Frame.

        Args:
            master (list): Arguments for customization.
        """
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(master=self, text='Online Clients')
        self.label.grid(row=0, column=0)

class Logger(ctk.CTkScrollableFrame):
    
    def __init__(self, master, **kwargs) -> None:
        """
        Logger Frame.

        Args:
            master (list): Arguments for customization.
        """
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(master=self, text='Logger')
        self.label.grid(row=0, column=0)

class MainView(ctk.CTk):
    
    def __init__(self) -> None:
        """
        View object.
        """  
        super().__init__()
        
        self.title("Sapkin Client")
        self.geometry(f'{800}x{500}')
        
        # Rows
        self.grid_rowconfigure(0, weight=1)
        
        # Columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._clients_logger = ScrollableClients(
            master=self, 
            fg_color='red'
        )
        
        self._logger = Logger(
            master=self, 
            fg_color='red'
        )
        
        self._clients_logger.grid(row=0, column=0, sticky='news')
        self._logger.grid(row=0, column=1, sticky='news')
    