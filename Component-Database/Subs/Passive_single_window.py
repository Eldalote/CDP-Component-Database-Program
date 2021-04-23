from tkinter import *
from Subs.Component_single_window import Component_single_window
from Subs.ValueConvert import ValueConvert

class Passive_single_window(Component_single_window):
    """Base class for the single component windows for the passive components"""

    def __init__(self, db_handler, screensize, window_position):
        super().__init__(db_handler, screensize, window_position)
        self.PassiveType = "ERROR"
        self.Power_Rating_name = "ERROR"

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to single passive component windows go here
        """        
        #first we start by calling parent function
        super()._create_window()

        #update valuedictionary with values common to passive components
        self.ValueDict.update({"Value": StringVar(),
                               "Tolerance": StringVar(),
                               "Power Rating": StringVar(),
                               "Material": StringVar(),
                               "Temperature Coef": StringVar()})

        #add stringvar for verbose value representation
        self.ValueVerbose = StringVar()
        #and trace the corresponding value
        self.ValueDict['Value'].trace('w', self._trace_verbose_value)

        #store gridrow position for use by children
        self.list_start_row = self.gridrow
        #Start building the window layout        
        #Labels for the values
        #Mfnf
        Label(self.window, text = "Manufacturer Part Number", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #Value
        Label(self.window, text = "Value (short notation)", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        Label(self.window, width = 35, textvariable = self.ValueVerbose).grid(row = self.gridrow, column = 2)
        self.gridrow += 1
        #is ferrite label
        self.is_ferrite_row = self.gridrow
        self.gridrow += 1
        #Footprint
        Label(self.window, text = "Footprint", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #Tolerance
        Label(self.window, text = "Tolerance", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #powerlabel
        Label(self.window, text = self.Power_Rating_name, width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #max dc resistant label
        self.max_dc_row = self.gridrow
        self.gridrow += 1
        #Material
        Label(self.window, text = "Material", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #Manufacturer
        Label(self.window, text = "Manufacturer", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #Temp coef
        Label(self.window, text = "Temperature coefficient", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #ESR label
        self.ESR_row = self.gridrow
        self.gridrow += 1
        #Kicad foot
        Label(self.window, text = "KiCad Footprint", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #note generic
        Label(self.window, text = "Generic Note", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #note qual
        Label(self.window, text = "Quality Note", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #note price
        Label(self.window, text = "Price Note", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1
        #note stock
        Label(self.window, text = "Note Own Stock", width = 25, anchor = 'w').grid(row = self.gridrow, column = 0)
        self.gridrow += 1


    def _trace_verbose_value(self, a,b,c):
        """Tracer for the value entry, writes the verbose presentation of the value, for typo prevention"""
        #get the value string
        value = self.ValueDict['Value'].get()
        #instantiate value converter
        convert = ValueConvert()
        #convert with correct type
        verbose = convert.short_to_verbose(self.PassiveType, value)
        self.ValueVerbose.set(verbose)