from tkinter import *

class Subwindow:
    """Base class of all windows that are not the main program window"""
    def __init__(self, db_handler, window_geometry):
        """:param db_handler: the datebase handler object
        :param window_geometry: tuple with geometry information of the window [x_size, y_size, x_offset, y_offset]
        """
        self.db = db_handler
        self.geometry = window_geometry

    def display(self):
        """Displays the window. Unhides it if it already exits, creates it if not."""
        try:
            self.window.deiconify()
        except:
            self._create_window()
        self.window.focus_set()

    def _hide(self):
        """Hides the window"""
        try: 
            self.window.withdraw()
        except:
            pass

    def _close(self):
        """Closes the window (destroy Toplevel object)"""
        try:
            self.window.close()
        except:
            pass

    def _create_window(self):
        """Creates the window"""
        
        #create the window
        self.window = Toplevel()
        geometry = f"{self.geometry[0]}x{self.geometry[1]}+{self.geometry[2]}+{self.geometry[3]}"
        self.window.geometry(geometry)

        #all general functionality goes here:
        #store the gridrow that we are currently building on
        self.gridrow = 0

        #change 'x' button behavour from close to hide
        self.window.protocol("WM_DELETE_WINDOW", self._hide)

        

   
        

