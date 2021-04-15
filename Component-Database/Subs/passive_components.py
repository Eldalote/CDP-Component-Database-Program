from tkinter import *
from Subs.component_category import component_category

class passive_components(component_category):
    """Base class for the passive components windows, child of component category
    (passives are resistor, capacitor, inductor)"""

    def __init__(self, db_handler, screensize, window_position):
        super().__init__(db_handler, screensize, window_position)


    def _get_power_table_discriptor(self):
        print("Override failure _get_power_table_discriptor(passive_components)")        

    def _populate_component_list_full(self, rows):
        """Function to populate the component list full list view, override of parent function"""
        
        #first, get table discriptors
        discriptor = self._get_power_table_discriptor()

        #start framerow at 0
        framerow = 0

        #create discription labels
        #value
        self.component_item_list.append(Label(self.list_frame, text = "Value", width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 0)
        #footprint
        self.component_item_list.append(Label(self.list_frame, text = "Footprint", width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 1)
        #Tolerance
        self.component_item_list.append(Label(self.list_frame, text = "Tolerance", width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 2)
        #power rating / max voltage / nominal current
        self.component_item_list.append(Label(self.list_frame, text = discriptor, width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 3)
        #leave room for max dc resistance (inductor only) / temperature coef code (caps)
        self.component_item_list.append(Label(self.list_frame, text = "", width = 0))
        self.component_item_list[-1].grid(row = framerow, column = 4)
        #Material
        self.component_item_list.append(Label(self.list_frame, text = "Material", width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 5)
        #Manufacturer
        self.component_item_list.append(Label(self.list_frame, text = "Manufacturer", width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 6)
        #MfNr
        self.component_item_list.append(Label(self.list_frame, text = "MfNr", width = 15))
        self.component_item_list[-1].grid(row = framerow, column = 7)

        #spacing label for looks
        self.component_item_list.append(Label(self.list_frame, text = "", width = 15))
        self.component_item_list[-1].grid(row = framerow +1, column = 0)
        framerow += 2

        #step through components
        for row in rows:
            #get value representation
            value = self._get_value(row)
            #value button
            self.component_item_list.append(Button(self.list_frame, text = value[1], width =15, command = lambda row = row: self._button_component_specific(row)))
            self.component_item_list[-1].grid(row = framerow, column = 0)
            #footprint label
            self.component_item_list.append(Label(self.list_frame, text = row[1], width = 15))
            self.component_item_list[-1].grid(row = framerow, column = 1)
            #Tolerance label
            self.component_item_list.append(Label(self.list_frame, text = row[2], width = 15))
            self.component_item_list[-1].grid(row = framerow, column = 2)
            #power rating / max voltage / nominal current label
            self.component_item_list.append(Label(self.list_frame, text = row[3], width = 15))
            self.component_item_list[-1].grid(row = framerow, column = 3)
            #room for max dc resistance / or temperature coef code
            self.component_item_list.append(Label(self.list_frame, text = "", width = 0))
            self.component_item_list[-1].grid(row = framerow, column = 4)
            #Material label
            self.component_item_list.append(Label(self.list_frame, text = row[4], width = 15))
            self.component_item_list[-1].grid(row = framerow, column = 5)
            #manufacturer label
            self.component_item_list.append(Label(self.list_frame, text = row[5], width = 15))
            self.component_item_list[-1].grid(row = framerow, column = 6)
            #MfNr button
            self.component_item_list.append(Button(self.list_frame, text = row[6], width =15, command = lambda MfNr = row[6]: self._button_MfNr(MfNr)))
            self.component_item_list[-1].grid(row = framerow, column = 7)
            #increment framerow
            framerow +=1


        
    