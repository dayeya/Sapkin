import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont

ENTER_KEY = '<Return>'

class NameEntry(ctk.CTkEntry):
    
    def __init__(self, master, **kwargs) -> None:
        """
        Entry object.

        Args:
            master (list): Arguments for customization.
        """
        super().__init__(master, **kwargs)
        self.bind(ENTER_KEY, lambda event: self.register(event))
        
    def register(self, event) -> None:
        """
        Handels name.
        """
        name = self.get()
        if not name:
            print("Name is in the wrong format!")
        else:
            print(name)
        
        
class View(ctk.CTk):
    
    def __init__(self, *args, **kwargs) -> None:
        """
        View object.
        """  
        super().__init__(*args, **kwargs)
        self.title("Sign Up")
        
        self._app_width = 240
        self._app_height = 150
        
        center_x = int(self.winfo_screenwidth() / 2  + self._app_width / 2)
        center_y = int(self.winfo_screenheight() / 2 - self._app_height / 2)
        
        self.geometry(f'{self._app_width}x{self._app_height}+{center_x}+{center_y}')
        
        # Rows
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Columns
        self.grid_columnconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            master=self,
            text="Sapkin Client"
        )
        label.grid(row=0, column=0, sticky='news', padx=20)
        
        self._name_entry = NameEntry(
            master=self,
            placeholder_text='Register your name'
        )
        self._name_entry.grid(row=1, column=0, sticky='news', padx=20, pady=20)
        
    def termiante(self) -> None:
        """
        Closes the GUI.
        """
        gui.destroy()
        
if __name__ == '__main__':
    gui = View()
    gui.protocol("WM_DELETE_WINDOW", gui.termiante)
    
    # Run the GUI
    gui.mainloop()
    