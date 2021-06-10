from tkinter import *
from Subs.Passive_single_window import Passive_single_window
from Subs.db_handler import component_database
from Subs.ValueConvert import ValueConvert
from Subs.OctoPartAPI import OctoPartAPI
import tkinter.messagebox
import pyperclip


class Add_passive_window(Passive_single_window):
    """Base class for the 'add' window for passive components"""

    def __init__(self, db_handler, screensize, window_position, master_window):
        super().__init__(db_handler, screensize, window_position)
        self.master_window = master_window
        self.PassiveType = "ERROR"

    def _create_window(self):
        """Create window function, override of parent
        all functionallity common to add passive component windows go here
        """        
        #first we start by calling parent function
        super()._create_window()

        #return to start of the grid of labels
        self.gridrow = self.list_start_row

        #add two stringvars: footprint_is_new and manufacturer_is_new; for typo prevention 
        self.footprint_is_new = StringVar()
        self.manufacturer_is_new = StringVar()
        
        #and then trace the corresponding dictionary stringvars
        self.ValueDict['Footprint'].trace('w', self._trace_footprint)
        self.ValueDict['Manufacturer'].trace('w', self._trace_manufacturer)        

        #build list of entries (also add labels with the "is new" info)
        #Octopart button next to MfNr
        OctoButton = Button(self.window, text = "Fetch Octopart Info", width = 15, command = lambda: self._button_octopart(self.ValueDict['MfNr'].get()))
        OctoButton.grid(row = self.gridrow, column = 2)
        #MfNr (name this one, so we can set focus on clearing values)
        self.MfNr_entry = Entry(self.window, width = 35, textvariable = self.ValueDict['MfNr'])
        self.MfNr_entry.grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #Value
        Entry(self.window, width = 35, textvariable = self.ValueDict['Value']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #skip one (is ferrite)
        self.gridrow += 1
        #footprint
        Entry(self.window, width = 35, textvariable = self.ValueDict['Footprint']).grid(row = self.gridrow, column = 1)
        Label(self.window, width = 35, textvariable = self.footprint_is_new).grid(row = self.gridrow, column = 2)
        self.gridrow += 1
        #tolerance
        Entry(self.window, width = 35, textvariable = self.ValueDict['Tolerance']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #power rating/max current/max voltage
        Entry(self.window, width = 35, textvariable = self.ValueDict['Power Rating']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #skip one (max dc resistance)
        self.gridrow += 1
        #Material
        Entry(self.window, width = 35, textvariable = self.ValueDict['Material']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #manufacturer
        Entry(self.window, width = 35, textvariable = self.ValueDict['Manufacturer']).grid(row = self.gridrow, column = 1)
        Label(self.window, width = 35, textvariable = self.manufacturer_is_new).grid(row = self.gridrow, column = 2)
        self.gridrow += 1
        #temp coef
        Entry(self.window, width = 35, textvariable = self.ValueDict['Temperature Coef']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #minmax temp
        Entry(self.window, width = 35, textvariable = self.ValueDict['MinMaxTemperature']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #skip one (ESR)
        self.gridrow += 1     
        #datasheet
        Entry(self.window, width = 35, textvariable = self.ValueDict['Datasheet']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note generic
        Entry(self.window, width = 35, textvariable = self.ValueDict['Note Generic']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note qual
        Entry(self.window, width = 35, textvariable = self.ValueDict['Note Quality']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note price
        Entry(self.window, width = 35, textvariable = self.ValueDict['Note Price']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1
        #note stock
        Entry(self.window, width = 35, textvariable = self.ValueDict['Note Stock']).grid(row = self.gridrow, column = 1)
        self.gridrow += 1

        #spacer for looks
        Label(self.window, text = "").grid(row = self.gridrow, column =0)
        self.gridrow += 1
        #add function buttons
        #add
        self.button_add = Button(self.window, width = 20, text = "Add to Database", command = self._button_add)
        self.button_add.grid(row = self.gridrow, column = 0)
        #add_close
        self.button_add_close = Button(self.window, width = 20, text = "Add and Close", command = self._button_add_close)
        self.button_add_close.grid(row = self.gridrow, column = 1)
        #close
        Button(self.window, width = 20, text = "Close", command = self._button_close).grid(row = self.gridrow, column = 2)

        #Bind keyboard presses to functions
        self.window.bind("<Return>", self._button_add)
        self.window.bind("<F1>", self._paste_mfnr)
        self.window.bind("<F2>", self._button_octopart)
        self.window.bind("<F3>", self._button_add)
        self.window.bind("<F4>", self._button_add_close)
        self.window.bind("<F5>", self._button_close)



    def _paste_mfnr(self, event = None):
        paste = pyperclip.paste()
        self.ValueDict['MfNr'].set(paste)

    def _trace_footprint(self, a,b,c):
        """Tracer of the footprint input. Writes if the footprint exists in the database yet. For typo prevention"""
        #get the entered footprint string
        foot = self.ValueDict['Footprint'].get()
        #if it's emtpy set empty and return
        if foot == "":
            self.footprint_is_new.set("")
            return
        #else check the database and set accordingly
        footexists = self.db.check_item_exists_in_table(self.PassiveType, "Footprint", foot)
        if footexists == 0:
            self.footprint_is_new.set("Footprint is new in "+ self.PassiveType +" db")
        else:
            self.footprint_is_new.set("Footprint exists in "+ self.PassiveType +" db")

    def _trace_manufacturer(self, a,b,c):
        """Tracer of the manufacturer input. Writes if the manufacturer exists in the database yet. For typo prevention"""
        #get manufacuter entry string
        man = self.ValueDict['Manufacturer'].get()
        #if empty, write empty and return
        if man == "":
            self.manufacturer_is_new.set("")
            return
        #else check the database and write accordingly
        manexists = self.db.check_item_exists_in_table(self.PassiveType, "Manufacturer", man)
        if manexists == 0:
            self.manufacturer_is_new.set("Manufacturer is new in "+ self.PassiveType +" db")
        else:
            self.manufacturer_is_new.set("Manufacturer exists in "+ self.PassiveType +" db")

    

    def _button_add(self, event = None):
        """Add component to the database. Override the _add_specific function in child for type specific actions"""
        #create component object
        component = []

        #instantiate value converter
        convert = ValueConvert()
        #get database storage value and add to the component object
        value = convert.short_to_db(self.PassiveType, self.ValueDict['Value'].get())
        component.append(value)

        #fill the rest of the component
        component.append(self.ValueDict['Footprint'].get())
        component.append(self.ValueDict['Tolerance'].get())
        component.append(self.ValueDict['Power Rating'].get())
        component.append(self.ValueDict['Material'].get())
        component.append(self.ValueDict['Manufacturer'].get())
        component.append(self.ValueDict['MfNr'].get())
        component.append(self.ValueDict['Temperature Coef'].get())
        component.append(self.ValueDict['MinMaxTemperature'].get())
        component.append(self.ValueDict['Datasheet'].get())
        component.append(self.ValueDict['Note Generic'].get())
        component.append(self.ValueDict['Note Quality'].get())
        component.append(self.ValueDict['Note Price'].get())
        component.append(self.ValueDict['Note Stock'].get())
        

        #call function from child, to add specific functionality
        self._add_specific()

        #debug delete
        print(component)

        #check if the data meets the minimum required entries
        if component[0] == "ERROR" or component[1] == "" or component[6] == "":
            tkinter.messagebox.showerror("Error with data", "Incomplete or incorrect data. MfNr, Value and Footprint are the minimum required data")
            return

        #if the minimum is met, add to database
        self.db.add_to_table(self.PassiveType, component)


        self._clean_entries()
        self.master_window._populate_component_list()

    def _add_specific(self):
        "Override in child"
        pass

    def _button_add_close(self, event = None):
        """First add, then close"""
        self._button_add()
        self._hide()

    def _button_close(self, event = None):
        """Clear entries, then hide window"""
        self._clean_entries()
        self._hide()

    def _clean_entries(self):
        """Clears all the stringvars of the valuedict, and sets focus to the first entry field"""
        for key in self.ValueDict:
            self.ValueDict[key].set("")
        self.MfNr_entry.focus_set()

    def _button_octopart(self, event = None):
        """Function to override, result of octopart button click"""        
        #get mfnr
        MfNr = self.ValueDict['MfNr'].get()
        print(MfNr)
        #if the button is pressed with an empty mfnr, do nothing
        if MfNr == "":
            return
        #TODO prevent multiple token usages, maybe?
        #start the api, and get the data matching the mfnr
        api = OctoPartAPI()
        octoData = api.search_by_mfnr(MfNr)
        print(octoData)
        #check if the right value is returned (Resistance, Capacitance, etc.) else pop up an error, and do not fill
        if self.Value_Name in octoData:
            self.ValueDict['Value'].set(octoData[self.Value_Name])
        else:
            errormessage = "MfNr returned data which did not match expectations. No " + self.Value_Name + " found in data."
            tkinter.messagebox.showerror("Error with MfNr", errormessage)
            return
        #fill in the rest
        if 'Case/Package' in octoData:
            self.ValueDict['Footprint'].set(octoData['Case/Package'])

        if 'Tolerance' in octoData:
            self.ValueDict['Tolerance'].set(octoData['Tolerance'])

        if self.Power_Rating_name in octoData:
            self.ValueDict['Power Rating'].set(octoData[self.Power_Rating_name])

        if self.Material_Name in octoData:
            self.ValueDict['Material'].set(octoData[self.Material_Name])

        if 'Manufacturer' in octoData:
            self.ValueDict['Manufacturer'].set(octoData['Manufacturer'])

        if 'Temperature Coefficient' in octoData:
            self.ValueDict['Temperature Coef'].set(octoData['Temperature Coefficient'])

        minmaxtemp = ""
        if 'Min Operating Temperature' in octoData:
            minmaxtemp = octoData['Min Operating Temperature'] + " - "
        if 'Max Operating Temperature' in octoData:
            minmaxtemp += octoData['Max Operating Temperature']
        if minmaxtemp != "":
            self.ValueDict['MinMaxTemperature'].set(minmaxtemp)
        
        if 'Datasheet' in octoData:
            self.ValueDict['Datasheet'].set(octoData['Datasheet'])

               
        #Finish the rest in component specific subclasses
