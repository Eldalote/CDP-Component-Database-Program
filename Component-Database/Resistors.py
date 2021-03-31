from tkinter import * 
import tkinter.messagebox
import db_handler

class resistor_window:
    def __init__(self, screensize, db):
        self.screensize = screensize
        self.db = db       
        self.display_item_list = []

    def display_main(self):
        """Displays the window. Unhides it if it already exits, creates it if not."""
        try:
            self.res_main.deiconify()
        except:
            self.create_window_main()
        self.res_main.focus_set()


    def create_window_main(self):
        """Create the main resistor window."""

        #Define the size of the window
        x = int(self.screensize[0]*0.3)
        y = int(self.screensize[1]*0.4)
        xoff = int(self.screensize[0]*0.35)
        yoff = int(self.screensize[1]*0.3)
        geometry = f'{x}x{y}+{xoff}+{yoff}'
        
        #Create window
        self.res_main = Toplevel()
        self.res_main.geometry(geometry)

        #set viewstyle
        self.main_viewstyle = StringVar()
        self.main_viewstyle.set("Simple")

        #Add new resitor button
        self.button_main_add_new = Button(self.res_main, text="Add new resistor", padx=10, pady= 25, command= self.display_add_new)
        self.button_main_add_new.grid(row =0, column = 0, rowspan= 2)

        #Grid spacer
        labelspacer = Label(self.res_main, text="", width =50).grid(row=0, column =1)

        #View type selection radiobuttons
        self.radio_main_view_simple = Radiobutton(self.res_main, text="Simple list view", variable=self.main_viewstyle, value="Simple")
        self.radio_main_view_full = Radiobutton(self.res_main, text="Full list view", variable=self.main_viewstyle, value="Full")
        self.radio_main_view_simple.grid(row=0, column = 2, sticky = W)
        self.radio_main_view_full.grid(row=1, column = 2, sticky = W)

        #Labelframe for listing the resistors
        self.list_frame = LabelFrame(self.res_main, text="Resistors", padx = 10, pady =10)
        self.list_frame.grid(row=2, column = 0, columnspan = 3)

        #Populate the list
        self.populate_resistor_list()


        



    def display_add_new(self):
        return False

    def populate_resistor_list(self):
        """Display the list of resistors Depending on the viewtype"""

        #Clear the list
        self.display_item_list.clear()
        #fetch all the resistors from the db
        rows = db.fetch_all_resistors()
        lastvalue = 0.0
        if self.main_viewstyle == "Simple":
            for row in rows:
                if row[1] != lastvalue:
                    lastvalue = row[1]
                    shortvalue = 
                    self.display_item_list.append(Button(self.res_main, text = shortvalue))

        else:
            return False




