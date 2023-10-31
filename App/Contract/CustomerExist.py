import tkinter as tk
import sqlite3

from Config.Config   import *
from tkinter  import messagebox, simpledialog
from datetime import datetime

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#############################################################################################################
class CustomerExistPage(tk.Toplevel):

    # 1 : Update your __init__ method to include self.edit_mode
    def __init__(self, master):
        if DEBUG == True :
            print("ข้อมูลลูกค้า")
        super().__init__(master)
        self.title("ข้อมูลลูกค้า")
        self.geometry("400x400")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()
        self.display_exist_customer()
        self.selected_customer_info = None # Initialize edit mode as False

    # 2 : Run   
    def create_widgets(self):
        if DEBUG == True :
            print("create_widgets_customer : CustomerExistPage.py")

        self.customer_listbox = tk.Listbox(self)
        self.customer_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        tk.Button(self, text="เลือก", command=self.select_Exist_customer).pack(pady=10)
    
    # 4 : Run
    def get_selected_customer_info(self):
        if DEBUG == True :
            print("get_selected_customer_info : CustomerExistPage.py")

        return self.selected_customer_info

    ###########################################################################################################
    # Exist customer window display
    ###########################################################################################################
    def display_exist_customer(self):
        if DEBUG == True :
            print("display_customer : CustomerExistPage.py")

        # Connect to the SQLite database
        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        customer_info_list = []
        self.customer_ids  = [] 

        try:
            cursor.execute("""SELECT * 
                              FROM Customer_TBL
                              ORDER BY FirstName""")
            rows = cursor.fetchall()

            # Display headers
            header = "{:<7} | {:<10}  {:<15}  {:<15}  {:<15} | {:<15}".format("ID", "Prefix", "First Name", "Last Name", "Nick Name", "Phone")
            self.customer_listbox.insert(tk.END, header)

            # Display customer information with separated columns
            for row in rows:
                customer_id = row[0]
                prefix, first_name, last_name, nick_name, phone = row[1], row[2], row[3], row[4], row[13]
                customer_info_list.append(row)                              # Append customer information to the list
                self.customer_ids.append(customer_id)                       # Store the customer ID
                customer_id_width = 3 if len(str(customer_id)) <= 1 else 0  # Determine the column width for customer_id based on its length
                formatted_info = "{:<{}} | {:<10}  {:<15}  {:<15} | {:<15} | {:<15}".format(customer_id, customer_id_width, prefix, first_name, last_name, nick_name, phone)
                self.customer_listbox.insert(tk.END, formatted_info)        # Format the customer information with separated columns

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            # Close the database connection
            if conn:
                conn.close()

        # Store the customer information list
        self.customer_info_list = customer_info_list

    ###########################################################################################################
    # Exist customer select from Display
    ###########################################################################################################
    def select_exist_customer(self):
        selected_item = self.customer_listbox.curselection()

        if DEBUG == True :
            print(selected_item)

        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a customer.")
            return

        # Selected item : Show the row following the selection (Not show the id so it can't use directly)
        # Ex I select : ID : 21 ทินกร แต่มันแสดงผลใน row 15, so 15 number is used as ID 15 : ทวีกร 
        index = int(selected_item[0])

        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            # Select customers from the table
            cursor.execute("""SELECT * 
                              FROM Customer_TBL
                              ORDER BY FirstName""")
            
            customer_info_array = cursor.fetchall()
            if DEBUG == True :
                for item in customer_info_array:
                    print(item)

            customer_info       = customer_info_array[index-1]
            #if DEBUG == True :
            #    print(customer_info)

            if customer_info:
                print("select_Exist_customer : CustomerExist.py")
                self.master.fill_customer_exist_info(customer_info)  # Fill the entry fields in the registration form
                self.destroy()
            else:
                messagebox.showinfo("Customer Not Found", "Customer information not found.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

    # 7 : 
    def on_close(self):
        #print("on close")
        self.master.deiconify()  # Show the main page
        self.destroy()
