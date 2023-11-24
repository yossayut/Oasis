import sqlite3
from tkinter       import ttk, messagebox
from Config.Config import *

class RoomFunctions:
    @staticmethod

    def display_show_all_room(tree, filter_var):
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if filter_var.get() == "Show_all_room" :
                if DEBUG == True :
                    print("Show_all_room")

                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'GardenView Room'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                    ELSE '-------- ว่าง --------'
                                END AS RoomStatus,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.StartDate
                                    ELSE '----------------'
                                END AS StartDate,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.EndDate
                                    ELSE '----------------'
                                END AS EndDate  

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID   = Contract_TBL.CustomerID

                                    LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID   = Booking_TBL.CustomerID

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;
                """)

            elif filter_var.get() == "Show_only_occupied_room" :
                if DEBUG == True :
                    print("Show_only_occupied_room")

                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,
                                    CASE
                                        WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                        WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'GardenView Room'
                                        ELSE '-'
                                    END AS RoomType,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                        ELSE '-------- ว่าง --------'
                                    END AS RoomStatus,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                        ELSE '----------------'
                                    END AS CustomerName,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                        ELSE '----------------'
                                    END AS StartDate,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                        ELSE '----------------'
                                    END AS EndDate

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID

                                WHERE
                                    Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active'  -- Show only rooms with an active contract

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;
                """)

            elif filter_var.get() == "Show_only_booked_room" :
                if DEBUG == True :
                    print("Show_only_booked_room")

                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,
                                    CASE
                                        WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                        WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'GardenView Room'
                                        ELSE '-'
                                    END AS RoomType,

                                    CASE
                                        WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN 'จอง'
                                        ELSE '-------- ว่าง --------'
                                    END AS RoomStatus,

                                    CASE
                                        WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                        ELSE '----------------'
                                    END AS CustomerName,

                                    '----------------' AS StartDate,  -- Placeholder for StartDate
                                    '----------------' AS EndDate     -- Placeholder for EndDate

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID

                                WHERE
                                    Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active'  -- Show only rooms with an active booking

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;

                """)

            elif filter_var.get() == "Show_free_room" :
                if DEBUG == True :
                    print("Show_free_room")

                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,
                                    CASE
                                        WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                        WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'GardenView Room'
                                        ELSE '-'
                                    END AS RoomType,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                        ELSE '-------- ว่าง --------'
                                    END AS RoomStatus,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                        ELSE '----------------'
                                    END AS CustomerName,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.StartDate
                                        ELSE '----------------'
                                    END AS StartDate,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.EndDate
                                        ELSE '----------------'
                                    END AS EndDate  

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                    LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID

                                WHERE
                                    (Contract_TBL.RoomID IS NULL OR Contract_TBL.Status != 'Active') AND
                                    (Booking_TBL.RoomID IS NULL OR Booking_TBL.Status != 'Active')  -- Show only rooms without an active contract or booking

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;

                """)

            else :
                if DEBUG == True :
                    print("Show_all_room")

                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'GardenView Room'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                    ELSE '-------- ว่าง --------'
                                END AS RoomStatus,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.StartDate
                                    ELSE '----------------'
                                END AS StartDate,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.EndDate
                                    ELSE '----------------'
                                END AS EndDate  

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID   = Contract_TBL.CustomerID

                                    LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID   = Booking_TBL.CustomerID

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;
                """)

            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                background_color = "light gray" if i % 2 == 0 else "white"
                tree.tag_configure(f"row{i}", background=background_color)
                tree.insert("", "end", values=row, tags=(f"row{i}"))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()