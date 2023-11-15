import customtkinter as ctk
from customtkinter import DISABLED, NORMAL
from customtkinter.windows.widgets.font import CTkFont

ENTER_KEY = '<Return>'

class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, error: str) -> None:
        """
        Error CTK window.

        Args:
            error (str): Error message.
        """
        super().__init__()
        self.title("Error!")
        self._app_width = 240
        self._app_height = 60
        
        center_x = int(self.winfo_screenwidth()  / 2 - self._app_width  / 2)
        center_y = int(self.winfo_screenheight() / 2 - self._app_height / 2)
        self.geometry(f'{self._app_width}x{self._app_height}+{center_x}+{center_y}')

        label = ctk.CTkLabel(self, text=error)
        label.pack(anchor=ctk.CENTER)

class View(ctk.CTk):
    
    def __init__(self, *args, **kwargs) -> None:
        """
        View object.
        """  
        super().__init__(*args, **kwargs)
        self.title("Sign Up")
        self._app_width = 240
        self._app_height = 120
        
        center_x = int(self.winfo_screenwidth()  / 2 + self._app_width / 2)
        center_y = int(self.winfo_screenheight() / 2 - self._app_height / 2)
        self.geometry(f'{self._app_width}x{self._app_height}+{center_x}+{center_y}')
        
        # Rows
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Columns
        self.grid_columnconfigure(0, weight=1)
        self._error_top_level = None
        
        label = ctk.CTkLabel(master=self, text="Sapkin Client")
        label.grid(row=0, column=0, sticky='news', padx=20)
        
        self._name_entry = ctk.CTkEntry(master=self, placeholder_text='Register your name')
        self.bind(ENTER_KEY, lambda event: self.register(event))
        self._name_entry.grid(row=1, column=0, sticky='news', padx=20, pady=20)
        
        # Client name.
        self.name = ''
        
    def __get__(self, instance, owner) -> str:
        """
        Returns:
            str: Name
        """
        return self.name
    
    def __set__(self, instance, name) -> None:
        """
        Sets self._name into value.
        """
        self.name = name
    
    def display_error(self, error: str) -> None:
        """
        Displayes an error message.
        """
        if not self._error_top_level or not self._error_top_level.winfo_exists():
            self._error_top_level = ErrorWindow(error)
            self._error_top_level.focus()            
        else:
            self._error_top_level.focus()
    
    def register(self, event) -> str:
        name = self._name_entry.get()
        if not name:
            self.display_error('Emtpy names are not supported.')
        
        else: 
            if self._error_top_level and self._error_top_level.winfo_exists():
                self._error_top_level.destroy()
            
            # Save the name.
            self.name = name
            self.destroy()