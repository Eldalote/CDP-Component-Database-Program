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
                                    id integer PRIMARY KEY,
                                    name text,
                                    value integer,
                                    value_multiplier text,
                                    footprint text,
                                    tollerance text,
                                    power_rating text                                    
                             );"""



firstWindow = Tk()


db_conn = create_db_connection(r"db/components.db")
if db_conn is not None:
    sql_execute(db_conn, sql_create_table_resistors)

else:
    tkinter.messagebox.showerror("Database error", "Some kind of error ")




db_conn.commit()
db_conn.close()
firstWindow.mainloop()


