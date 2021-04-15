from tkinter import *
from Subs.Passive_single_window import Passive_single_window

class Add_passive_window(Passive_single_window):
    """Base class for the 'add' window for passive components"""

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to add passive component windows go here
        """        
        #first we start by calling parent function
        super()._create_window()

        #return to start of the grid of labels
        self.gridrow = self.list_start_row

        #add two stringvars: footprint_is_new and manufacturer_is_new; for typo prevention.
        self.footprint_is_new = StringVar()
        self.manufacturer_is_new = StringVar()
        #and then trace the corresponding dictionary stringvars
        self.ValueDict['Footprint'].trace('w', self._trace_footprint)
        self.ValueDict['Manufacturer'].trace('w', self._trace_manufacturer)

        #build list of entries (also add labels with the "is new" info)


    def _trace_footprint(self, a,b,c):
        pass

    def _trace_manufacturer(self, a,b,c):
        pass
