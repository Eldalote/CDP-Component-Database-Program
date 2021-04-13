from tkinter import * 
import tkinter.messagebox
import sqlite3
from sqlite3 import Error

class component_database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = self.open_connection()

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
                    MfNr text,
                    value text,                                    
                    footprint text,
                    tolerance text,                                                                       
                    power_rating text,
                    manufacturer text,
                    composition text,
                    temperature_coef text,
                    note_generic text,
                    note_quality text,
                    note_price text,
                    note_own_stock
                    );"""
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            tkinter.messagebox.showerror("Database table error", "Error message: " + str(e))


    def add_resistor(self, resistor):
        """Add new resistor entry to resistor table.
        :param resistor: object with resistor data; MfNr, value, footprint, tolerance, power_rating, manufacturer, composition, temperature_coef, note_generic, note_quality, note price, note_own_stock
        :return: last row id
        """
        sql = """INSERT INTO resistors(
                    MfNr,
                    value,
                    footprint,
                    tolerance,
                    power_rating,
                    manufacturer,
                    composition,
                    temperature_coef,
                    note_generic,
                    note_quality,
                    note_price,
                    note_own_stock)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
        c = self.conn.cursor()
        c.execute(sql, resistor)
        self.conn.commit()
        return c.lastrowid

    def fetch_all_resistors(self, sortcolumn, asc):
        """Fetch all resistors in the table, sorted by sortcolumn, always secondarily sorted by footprint
        :param asc: sort by ascending (true) or descending(false)
        :return: list of rows
        """
        c = self.conn.cursor()
        if asc == True:
            sql = "SELECT * FROM resistors ORDER BY "+str(sortcolumn)+" ASC, footprint DESC;"
        else:
            sql = "SELECT * FROM resistors ORDER BY "+str(sortcolumn)+" DESC, footprint DESC;"
        c.execute(sql)
        rows = c.fetchall()
        return rows

    def fetch_resistors_by_value(self, value):
        """Fetch all resistors with matching value
        :param value: The resistor value to search by.
        :return: rows, a list of rows with matching value.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM resistors WHERE value = ?",(value,))
        rows = c.fetchall()
        return rows

    def check_footprint_exists_resistor(self, footprint):
        """Checks whether the footprint is already present in database. Can be used to prevent typos
        :param footprint: The footprint to be checked for
        :return: 0 or 1
        """
        c = self.conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM resistors WHERE footprint = ? LIMIT 1)",(footprint,))
        return c.fetchall()[0][0]

    def check_manufacturer_exists_resistor(self, manufacturer):
        """Checks whether the manufacturer is already present in database. Can be used to prevent typos
        :param footprint: The manufacturer to be checked for
        :return: 0 or 1
        """
        c = self.conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM resistors WHERE manufacturer = ? LIMIT 1)",(manufacturer,))
        return c.fetchall()[0][0]
