from tkinter import *
from Subs.Add_passive_window import Add_passive_window
from Subs.Inspect_passive_window import Inspect_passive_window
from Subs.Edit_passive_window import Edit_passive_window




class Add_resistor_window(Add_passive_window):
    """Window for adding new resistors to the database. Most basic component, very little to add or override"""

    def __init__(self, db_handler, screensize, window_position, master_window):
        super().__init__(db_handler, screensize, window_position, master_window)
        self.PassiveType = "Resistor"
        self.Power_Rating_name = "Power Rating"
        self.Value_Name = "Resistance"
        self.Material_Name = "Composition"

    def _button_octopart(self, event=None):
        super()._button_octopart(event=event)

        



class Inspect_resistor_window(Inspect_passive_window):
    
    def __init__(self, db_handler, screensize, window_position, master):
        super().__init__(db_handler, screensize, window_position, master)
        self.PassiveType = "Resistor"
        self.Power_Rating_name = "Power Rating"
        self.Value_Name = "Resistance"
        self.Material_Name = "Composition"



class Edit_resistor_window(Edit_passive_window):

    def __init__(self, db_handler, screensize, window_position, master_window):
        super().__init__(db_handler, screensize, window_position, master_window)
        self.PassiveType = "Resistor"
        self.Power_Rating_name = "Power Rating"
        self.Value_Name = "Resistance"
        self.Material_Name = "Composition"