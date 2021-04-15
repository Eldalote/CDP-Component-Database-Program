from tkinter import * 
import tkinter.messagebox
import sqlite3
from sqlite3 import Error

class component_database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = self.open_connection()
        self.create_resistor_table()

    def open_connection(self):
        """Create a database connection to a SQLite database        
        :return: conn, database connection object.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            #print(sqlite3.version)
        except Error as e:
            tkinter.messagebox.showerror("Database connection error", "Error message: " + str(e))   
        return conn

    def close(self):
        """Close database connection."""
        self.conn.close()

    def create_resistor_table(self):
        """Create resistor table in database, if it does not already exist."""
        sql = """CREATE TABLE IF NOT EXISTS resistors ( 
                    Value text,
                    Footprint text,                                    
                    Tolerance text,
                    Power_rating text,                                                                       
                    Material text,
                    Manufacturer text,
                    MfNr text,
                    Temperature_coef text,
                    Note_generic text,
                    Note_quality text,
                    Note_price text,
                    Note_own_stock
                    );"""
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            tkinter.messagebox.showerror("Database table error", "Error message: " + str(e))


    def add_resistor(self, resistor):
        """Add new resistor entry to resistor table.
        :param resistor: object with resistor data; value, footprint, tolerance, power_rating, material, manufacturer, MfNr, temperature_coef, note_generic, note_quality, note price, note_own_stock
        :return: last row id
        """
        sql = """INSERT INTO resistors(
                    Value,
                    Footprint,
                    Tolerance,
                    Power_rating,
                    Material,
                    Manufacturer,
                    MfNr,
                    Temperature_coef,
                    Note_generic,
                    Note_quality,
                    Note_price,
                    Note_own_stock)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
        c = self.conn.cursor()
        c.execute(sql, resistor)
        self.conn.commit()
        return c.lastrowid


    def fetch_all_components_type(self, table, sortcolumn, asc):
        """Fetch all components from a table, sorted by sortcolumn, always secondarily sorted by footprint
        :param table: name of the table (ex: 'resistors')
        :param sortcolumn: name of the column to sort by (ex: "value")
        :param asc: sort by ascending (true) or descending(false)
        :return: list of rows
        """
        c = self.conn.cursor()
        if asc == True:
            sql = "SELECT * FROM "+str(table)+" ORDER BY "+str(sortcolumn)+" ASC, footprint ASC;"
        else:
            sql = "SELECT * FROM "+str(table)+" ORDER BY "+str(sortcolumn)+" DESC, footprint ASC;"
        c.execute(sql)
        rows = c.fetchall()
        return rows

    def fetch_component_by_value(self,table, value):
        """Fetch all components in the table with matching value
        :param table: name of the table to search in (ex: 'resistors')
        :param value: The resistor value to search by.
        :return: rows, a list of rows with matching value.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM "+str(table)+" WHERE Value = ?",(value,))
        rows = c.fetchall()
        return rows

    def check_item_exists_in_table(self, table, itemtype, item):
        """Checks whether a specific item is already present in the table. Can be used to prevent typos
        :param table: name of the table to search in (ex: 'resistors')
        :param itemtype: name of the column to search in (ex: Footprints)
        :return: 0 or 1
        """
        c = self.conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM "+str(table)+" WHERE "+str(itemtype)+" = ? LIMIT 1)",(footprint,))
        return c.fetchall()[0][0]

