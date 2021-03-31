from tkinter import * 
import tkinter.messagebox
import sqlite3
from sqlite3 import Error
import db_handler
import Resistors


def get_screen_size():
    """
    Hack to get the resolution of the active monitor
    :return: x, y, tuple with resolution in pixels.
    """
    test = Tk()
    test.update_idletasks()
    test.attributes('-fullscreen', True)
    test.state('iconic')
    x = test.winfo_width()
    y = test.winfo_height()    
    test.destroy()
    return x, y

def main():
    #Get screen resolution of the active monitor
    screensize = get_screen_size()

    #create database object
    db = db_handler.component_database(r"db/components.db")

    #create the resistor window object
    resistor_window = Resistors.resistor_window(screensize, db)

    #build the main window
    mainWindow = Tk()
    mainWindow.geometry(f'{300}x{300}+{int(screensize[0]*0.4)}+{int(screensize[1]*0.4)}')

    #add the Resistor button
    resistor_button = Button(mainWindow, text= "Resistors", command=resistor_window.display_main)
    resistor_button.grid(row=0, column=0)

    #main windown main loop
    mainWindow.mainloop()

    #Stuff to do when closing program
    #close db connection
    db.close()


if __name__ == "__main__":
    main()
