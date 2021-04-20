from tkinter import *
from Subs.passive_components import passive_components
from Subs.db_handler import component_database
from Subs.Value_conversion import ValueConvert
from Subs.Resistor_singles_windows import *

class Resistor_window(passive_components):
    """Class for the resistors window"""

    def __init__(self, db_handler, screensize, window_position):
        super().__init__(db_handler, screensize, window_position)
        self.add_window = Add_resistor_window(self.db, self.screensize, (100, 100), self)
        self.inspect_window = Inspect_resistor_window(self.db, self.screensize, (100, 100), self)
        self.edit_window = Edit_resistor_window(self.db, self.screensize, (100, 100), self)
        self.db.create_table_if_new("Resistor")


    def _get_power_table_discriptor(self):
        """Just return 'Power Rating'"""
        return "Power Rating"

    def _fetch_all_components(self):
        """Return the function to fetch all resistors"""
        return self.db.fetch_all_components_type("Resistor", "value", True)

    def _get_value(self, db_row):
        """Function to get the value and display value for the given row
        :param db_row: database row to get value from
        :return: tuple with [database value, short representation value, verbose value]
        """
        
        #initiate value converter
        convert = ValueConvert()
        db_value = db_row[0]
        #convert the value
        convvalue = convert.real_to_short("Resistor", db_value)
        return (db_value, convvalue[0], convvalue[1])

    def _button_add_new_component(self):
        self.add_window.display()

    def _button_component_specific(self, row):
        self.inspect_window.display(row)

    def _open_edit_window(self, row):
        self.edit_window.display(row)