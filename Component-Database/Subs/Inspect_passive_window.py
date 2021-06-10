from tkinter import *
from Subs.Passive_single_window import Passive_single_window
from Subs.db_handler import component_database
from Subs.ValueConvert import ValueConvert
import tkinter.messagebox


class Inspect_passive_window(Passive_single_window):
    """base Window for the 'inspect' type of window for passive components, child of passive single window"""

    def __init__(self, db_handler, screensize, window_position, master):
        super().__init__(db_handler, screensize, window_position)
        self.master = master

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to inspect passive component windows go here
        """        
        #first we start by calling parent function
        super()._create_window()

        #return to start of the grid of labels
        self.gridrow = self.list_start_row

        #build label list with the values
        #MfNr
        Label(self.window, textvariable = self.ValueDict['MfNr'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #Value
        Label(self.window, textvariable = self.ValueDict['Value'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #space for is ferrite
        self.gridrow += 1
        #footprint
        Label(self.window, textvariable = self.ValueDict['Footprint'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #tolerance
        Label(self.window, textvariable = self.ValueDict['Tolerance'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #power rating
        Label(self.window, textvariable = self.ValueDict['Power Rating'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #space for max dc resistance
        self.gridrow += 1
        #material
        Label(self.window, textvariable = self.ValueDict['Material'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #manufacturer
        Label(self.window, textvariable = self.ValueDict['Manufacturer'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #temp coef
        Label(self.window, textvariable = self.ValueDict['Temperature Coef'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #minmaxtemp
        Label(self.window, textvariable = self.ValueDict['MinMaxTemperature'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #space for ESR
        self.gridrow += 1      
        #Datasheet TODO make it a button
        Label(self.window, textvariable = self.ValueDict['Datasheet'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note generic
        Label(self.window, textvariable = self.ValueDict['Note Generic'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note qual
        Label(self.window, textvariable = self.ValueDict['Note Quality'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note price
        Label(self.window, textvariable = self.ValueDict['Note Price'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note stock
        Label(self.window, textvariable = self.ValueDict['Note Stock'], width = 25, anchor = 'w').grid(row = self.gridrow, column = 1)
        self.gridrow += 1

        #close button
        Button(self.window, text= "Close", command = self._hide).grid(row = self.gridrow, column = 0)

        #edit button
        Button(self.window, text = "Edit", command = self._edit_entry).grid(row= self.gridrow, column =1)

        #bind keys
        self.window.bind("<Return>", self._hide)
        self.window.bind("<F3>", self._hide)

    def _fill_data(self, row):
        """Fill the value dict with data from the database row
        :param row: database row with all the data from one row
        """
        #get the converter for value
        convert = ValueConvert()
        value, verbose = convert.db_to_readable(self.PassiveType, row[0])
        self.ValueDict['Value'].set(value)
        #just fill the rest
        self.ValueDict['Footprint'].set(row[1])
        self.ValueDict['Tolerance'].set(row[2])
        self.ValueDict['Power Rating'].set(row[3])
        self.ValueDict['Material'].set(row[4])
        self.ValueDict['Manufacturer'].set(row[5])
        self.ValueDict['MfNr'].set(row[6])
        self.ValueDict['Temperature Coef'].set(row[7])
        self.ValueDict['MinMaxTemperature'].set(row[8])
        self.ValueDict['Datasheet'].set(row[9])
        self.ValueDict['Note Generic'].set(row[10])
        self.ValueDict['Note Quality'].set(row[11])
        self.ValueDict['Note Price'].set(row[12])
        self.ValueDict['Note Stock'].set(row[13])
        

    def display(self, row):
        super().display()
        self._fill_data(row)
        self.row = row

    def _edit_entry(self):
        self.master._open_edit_window(self.row)
        self._hide()