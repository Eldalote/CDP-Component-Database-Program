from tkinter import *
from Subs.component_category import component_category
from Subs.ValueConvert import ValueConvert
from icecream import ic


class Short_list_window(component_category):
    """Base class for all "short list" classes. Build on the component_category class (or more acurately, takes away from)"""

    def __init__(self, db_handler, screensize, window_position):
        super().__init__(db_handler, screensize, window_position)

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to component categotry windows go here
        """        
        #first we start by calling parent function
        super()._create_window()
        #then we finish the construction

        #We dont need the simple or full list radio buttons
        self.radio_view_full.destroy()
        self.radio_view_simple.destroy()

    def _populate_component_list(self):
        """We overide this function, because we dont actually want to populate the list in this step."""
        pass

    def _populate_short(self, Value):
        """Function to populate the window from the short list"""
        
        #to start, clear the old list of display widgets
        for item in self.component_item_list:
            item.destroy()
        self.component_item_list.clear()

        #fetch all components
        rows = self.db.fetch_component_by_value(self.Component_type, "Value", Value)

        #Debug
        ic(rows)

        #then use the normal function to populate
        self._populate_component_list_full(rows)

    def display(self, Value):
        super().display()
        self._populate_short(Value)

   
