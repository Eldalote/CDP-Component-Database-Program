from tkinter import *
from Subs.passive_components import passive_components
from Subs.Short_list_window import Short_list_window


class Short_list_passives(passive_components, Short_list_window):
    
    def __init__(self, db_handler, screensize, window_position):
        super().__init__(db_handler, screensize, window_position)
    
    def _create_window(self):
        return Short_list_window._create_window(self)

   
