import sqlite3

from Config.Config  import *
from tkinter        import messagebox

####################################################
# Get information from Database
####################################################
def keycard_check(keycard_number) :
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()
        
        if DEBUG == True :
            print(keycard_number)
            
        cursor.execute("SELECT ID FROM Access_Card_Manage_TBL WHERE KeyCardID = ? ", (keycard_number,))
        KeyCardID_Input = cursor.fetchone()[0]
        
        if KeyCardID_Input:
            return True
            
            if DEBUG == True :
                print("keycard_check => KeyCardID_Input : ", KeyCardID_Input)
        else:
            return False
            
            if DEBUG == True :
                print("Employee not found")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()