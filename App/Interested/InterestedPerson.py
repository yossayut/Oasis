import tkinter as tk
import sqlite3

from tkinter  import messagebox, simpledialog
from datetime import datetime

from config   import *

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#############################################################################################################
class InterestedPersonPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("บันทึกผู้สนใจ")
        self.geometry("400x400")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets_interested_person()
        self.display_interested_person()

    def create_widgets_interested_person(self):
        self.interested_listbox = tk.Listbox(self)
        self.interested_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Button to add a new interested person
        tk.Button(self, text="Add Interested Person", command=self.add_interested_person).pack(pady=10)

        # Button to delete the selected interested person
        tk.Button(self, text="Delete Selected", command=self.delete_selected).pack(pady=10)

    def display_interested_person(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            # Select interested persons from the table
            cursor.execute("SELECT * FROM Interested_People_TBL")
            rows = cursor.fetchall()
            for row in rows:
                self.interested_listbox.insert(tk.END, row)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            # Close the database connection
            if conn:
                conn.close()

    def add_interested_person(self):
        # TODO: Implement adding a new interested person
        pass

    def delete_selected(self):
        # Get the selected item
        selected_item = self.interested_listbox.get(tk.ACTIVE)

        if selected_item:
            # Connect to the SQLite database
            conn = sqlite3.connect(Oasis_database_full_path)
            cursor = conn.cursor()

            try:
                # Delete the selected interested person
                cursor.execute("DELETE FROM Interested_People_TBL WHERE InterestID = ?", (selected_item[0],))
                conn.commit()

                # Clear the listbox and display the updated data
                self.interested_listbox.delete(0, tk.END)
                self.display_interested_person()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

            finally:
                # Close the database connection
                if conn:
                    conn.close()

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()