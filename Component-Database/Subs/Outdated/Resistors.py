"""
Outdated! use Resistor_window.py instead.


"""












from tkinter import * 
import tkinter.messagebox
import Subs.db_handler as db_handler
from Subs.Value_conversion import ValueConvert

class resistor_window:
    def __init__(self, screensize, db):
        self.screensize = screensize
        self.db = db
        self.db.create_resistor_table()

    def display_main(self):
        """Displays the window. Unhides it if it already exits, creates it if not."""
        try:           
            self.res_main.deiconify()
        except:                      
            self.__create_window_main()
        self.res_main.focus_set()

    def __hide_main(self):
        """Hides the window"""
        try:
            self.res_main.withdraw()
        except:
            pass



    def __create_window_main(self):
        """Create the main resistor window."""

        #Define the size of the window
        x = int(self.screensize[0]*0.5)
        y = int(self.screensize[1]*0.5)
        xoff = int(self.screensize[0]*0.25)
        yoff = int(self.screensize[1]*0.25)
        geometry = f'{x}x{y}+{xoff}+{yoff}'
        
        #Create window
        self.res_main = Toplevel()
        self.res_main.geometry(geometry)

        #change 'x' button from close to hide
        self.res_main.protocol("WM_DELETE_WINDOW", self.__hide_main)

        #set viewstyle
        self.main_viewstyle = StringVar()
        self.main_viewstyle.set("Simple")

        #Add new resitor button
        self.button_main_add_new = Button(self.res_main, text="Add new resistor", padx=10, pady= 25, command= self.__display_add_new)
        self.button_main_add_new.grid(row =0, column = 0, rowspan= 2)

        #Grid spacer
        labelspacer = Label(self.res_main, text="", width =50).grid(row=0, column =1)

        #View type selection radiobuttons
        self.radio_main_view_simple = Radiobutton(self.res_main, text="Simple list view", variable=self.main_viewstyle, value="Simple", command = self.__populate_resistor_list)
        self.radio_main_view_full = Radiobutton(self.res_main, text="Full list view", variable=self.main_viewstyle, value="Full", command = self.__populate_resistor_list)
        self.radio_main_view_simple.grid(row=0, column = 2, sticky = W)
        self.radio_main_view_full.grid(row=1, column = 2, sticky = W)

        #Labelframe for listing the resistors
        self.list_frame = LabelFrame(self.res_main, text="Resistors", width= 500, pady =10, labelanchor = 'n')        
        self.list_frame.grid(row=2, column = 0, columnspan = 3)

        #Populate the list
        self.resistor_listing_list = [] #we use a list, so we can clear it when we redraw the list on the screen.
        self.__populate_resistor_list()



    def __populate_resistor_list(self):
        """Display the list of resistors Depending on the viewtype"""   
        #clear the old list of display items
        for item in self.resistor_listing_list:
            item.destroy()
        self.resistor_listing_list.clear()
        #fetch all the resistors from the db
        rows = self.db.fetch_all_resistors("value", True)
        print(rows)
        
        #starting values
        lastvalue = ""
        duplicates = 0
        gridplace = 1
        #instantiate value converter
        converter = ValueConvert()
        #the simple view
        if self.main_viewstyle.get() == "Simple":
            #place spacers in the labelframe for better look
            self.resistor_listing_list.append(Label(self.list_frame, text= "", width = 20))
            self.resistor_listing_list[-1].grid(row = 0, column = 0)
            self.resistor_listing_list.append(Label(self.list_frame, text= "", width = 15))
            self.resistor_listing_list[-1].grid(row = 0, column = 1)
            self.resistor_listing_list.append(Label(self.list_frame, text= "", width = 50))
            self.resistor_listing_list[-1].grid(row = 0, column = 2)
            #step through resistors from the database
            for row in rows:
                #if it is a new value, create an entry
                if row[1] != lastvalue:
                    #but first, list how many entries the last value had (if this isn't the first of the entire list)
                    if duplicates != 0:
                        duptext = str(duplicates) + " Type"
                        if duplicates > 1:
                            duptext += "s"
                        self.resistor_listing_list.append(Label(self.list_frame, text = duptext))
                        self.resistor_listing_list[-1].grid(row = gridplace -1, column = 1)
                    #This is the first of this value
                    duplicates = 1
                    #remember for comparison with next resistor
                    lastvalue = row[1]
                    shortvalue = converter.real_to_short_resistor(row[1])
                    #TODO add function for actually clicking the button
                    self.resistor_listing_list.append(Button(self.list_frame, text = shortvalue[0], width = 15))
                    self.resistor_listing_list[-1].grid(row = gridplace, column = 0)
                    gridplace += 1
                else:
                    #if it is the same value, add one
                    duplicates += 1

            #After the loop, we need to list how many the last type had, if any resistors were in the list
            if duplicates != 0:
                duptext = str(duplicates) + " Type"
                if duplicates > 1:
                    duptext += "s"
                self.resistor_listing_list.append(Label(self.list_frame, text = duptext))
                self.resistor_listing_list[-1].grid(row = gridplace -1, column = 1)
        else:
            #Discription labels
            self.resistor_listing_list.append(Label(self.list_frame, text = "Value", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 0)
            self.resistor_listing_list.append(Label(self.list_frame, text = "Footprint", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 1)
            self.resistor_listing_list.append(Label(self.list_frame, text = "Tolerance", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 2)
            self.resistor_listing_list.append(Label(self.list_frame, text = "Power rating", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 3)
            self.resistor_listing_list.append(Label(self.list_frame, text = "Manufacturer", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 4)
            self.resistor_listing_list.append(Label(self.list_frame, text = "MfNr", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 5)
            gridplace += 1
            #spacing label
            self.resistor_listing_list.append(Label(self.list_frame, text = "", width = 15))
            self.resistor_listing_list[-1].grid(row = gridplace, column = 0)
            gridplace += 1

            #step through the resistors in the database
            for row in rows:
                #get value representation
                shortvalue = converter.real_to_short_resistor(row[1])
                #TODO add function for clicking the button
                #Value button
                self.resistor_listing_list.append(Button(self.list_frame, text = shortvalue[0], width = 15))
                self.resistor_listing_list[-1].grid(row = gridplace, column = 0)
                #footprint label
                self.resistor_listing_list.append(Label(self.list_frame, text = row[2], width = 15))
                self.resistor_listing_list[-1].grid(row = gridplace, column = 1)
                #Tolerance label
                self.resistor_listing_list.append(Label(self.list_frame, text = row[3], width = 15))
                self.resistor_listing_list[-1].grid(row = gridplace, column = 2)
                #power rating label
                self.resistor_listing_list.append(Label(self.list_frame, text = row[4], width = 15))
                self.resistor_listing_list[-1].grid(row = gridplace, column = 3)
                #manufacturer label
                self.resistor_listing_list.append(Label(self.list_frame, text = row[5], width = 20))
                self.resistor_listing_list[-1].grid(row = gridplace, column = 4)
                #MfNr button
                #TODO function for clipboard stuff with this button
                self.resistor_listing_list.append(Button(self.list_frame, text = row[0], width = 25))
                self.resistor_listing_list[-1].grid(row = gridplace, column = 5)
                gridplace += 1


    def __display_add_new(self):
        """Displays the new resistor window. Unhides it if it already exits, creates it if not."""
        try:
            self.res_add_new.deiconify()
        except:
            self.__create_window_add_new()
        self.res_add_new.focus_set()

    def __create_window_add_new(self):
        """Create the add new resistor window."""

        #Define the size of the window
        x = int(self.screensize[0]*0.3)
        y = int(self.screensize[1]*0.3)
        xoff = int(self.screensize[0]*0.33)
        yoff = int(self.screensize[1]*0.33)
        geometry = f'{x}x{y}+{xoff}+{yoff}'
        
        #Create window
        self.res_add_new = Toplevel()
        self.res_add_new.geometry(geometry)

        #change 'x' button function to hide
        self.res_add_new.protocol("WM_DELETE_WINDOW", self.__hide_add_new_window)
       
        #Create entryfield dictionary. We use dictionary so we can easily call back for resistor data, and to autofill from API
        self.EntryDict = {}

        #start building the ui
        #Manufacturers number
        MfNrLabel = Label(self.res_add_new, text = "Manufacturer Part Number", width = 30, anchor = "w")
        MfNrLabel.grid(row = 0, column = 0)
        self.EntryDict['MfNr'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['MfNr'].grid(row = 0, column = 1)
        #TODO actually do the whole API thing
        API_Button = Button(self.res_add_new, text = "Fetch Octopart data")
        API_Button.grid(row = 0, column = 2)

        #Value
        ValueLabel = Label(self.res_add_new, text = "Resistor Value (short notation)", width = 30, anchor = "w")
        ValueLabel.grid(row = 1, column = 0)
        #setup stringvariable for the input, so we can trace it, and update while typing.
        self.ShortValueText = StringVar()
        self.ShortValueText.trace('w', self.__value_entry_tracer)
        self.EntryDict['Value'] = Entry(self.res_add_new, textvariable = self.ShortValueText, width = 35)
        self.EntryDict['Value'].grid(row = 1, column = 1)
        #set the string variable that the verbose represenation gets written to
        self.VerboseValueText = StringVar()        
        VerboseValueLabel = Label(self.res_add_new, textvariable = self.VerboseValueText, width = 25)
        VerboseValueLabel.grid(row = 1, column = 2)

        #footprint
        FootprintLabel = Label(self.res_add_new, text = "Footprint", width = 30, anchor = "w")
        FootprintLabel.grid(row= 2, column =0)
        #setup string variable for input, so we can trace it, to check if footprint is already in the db.
        self.FootprintEntryText = StringVar()
        self.FootprintEntryText.trace('w', self.__footprint_entry_tracer)
        self.EntryDict['Footprint'] = Entry(self.res_add_new, textvariable = self.FootprintEntryText, width = 35)
        self.EntryDict['Footprint'].grid(row = 2, column = 1)
        #Setup stringvar to set the conclusion of whether the footprint is new or not
        self.FootprintNewText = StringVar()
        NewFootprintLabel = Label(self.res_add_new, textvariable = self.FootprintNewText, width = 30)
        NewFootprintLabel.grid(row = 2, column = 2)

        #tolerance
        ToleranceLabel = Label(self.res_add_new, text = "Tolerance", width = 30, anchor = 'w')
        ToleranceLabel.grid(row = 3, column  = 0)
        self.EntryDict['Tolerance'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['Tolerance'].grid(row = 3, column =1)

        #power rating
        PowerRatingLabel = Label(self.res_add_new, text = "Power Rating", width = 30, anchor = 'w')
        PowerRatingLabel.grid(row = 4, column  = 0)
        self.EntryDict['PowerRating'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['PowerRating'].grid(row = 4, column =1)

        #manufacturer
        ManufacturerLabel = Label(self.res_add_new, text = "Manufacturer", width = 30, anchor = 'w')
        ManufacturerLabel.grid(row = 5, column  = 0)
        #setup string variable for input, so we can trace it, to check if manufacturer is already in the db.
        self.ManufacturerEntryText = StringVar()
        self.ManufacturerEntryText.trace('w', self.__manufacturer_entry_tracer)
        self.EntryDict['Manufacturer'] = Entry(self.res_add_new, textvariable = self.ManufacturerEntryText, width = 35)
        self.EntryDict['Manufacturer'].grid(row = 5, column =1)
        #Setup stringvar to set the conclusion of whether the manufacturer is new or not
        self.ManufacturerNewText = StringVar()
        NewManufacturerLabel = Label(self.res_add_new, textvariable = self.ManufacturerNewText, width = 30)
        NewManufacturerLabel.grid(row = 5, column = 2)

        #composition
        CompositionLabel = Label(self.res_add_new, text = "Composition", width = 30, anchor = 'w')
        CompositionLabel.grid(row = 6, column  = 0)
        self.EntryDict['Composition'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['Composition'].grid(row = 6, column =1)

        #Temperature coefficient
        TempcoefLabel = Label(self.res_add_new, text = "Temperature coefficient", width = 30, anchor = 'w')
        TempcoefLabel.grid(row = 7, column  = 0)
        self.EntryDict['TempCoef'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['TempCoef'].grid(row = 7, column =1)

        #generic note
        NoteGenLabel = Label(self.res_add_new, text = "Generic note", width = 30, anchor = 'w')
        NoteGenLabel.grid(row = 8, column  = 0)
        self.EntryDict['Note Generic'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['Note Generic'].grid(row = 8, column =1)
        
        #quality note
        NoteQualLabel = Label(self.res_add_new, text = "Quality note", width = 30, anchor = 'w')
        NoteQualLabel.grid(row = 9, column  = 0)
        self.EntryDict['Note Qual'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['Note Qual'].grid(row = 9, column =1)

        #price note
        NotePriceLabel = Label(self.res_add_new, text = "Price note", width = 30, anchor = 'w')
        NotePriceLabel.grid(row = 10, column  = 0)
        self.EntryDict['Note Price'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['Note Price'].grid(row = 10, column =1)

        #note own stock
        NoteStockLabel = Label(self.res_add_new, text = "Own stock note", width = 30, anchor = 'w')
        NoteStockLabel.grid(row = 11, column  = 0)
        self.EntryDict['Note Stock'] = Entry(self.res_add_new, text = "", width = 35)
        self.EntryDict['Note Stock'].grid(row = 11, column =1)

        #add the buttons
        AddButton = Button(self.res_add_new, text = "Add to DB", command = self.__add_new_button_add)
        AddButton.grid(row = 12, column = 0)
        AddCloseButton = Button(self.res_add_new, text = "Add and close", command = self.__add_new_button_add_close)
        AddCloseButton.grid(row = 12, column = 1)
        CloseButton = Button(self.res_add_new, text = "Close", command = self.__add_new_button_close)
        CloseButton.grid(row = 12, column  =2)

        #Bind keyboard presses to functions
        self.res_add_new.bind("<Return>", self.__add_new_button_add)
        self.res_add_new.bind("<F1>", self.__add_new_button_add)
        self.res_add_new.bind("<F2>", self.__add_new_button_add_close)
        self.res_add_new.bind("<F3>", self.__add_new_button_close)
        

    

    def __add_new_button_add_close(self, event = None):
        self.__add_new_button_add()
        self.__add_new_button_close()

    def __add_new_button_add(self, event = None):
        """Add resistor to db function, by button press or keyboard event"""
        #instantiate value converter
        converter = ValueConvert()
        
        #create resistor object to be filled with data
        resistor = []
        #start filling
        resistor.append(self.EntryDict['MfNr'].get())
        #transform value
        value = converter.short_to_real_resistor(self.EntryDict['Value'].get())
        resistor.append(value[0])

        #fill with the rest
        resistor.append(self.EntryDict['Footprint'].get())
        resistor.append(self.EntryDict['Tolerance'].get())
        resistor.append(self.EntryDict['PowerRating'].get())
        resistor.append(self.EntryDict['Manufacturer'].get())
        resistor.append(self.EntryDict['Composition'].get())
        resistor.append(self.EntryDict['TempCoef'].get())
        resistor.append(self.EntryDict['Note Generic'].get())
        resistor.append(self.EntryDict['Note Qual'].get())
        resistor.append(self.EntryDict['Note Price'].get())
        resistor.append(self.EntryDict['Note Stock'].get())      

        print(resistor)
        #check if the resistor data is enough to be entered into the db. if not, break off here.
        if resistor[0] == "" or resistor[1] == "ERROR" or resistor[2] == "":
            tkinter.messagebox.showerror("Error with data", "Incomplete or incorrect data. MfNr, Value and Footprint are the minimum required data")
            return

        #insert the resistor into the database
        self.db.add_resistor(resistor)

        #clean up the entry fields
        self.EntryDict['MfNr'].delete(0, 'end')
        self.EntryDict['Tolerance'].delete(0, 'end')
        self.EntryDict['PowerRating'].delete(0, 'end')        
        self.EntryDict['Composition'].delete(0, 'end')
        self.EntryDict['TempCoef'].delete(0, 'end')
        self.EntryDict['Note Generic'].delete(0, 'end')
        self.EntryDict['Note Qual'].delete(0, 'end')
        self.EntryDict['Note Price'].delete(0, 'end')
        self.EntryDict['Note Stock'].delete(0, 'end')
        #clear the stringvars
        self.ShortValueText.set("")
        self.FootprintEntryText.set("")
        self.ManufacturerEntryText.set("")
        #set focus to the first entry field
        self.EntryDict['MfNr'].focus_set()

        #call the populate resistor list command, so the new resistor shows up.
        self.__populate_resistor_list()

    def __add_new_button_close(self, event = None):
        """Cleans up the entry fields and hides the window"""
         #clean up the entry fields
        self.EntryDict['MfNr'].delete(0, 'end')
        self.EntryDict['Tolerance'].delete(0, 'end')
        self.EntryDict['PowerRating'].delete(0, 'end')        
        self.EntryDict['Composition'].delete(0, 'end')
        self.EntryDict['TempCoef'].delete(0, 'end')
        self.EntryDict['Note Generic'].delete(0, 'end')
        self.EntryDict['Note Qual'].delete(0, 'end')
        self.EntryDict['Note Price'].delete(0, 'end')
        self.EntryDict['Note Stock'].delete(0, 'end')
        #clear the stringvars
        self.ShortValueText.set("")
        self.FootprintEntryText.set("")
        self.ManufacturerEntryText.set("")
        #set focus to the first entry field
        self.EntryDict['MfNr'].focus_set()   
        #hide the window
        self.__hide_add_new_window()

    def __hide_add_new_window(self):
        try:
            self.res_add_new.withdraw()
        except:
            pass

        
    def __value_entry_tracer(self, a, b, c):   
        """tracer function for the value entrybox"""
        #instantiate value converter
        converter = ValueConvert()
        #get string value of the variable
        strshort = self.ShortValueText.get()        
        #convert it, and set the display variable to the verbose output.
        convertoutput = converter.short_to_real_resistor(strshort)        
        self.VerboseValueText.set(convertoutput[1])

    def __footprint_entry_tracer(self, a,b,c):
        """tracer function for the footprint entrybox"""
        strfootprint = self.FootprintEntryText.get()
        footexists = self.db.check_footprint_exists_resistor(strfootprint)
        if footexists == 0:
            self.FootprintNewText.set("This footprint is new in the DB")
        else:
            self.FootprintNewText.set("Footprint not new in the DB")

    def __manufacturer_entry_tracer(self, a,b,c):
        """tracer function for the manufacturer entrybox"""
        strmanufacturer = self.ManufacturerEntryText.get()
        manexists = self.db.check_manufacturer_exists_resistor(strmanufacturer)
        if manexists == 0:
            self.ManufacturerNewText.set("This Manufacturer is new in the DB")
        else:
            self.ManufacturerNewText.set("Manufacturer not new in the DB")
