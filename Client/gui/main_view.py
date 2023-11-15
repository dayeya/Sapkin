import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont

import os, sys
from PIL import Image
from help import Help_Window
from navigation import NavBar
from settings import Settings_Window
from utils import NO_COLOR, BLANK

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"

class ScrollableClients(ctk.CTkScrollableFrame):
    
    def __init__(self, master, **kwargs) -> None:
        """
        Scrollable Clients Frame.

        Args:
            master (list): Arguments for customization.
        """
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        
        self._slots = []

class Logger(ctk.CTkScrollableFrame):
    
    def __init__(self, master, **kwargs) -> None:
        """
        Logger Frame.
        
        Args:
            master (list): Arguments for customization.
        """
        super().__init__(master, **kwargs)

class MainView(ctk.CTk):
    
    def __init__(self, name) -> None:
        """  
        View object.
        """
        super().__init__()
        self.title("Sapkin Fingerprinter")
        
        self._app_width = 800
        self._app_height = 500
        self.geometry(f'{self._app_width}x{self._app_height}')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.root = ctk.CTkFrame(master=self)
        self.root.grid(row=0, column=0, sticky='news')
        
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure((1, 2), weight=1)
        
        self._help_window = Help_Window(self, self.root, name)
        self._settings_window = Settings_Window(self, self.root, name)
        
        header = ctk.CTkLabel(master=self.root,text=f'Connected as - {name}')
        header.grid(row=0, column=0, padx=8, sticky='nws')
        
        users = ctk.CTkLabel(master=self.root,text=f'Online Clients')
        users.grid(row=0, column=1, sticky='we')
        
        logger = ctk.CTkLabel(master=self.root,text=f'Network logger')
        logger.grid(row=0, column=2, padx=8, sticky='news')
        
        self._bar = NavBar(master=self.root, fg_color=NO_COLOR, corner_radius=0,  width=int(self._app_width * .075))  
        self._bar._help_button.configure(command=lambda: self._display_help())
        self._bar._settings_button.configure(command=lambda: self._display_settings())
        self._bar.grid(row=1, column=0, sticky='news')    
    
        self._clients_logger = ScrollableClients(master=self.root, corner_radius=0, fg_color=NO_COLOR, width=int(self._app_width * .575))      
        self._clients_logger.grid(row=1, column=1, sticky='news')
        
        self._logger = Logger(master=self.root, corner_radius=0, fg_color=NO_COLOR, width=int(self._app_width * .35))
        self._logger.grid(row=1, column=2, sticky='news')
    
    def _display_help(self) -> None:
        """
        Switches from Home to Help window.
        """
        self.root.forget()
        self._help_window.grid(row=0, column=0, sticky='news')
        
    def _display_settings(self) -> None:
        """
        Switches from Home to Settings window.
        """
        self.root.forget()
        self._settings_window.grid(row=0, column=0, sticky='news')

if __name__ == "__main__":
    app = MainView('Daniel')
    app.mainloop()