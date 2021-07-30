from tkinter import *
from Subs.Subwindow import Subwindow
from Subs.ValueConvert import ValueConvert
from icecream import ic

class component_category(Subwindow):
    """Base class for all component category windows, child of subwindow"""

    def __init__(self, db_handler, screensize, window_position):
        """:param db_handler: the datebase handler object
        :param window_position: tuple with position information of the window [x_offset, y_offset]
        :param screensize: tuple with screensize in pixels
        """
        self.screensize = screensize
        x = int(screensize[0]*0.5)
        y = int(screensize[1]*0.5) 
        geometry = [x,y,window_position[0], window_position[1]]
        super().__init__(db_handler, geometry)
        self.Component_type = "ERROR"
        self.Power_Rating_name = "ERROR"
        self.add_window = None
        self.inspect_window = None
        self.edit_window = None       

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to component categotry windows go here
        """        
        #first we start by calling parent function
        super()._create_window()
        #then we finish the construction

        #place the add new component button
        self.button_add_new_component = Button(self.window, text = "Add new", width = 25, height = 5, command = self.add_window.display)
        self.button_add_new_component.grid(row = self.gridrow, column = 0, rowspan = 2)

        #place spacer for looks
        Label(self.window, text= "", width = 50).grid(row = self.gridrow, column = 1)

        #setup viewstype and place radiobuttons
        self.viewStyle = StringVar()
        self.viewStyle.set("Full")
        self.radio_view_simple = Radiobutton(self.window, text = "Simple list view", variable = self.viewStyle, value = "Simple", command = self._populate_component_list)
        self.radio_view_full   = Radiobutton(self.window, text = "Full list view", variable = self.viewStyle, value = "Full", command = self._populate_component_list)
        self.radio_view_simple.grid(row = self.gridrow, column = 2, sticky = W, columnspan = 6)
        self.radio_view_full.grid(row = self.gridrow +1, column = 2, sticky = W, columnspan = 6)
        #add spacer 
        Label(self.window, text= "", width = 50).grid(row = self.gridrow +2, column = 0)
        #set gridrow to past the radiobuttons and spacer
        self.gridrow += 3

        #create frame for the component list
        self.list_frame = Frame(self.window)
        self.list_frame.grid(row =self.gridrow, column = 0, columnspan = 6)

        #create itemlist for the components (so we can destroy widgets when we refresh the screen)
        self.component_item_list = []

        #call populate component list function
        self._populate_component_list()
        

    def _button_component_value(self, value):
        ic()
        

    def _populate_component_list(self):
        """Function to populate the component list"""

        #first, clear the old list of display widgets
        for item in self.component_item_list:
            item.destroy()
        self.component_item_list.clear()
        
        #fetch all components
        rows = self.db.fetch_all_components_type(self.Component_type, "Value", True)

        #Debug
        ic(rows)

        #the simple list viewstyle:
        if self.viewStyle.get() == "Simple":
            #set starting values for some variables
            lastvalue = ""
            duplicates = 0
            framerow = 0

            #place spacers for looks
            self.component_item_list.append(Label(self.list_frame, text = "", width = 20))
            self.component_item_list[-1].grid(row = framerow, column = 0)
            self.component_item_list.append(Label(self.list_frame, text = "", width = 15))
            self.component_item_list[-1].grid(row = framerow, column = 1)
            self.component_item_list.append(Label(self.list_frame, text = "", width = 50))
            self.component_item_list[-1].grid(row = framerow, column = 2)

            #step through the components from the db, and create listing
            convert = ValueConvert()            
            for row in rows:
                #get value
                short, verbose = convert.db_to_readable(self.Component_type, row[0])
                #if the value is not the same as last time, create an entry
                if row[0] != lastvalue:
                    #this is a new value, so first we start with listing how many entries the last value had (if any)
                    if duplicates != 0:
                        duptext = str(duplicates) + " Type"
                        if duplicates >1:
                            duptext += "s"
                        self.component_item_list.append(Label(self.list_frame, text = duptext, width = 15))
                        self.component_item_list[-1].grid(row = framerow, column = 1)
                        framerow +=1
                    #this is the first of the value, so duplicates =1
                    duplicates = 1
                    #remember value for next row comparisson
                    lastvalue = row[0]
                    #add component value button
                    self.component_item_list.append(Button(self.list_frame, text = short, width = 15, command = lambda value = row[0]: self._button_component_value(value)))
                    self.component_item_list[-1].grid(row = framerow, column = 0)

                else:
                    #if this is not a new value, add 1 to duplicates
                    duplicates +=1

            #after the loop, we also list how many entries the last value had, if any.
            if duplicates != 0:
                duptext = str(duplicates) + " Type"
                if duplicates >1:
                    duptext += "s"
                self.component_item_list.append(Label(self.list_frame, text = duptext, width = 15))
                self.component_item_list[-1].grid(row = framerow, column = 1)

        else:
            #if the viewstyle is not simple, call child function to do the population
            self._populate_component_list_full(rows)

    def _populate_component_list_full(self):
        """Function for polulating the more complex full component list, to be overridden"""
        print("Override failure _populate_component_list_full(component_category)")        
