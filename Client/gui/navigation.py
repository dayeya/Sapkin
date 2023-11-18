import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont

import os, sys
from PIL import Image
from .utils import NO_COLOR, BLANK, ROOT_FOLDER

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"

class NavBar(ctk.CTkFrame): 
    
    def __init__(self, master, **kwargs) -> None:
        """
        NavBar Frame.
        
        Args:
            master (list): Arguments for customization.
        """
        super().__init__(master, **kwargs)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # Button width.
        button_width = self.winfo_reqwidth() * 0.9
                                  
        self._home_image = ctk.CTkImage(dark_image=Image.open(os.path.join(ROOT_FOLDER, "white_home.png")), size=(24, 24))
        self._home_button = ctk.CTkButton(master=self, text=BLANK, width=button_width, image=self._home_image, 
                fg_color=NO_COLOR,
                corner_radius=0
            )
        self._home_button.grid(row=0, column=0, pady=4, sticky='w')
                
        self._settings_image = ctk.CTkImage(dark_image=Image.open(os.path.join(ROOT_FOLDER, "settings.png")), size=(35, 35))
        self._settings_button = ctk.CTkButton(master=self, text=BLANK, width=button_width, image=self._settings_image, 
                fg_color=NO_COLOR,
                corner_radius=0
            )
        self._settings_button.grid(row=1, column=0, pady=4, sticky='w')
                
        self._help_image = ctk.CTkImage(dark_image=Image.open(os.path.join(ROOT_FOLDER, "help.png")), size=(32, 21))
        self._help_button = ctk.CTkButton(master=self, text=BLANK, width=button_width, image=self._help_image, 
                fg_color=NO_COLOR,
                corner_radius=0
            )
        self._help_button.grid(row=3, column=0, pady=4, sticky='w')