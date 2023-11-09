import sqlite3

from Config.Config  import *
from tkinter        import messagebox

####################################################
# Get information from Database
####################################################
def get_current_customer_name() :
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)  
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Customer_TBL.FirstName, Customer_TBL.LastName
            FROM Contract_TBL
            JOIN  Customer_TBL on Contract_TBL.CustomerID = Customer_TBL.CustomerID
            WHERE Contract_TBL.Status = "Active"
            ORDER By Customer_TBL.FirstName
        """)

        current_customer_names = cursor.fetchall()

        if not current_customer_names:
            return ["ยังไม่มีลูกค้า กรุณาทำสัญญาก่อนเบิกบัตร"]
        else:
            return current_customer_names

       # if DEBUG == True :
        #    for item in current_customer_names:
         #       print(item)
        
        return current_customer_names

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()