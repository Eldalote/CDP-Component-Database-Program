from tkinter import *
from Subs.Passive_single_window import Passive_single_window
from Subs.Add_passive_window import Add_passive_window
from Subs.db_handler import component_database
from Subs.ValueConvert import ValueConvert
import tkinter.messagebox

class Edit_passive_window(Add_passive_window):
    """Base class for the 'Edit' window for passive components, builds on the add window"""

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to edit passive component windows go here
        """        
        #first we start by calling parent function
        super()._create_window()

        #first, delete the add button, and add_close button
        self.button_add.destroy()
        self.button_add_close.destroy()

        #add an "Edit" button
        Button(self.window, width = 20, text = "Edit", command = self._button_add).grid(row = self.gridrow, column = 0)

    def _button_add(self, event=None):
        """Override of the add function, does edit instead of add"""
        #create component object
        component = []

        #instantiate value converter
        convert = ValueConvert()
        #get database storage value and add to the component object
        value = convert.short_to_db(self.PassiveType, self.ValueDict['Value'].get())
        component.append(value[0])

        #fill the rest of the component
        component.append(self.ValueDict['Footprint'].get())
        component.append(self.ValueDict['Tolerance'].get())
        component.append(self.ValueDict['Power Rating'].get())
        component.append(self.ValueDict['Material'].get())
        component.append(self.ValueDict['Manufacturer'].get())
        component.append(self.ValueDict['MfNr'].get())
        component.append(self.ValueDict['Temperature Coef'].get())
        component.append(self.ValueDict['Datasheet'].get())
        component.append(self.ValueDict['Note Generic'].get())
        component.append(self.ValueDict['Note Quality'].get())
        component.append(self.ValueDict['Note Price'].get())
        component.append(self.ValueDict['Note Stock'].get())
        component.append(self.ValueDict['KiCad Footprint'].get())

        #call function from child, to add specific functionality
        self._add_specific()

        #debug delete
        print(component)

        #check if the data meets the minimum required entries
        if component[0] == "ERROR" or component[1] == "" or component[6] == "":
            tkinter.messagebox.showerror("Error with data", "Incomplete or incorrect data. MfNr, Value and Footprint are the minimum required data")
            return

        #if the minimum is met, eddit to database
        self.db.edit_entry_in_table(self.PassiveType, self.key, component)


        self._clean_entries()
        self.master_window._populate_component_list()
        self._hide()

    def _button_add_close(self, event=None):
        """Override of the add close function (for keybind reasons) does nothing"""
        pass

    def display(self, row):
        super().display()
        self._fill_data(row)

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
        self.key = row[-1]

        #debug delete
        print(self.key)