from tkinter import * 
import tkinter.messagebox
import sqlite3
from sqlite3 import Error



def create_db_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        tkinter.messagebox.showerror("Database connection error", "Error message: " + str(e))    

    return conn
        
def sql_execute(conn, sql_command):
    """Execute sql commands from sql_command 
    :param conn: Connection object
    :param sql_command: an SQL statement
    :return:
    """ 
    try:
        c = conn.cursor()
        c.execute(sql_command)
    except Error as e:
        tkinter.messagebox.showerror("Database table error", "Error message: " + str(e))
    
sql_create_table_resistors = """ CREATE TABLE IF NOT EXISTS resistors (                                    
                                    name text,
                                    value integer,                                    
                                    footprint text,
                                    tollerance text,
                                    MfNr text,                                   
                                    power_rating text                                    
                             );"""

def add_resistor(conn, resistor):
    """
    Add a new resistor to the resistor table
    :param conn: database connection object
    :param resistor: object with resistor data
    :return: resistor id  
    """
    sql = ''' INSERT INTO resistors(
                name,
                value,
                footprint,
                tollerance,
                MfNr,
                power_rating)
                VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, resistor)
    conn.commit()
    return cur.lastrowid

def print_all_resistors(conn):
    """ 
    Print all resistors, sorted by value
    :param conn: database connection object
    :return: 
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM resistors ORDER BY value ASC")
    rows = cur.fetchall()

    for row in rows:
        print(row)

def show_all_resistors(conn, frame, itemlist):
    cur = conn.cursor()
    cur.execute("SELECT * FROM resistors ORDER BY value ASC")
    rows = cur.fetchall()
    i= 0
    itemlist.clear()
    for row in rows:
        
        itemlist.append(Button(frame, text= row[0], pady= 4, command=lambda value=row[1]: resistor_click(conn,value)).grid(row= i, column= 0))
        itemlist.append(Label(frame, text=row[2], pady= 4).grid(row = i, column =1))
        itemlist.append(Label(frame, text=row[3], pady= 4).grid(row = i, column =2))
        itemlist.append(Label(frame, text=row[5], pady= 4).grid(row = i, column =3))
        itemlist.append(Label(frame, text=row[4], pady= 4).grid(row = i, column =4))

        #namebut = Button(frame, text= row[0], pady= 4, command=lambda: resistor_click(conn, row[1]))
        #footlabel = Label(frame, text=row[2], pady= 4)
        #tolllabel = Label(frame, text=row[3], pady= 4)
        #powerlabel = Label(frame, text=row[5], pady= 4)
        #mflabel = Label(frame, text=row[4], pady= 4)
        #namebut.grid(row = i, column = 0)
        #footlabel.grid(row = i, column =1)
        #tolllabel.grid(row = i, column =2)
        #powerlabel.grid(row = i, column =3)
        #mflabel.grid(row = i, column =4)
        i= i+1


def resistor_click(conn, value):
    cur = conn.cursor()
    cur.execute("SELECT * FROM resistors WHERE value = ?", (value,))
    rows = cur.fetchall()
    for row in rows:
        tkinter.messagebox.showinfo("You clicked on a resistor!","The resistor you clicked was: " + row[0])


def create_input():
    top = Toplevel()
    donebut = Button(top, text = "done")
    donebut.pack()

def get_window_size():
    test = Tk()
    test.update_idletasks()
    test.attributes('-fullscreen', True)
    test.state('iconic')
    x = test.winfo_width()
    y = test.winfo_height()    
    test.destroy()
    return x, y




class resistor_input:
    def __init__(self, conn, screensize):
        self.conn = conn
        self.screensize = screensize
    

    def display(self):
        try:
           self.top.deiconify()
        except:
            self.create_window()
        self.top.focus_set()

    def create_window(self):
        self.top = Toplevel()
        x = int(self.screensize[0]*0.3)
        y = int(self.screensize[1]*0.4)
        xoff = int(self.screensize[0]*0.35)
        yoff = int(self.screensize[1]*0.3)
        geom = f'{x}x{y}+{xoff}+{yoff}'
        self.top.geometry(geom)
        self.donebutton = Button(self.top, text = "done", command = self.hide).pack()

    def hide(self):
        self.top.withdraw()

    






db_conn = create_db_connection(r"db/components.db")
if db_conn is not None:
    sql_execute(db_conn, sql_create_table_resistors)

else:
    tkinter.messagebox.showerror("Database error", "Some kind of error ")

#resistor_1 = ('10k', 10000, '0402', '1%', 'RC0402FR-074K7L', '1/16')
#resistor_2 = ('1M',1000000,'0805','0.5%','P3.3KBNCT-ND','1/8')

#add_resistor(db_conn, resistor_1)
#add_resistor(db_conn, resistor_2)

#print_all_resistors(db_conn)
screensize = get_window_size()

print(screensize)

firstWindow = Tk()
firstWindow.minsize(width=int(screensize[0]*0.3), height=int(screensize[1]*0.7))
firstWindow.geometry(f'+{int(screensize[0]*0.35)}+{int(screensize[1]*0.15)}')

input = resistor_input(db_conn, screensize)

resistorFrame = LabelFrame(firstWindow, text= "Resistors", padx=10, pady=10)
resistorFrame.grid(row=1, column=0, columnspan= 2)
addresistorbutton = Button(firstWindow, text = "Add a resistor to database", command = input.display)
addresistorbutton.grid(row = 0, column = 0)
show_resistors_button = Button(firstWindow, text = "Show the resistors!", command= lambda: show_all_resistors(db_conn, resistorFrame, itemlist))
show_resistors_button.grid(row = 0, column = 1)

itemlist = []
clicklist= []


#show_all_resistors(db_conn, resistorFrame, itemlist, clicklist)




firstWindow.mainloop()
db_conn.commit()
db_conn.close()


