from tkinter import *
from Subs.passive_components import passive_components
from Subs.db_handler import component_database
from Subs.Short_list_passives import Short_list_passives
from Subs.ValueConvert import ValueConvert
from Subs.Resistor_singles_windows import *

class Resistor_window(passive_components):
    """Class for the resistors window"""

    def __init__(self, db_handler, screensize, window_position):        
        super().__init__(db_handler, screensize, window_position)
        self.add_window = Add_resistor_window(self.db, self.screensize, (100, 100), self)
        self.inspect_window = Inspect_resistor_window(self.db, self.screensize, (100, 100), self)
        self.edit_window = Edit_resistor_window(self.db, self.screensize, (100, 100), self)
        self.short_window = Resistor_window_short(self.db, self.screensize,(100, 100))
        self.Component_type = "Resistor"
        self.db.create_table_if_new("Resistor")
        self.Power_Rating_name = "Power Rating"

    def _button_component_value(self, value):
        self.short_window.display(value)


class Resistor_window_short(Short_list_passives):
    """Class for the resistors window"""

    def __init__(self, db_handler, screensize, window_position):        
        super().__init__(db_handler, screensize, window_position)
        self.add_window = Add_resistor_window(self.db, self.screensize, (100, 100), self)
        self.inspect_window = Inspect_resistor_window(self.db, self.screensize, (100, 100), self)
        self.edit_window = Edit_resistor_window(self.db, self.screensize, (100, 100), self)
        self.Component_type = "Resistor"        
        self.Power_Rating_name = "Power Rating"