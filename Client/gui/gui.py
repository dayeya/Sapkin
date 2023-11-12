import customtkinter as ctk

class ScrollableClients(ctk.CTkScrollableFrame):
    
    def __init__(self, master, **kwargs) -> None:
        """
        Scrollable Clients Frame.

        Args:
            master (list): Arguments for custommization.
        """
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(master=self, text='Online Clients')
        self.label.grid(row=0, column=0)

class Logger:
    pass

class View(ctk.CTk):
    
    def __init__(self) -> None:
        """
        View object.
        """
        super().__init__()
        
        self.title("Sapkin Client")
        self.geometry(f'{800}x{500}')
        
        # Rows
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self._clients_logger = ScrollableClients(
            master=self, 
            fg_color='red'
        )
        
        self._clients_logger.grid(column=0, sticky='ns')
        