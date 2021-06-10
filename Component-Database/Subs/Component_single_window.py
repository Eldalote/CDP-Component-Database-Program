from tkinter import *
from Subs.Subwindow import Subwindow

class Component_single_window(Subwindow):
    """Base class for the single component windows, child of subwindow
    single component windows are the windows where all the information for a single component is presented, entered or edited"""

    def __init__(self, db_handler, screensize, window_position):
        """:param db_handler: the datebase handler object
        :param window_position: tuple with position information of the window [x_offset, y_offset]
        :param screensize: tuple with screensize in pixels
        """
        self.screensize = screensize
        x = int(screensize[0]*0.25)
        y = int(screensize[1]*0.3) 
        geometry = [x,y,window_position[0], window_position[1]]
        super().__init__(db_handler, geometry)


    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to single component windows go here
        """        
        #first we start by calling parent function
        super()._create_window()

        #create a value dictionary with info all components have. to be added to by component type
        self.ValueDict = {"MfNr": StringVar(),
                          "Footprint": StringVar(),
                          "MinMaxTemperature": StringVar(),
                          "Manufacturer": StringVar(),
                          "Note Generic": StringVar(),
                          "Note Quality": StringVar(),
                          "Note Price": StringVar(),
                          "Note Stock": StringVar(),
                          "Datasheet": StringVar()}
