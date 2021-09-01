from tkinter import * 
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
from icecream import ic

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
        except Error as e:
            tkinter.messagebox.showerror("Database connection error", "Error message: " + str(e))   
        return conn

    def close(self):
        """Close database connection."""
        self.conn.close()

    def add_to_table(self, table, component):
        """generic function to add a component to a table. Redirects to correct function"""
        nextKey = self._get_next_key(table)
        component.append(nextKey)
        if table == "Resistor":
            return self._add_resistor(component)
        else: 
            print("ERROR: Not yet implemented or wrong type")
            return -1

    def create_table_if_new(self, table):
        """Generic function to create a table in the database, if it does not exist yet. Redirects to correct function"""
        if table == "Resistor":
            return self._create_resistor_table()
        else:
            print("ERROR: Not yet implemented, or typo: " + table )


    def edit_entry_in_table(self, table, key, new_entry):
        """Generic function to edit an entry in a table
        effectively deletes the entry, and adds a new one in its place
        :param table: db table this affects
        :param key: key of the entry to "edit" (is deleted)
        :param new_entry: new component object (must be without key)
        """
        self.delete_entry_in_table(table, key)
        self.add_to_table(table, new_entry)


    def delete_entry_in_table(self, table, key):
        """Generic function to delete an entry from a table"""
        c = self.conn.cursor()
        sql = "DELETE FROM " + table + " WHERE Key = ?" 
        c.execute(sql, (key,))
        self.conn.commit()


    def _create_resistor_table(self):
        """Create resistor table in database, if it does not already exist."""
        sql = """CREATE TABLE IF NOT EXISTS Resistor ( 
                    Value text,
                    Footprint text,                                    
                    Tolerance text,
                    Power_rating text,                                                                       
                    Material text,
                    Manufacturer text,
                    MfNr text,
                    Temperature_coef text,
                    MinMaxTemperature text,
                    Datasheet_URL text,
                    Note_generic text,
                    Note_quality text,
                    Note_price text,
                    Note_own_stock text,                    
                    Key integer
                    );"""
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Error as e:
            tkinter.messagebox.showerror("Database table error", "Error message: " + str(e))


    def _add_resistor(self, resistor):
        """Add new resistor entry to resistor table.
        :param resistor: object with resistor data; value, footprint, tolerance, power_rating, material, manufacturer, MfNr, temperature_coef, MinMaxTemperature, datasheet url, note_generic, note_quality, note price, note_own_stock
        :return: last row id
        """
        sql = """INSERT INTO Resistor(
                    Value,
                    Footprint,
                    Tolerance,
                    Power_rating,
                    Material,
                    Manufacturer,
                    MfNr,
                    Temperature_coef,
                    MinMaxTemperature,
                    Datasheet_URL,
                    Note_generic,
                    Note_quality,
                    Note_price,
                    Note_own_stock,                    
                    Key)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        c = self.conn.cursor()
        c.execute(sql, resistor)
        self.conn.commit()
        return c.lastrowid


    def fetch_all_components_type(self, table, sortcolumn, asc):
        """Fetch all components from a table, sorted by sortcolumn, always secondarily sorted by footprint
        :param table: name of the table (ex: 'Resistor')
        :param sortcolumn: name of the column to sort by (ex: "Value")
        :param asc: sort by ascending (true) or descending(false)
        :return: list of rows
        """
        return self.fetch_components_type_multisorted(table, [[sortcolumn, asc],["Footprint",True]])        

    def fetch_components_type_multisorted(self, table, sortlist):
        """ Fetch all components from a table, sorted by (optionally) multiple different columns
        :param table: name of the table (ex: "Resistor") (Hardcoded names only)
        :param sortlist: list of lists, like [[table, asc], [table, asc], [table, asc]] where table is the table to be sorted by, and asc a bool wether ascending or descending. Highest priority sort table listed first.
        :return: list of rows
        """
        ic(sortlist)
        c = self.conn.cursor()
        sql = "SELECT * FROM "+str(table)
        if sortlist:
            sql += " ORDER BY"
            for sort in sortlist:
                sql += " "+str(sort[0])
                if sort[1]:
                    sql += " ASC,"
                else:
                    sql += " DESC,"
            sql = sql[:-1] + ";"
        ic(sql)
        c.execute(sql)
        rows = c.fetchall()
        return rows

    def fetch_component_by_value(self,table, valuetype, value):
        """Fetch all components in the table with matching value
        :param table: name of the table to search in (ex: 'Resistor')
        :param valuetype: the column to search in (ex: "Footprint"
        :param value: The resistor value to search by.
        :return: rows, a list of rows with matching value.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM "+str(table)+" WHERE "+str(valuetype)+" = ?",(value,))
        rows = c.fetchall()
        return rows

    def check_item_exists_in_table(self, table, itemtype, item):
        """Checks whether a specific item is already present in the table. Can be used to prevent typos
        :param table: name of the table to search in (ex: 'Resistor')
        :param itemtype: name of the column to search in (ex: Footprint)
        :return: 0 or 1
        """
        c = self.conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM "+str(table)+" WHERE "+str(itemtype)+" = ? LIMIT 1)",(item,))
        return c.fetchall()[0][0]

    def _get_next_key(self, table):
        """returns highest index in the table +1"""
        c = self.conn.cursor()
        sql = "Select MAX(Key) from " + table
        c.execute(sql)
        MaxKey = c.fetchall()
        ic(MaxKey)
        ic(MaxKey[0][0])
        if MaxKey[0][0] == None:
            return 1
        else:
            return MaxKey[0][0] + 1

    def find_duplicates(self, table):
        c = self.conn.cursor()
        sql = "Select MfNr, COUNT(*) c FROM " + str(table) + " GROUP BY MfNr HAVING c >1"
        c.execute(sql)
        duplicates = c.fetchall()
        ic(duplicates)
        for duplicate in duplicates:
            rows = self.fetch_component_by_value(table, "MfNr", duplicate[0])
            ic(rows)            
            ic(rows[0][0:-1])
            if rows[0][0:-1] == rows[1][0:-1]:
                self.delete_entry_in_table(table, rows[1][-1])
            else:
                messagebox.showwarning("Database conflict", "Database conflict detected. Manufacturer number " + str(duplicate[0]) + " has multiple entries. Please resolve by deleting or editing one of them.")
    