import sqlite3

from Config.Config  import *
from tkinter        import messagebox

####################################################
# Get information from Database
####################################################
def fill_customer_database(prefix, first_name, last_name, nick_name, thai_national_id, birth_day, address_number, address_cont, address_road, address_sub_province, address_province, address_city, phone, line_id, job, emergency, register_date):
    try:
        # Insert data into the table
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        sql = """
            INSERT INTO Customer_TBL 
            (Prefix, FirstName, LastName, NickName, ThaiNationalID, BirthDay, AddressNumber, AddressCont,
            AddressRoad, AddressSubProvince, AddressProvince, AddressCity, Phone, LineID, Job, ReferencePerson, RegisterDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Parameters for the query
        params = (prefix, first_name, last_name, nick_name, thai_national_id, birth_day, address_number, address_cont, address_road, address_sub_province, address_province, address_city, phone, line_id, job, emergency, register_date)

        cursor.execute(sql, params)
        conn.commit()

        return True  # Return True if the insertion is successful

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return False  # Return False if there's an error

    finally:
        # Close the database connection
        if conn:
            conn.close()