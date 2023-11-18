import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont

from .navigation import NavBar
from .utils import NO_COLOR, BLANK

class Help_Window(ctk.CTkFrame):
    
    DESCRIPTION = """
        Welcome to Sapkin, an online passive OS fingerprinting tool.
        Credit to p0f.
    """
    
    def __init__(self, master, root_dir, name, **kwargs) -> None:
        """
        View object.
        """
        super().__init__(master, **kwargs)
        self._app_width = 800
        self._app_height = 500
        
        self._parent = root_dir # Main Frame.
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkLabel(master=self ,text=f'Connected as - {name}')
        header.grid(row=0, column=0, columnspan=2, padx=8, sticky='nws')
        
        self.bar = NavBar(master=self, fg_color=NO_COLOR, corner_radius=0,  width=int(self._app_width * .075))
        self.bar._home_button.configure(command=lambda: self._display_main())
        self.bar.grid(row=1, column=0, sticky='news')
        
        self._description = ctk.CTkLabel(
            master=self,
            text=Help_Window.DESCRIPTION
        )
        self._description.grid(row=1, column=1, sticky='news')
        
    def _display_main(self) -> None:
        """
        Returns into Main Window.
        """
        self.grid_forget()
        self._parent.grid(row=0, column=0, sticky='news')