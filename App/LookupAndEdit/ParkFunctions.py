import sqlite3
from tkinter import ttk, messagebox
from Config.Config import *

class ParkFunctions:
    @staticmethod

    def display_show_all_parking(tree, filter_var):
        if DEBUG == True :
            print("come to display show all car")
        
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if filter_var.get() == "Show_all_car" :
                cursor.execute("""
                           SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName  || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Car' AS VehicleType,

                                CASE 
                                    WHEN Car_TBL.Brand_Model IS NOT NULL THEN Car_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Car_Brand,

                                CASE
                                    WHEN Car_TBL.Color IS NOT NULL THEN Car_TBL.Color
                                    ELSE '----------------'
                                END AS Car_color,
                                 
                                CASE WHEN Car_TBL.PlateNo IS NOT NULL THEN Car_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Car_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Car_TBL      ON Customer_Contract.CustomerID = Car_TBL.CustomerID
                            
                            WHERE
                                (Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active') OR
                                (Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active')

                            UNION

                            SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Motorcycle' AS VehicleType,

                                CASE 
                                    WHEN Motocycle_TBL.Brand_Model IS NOT NULL THEN Motocycle_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Motocycle_Brand,

                                CASE
                                    WHEN Motocycle_TBL.Color IS NOT NULL THEN Motocycle_TBL.Color
                                    ELSE '----------------'
                                END AS Motocycle_color,
                                 
                                CASE WHEN Motocycle_TBL.PlateNo IS NOT NULL THEN Motocycle_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Motocycle_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL    ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL     ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Motocycle_TBL   ON Customer_Contract.CustomerID = Motocycle_TBL.CustomerID 
                            WHERE
                                (Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active') OR
                                (Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active')

                            ORDER BY
                                RoomNo, VehicleType;

                """)

            elif filter_var.get() == "Show_only_parked_room" :
                cursor.execute("""
                           SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName  || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Car' AS VehicleType,

                                CASE 
                                    WHEN Car_TBL.Brand_Model IS NOT NULL THEN Car_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Car_Brand,

                                CASE
                                    WHEN Car_TBL.Color IS NOT NULL THEN Car_TBL.Color
                                    ELSE '----------------'
                                END AS Car_color,
                                 
                                CASE WHEN Car_TBL.PlateNo IS NOT NULL THEN Car_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Car_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Car_TBL      ON Customer_Contract.CustomerID = Car_TBL.CustomerID
                            
                            WHERE
                                Car_TBL.Brand_Model IS NOT NULL

                            UNION

                            SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Motorcycle' AS VehicleType,

                                CASE 
                                    WHEN Motocycle_TBL.Brand_Model IS NOT NULL THEN Motocycle_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Motocycle_Brand,

                                CASE
                                    WHEN Motocycle_TBL.Color IS NOT NULL THEN Motocycle_TBL.Color
                                    ELSE '----------------'
                                END AS Motocycle_color,
                                 
                                CASE WHEN Motocycle_TBL.PlateNo IS NOT NULL THEN Motocycle_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Motocycle_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL    ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL     ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Motocycle_TBL   ON Customer_Contract.CustomerID = Motocycle_TBL.CustomerID 
                           
                            WHERE
                                Motocycle_TBL.Brand_Model IS NOT NULL

                            ORDER BY
                                RoomNo, VehicleType;

                """)

            elif filter_var.get() == "Show_only_room_have_bike" :
                cursor.execute("""

                            SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Motorcycle' AS VehicleType,

                                CASE 
                                    WHEN Motocycle_TBL.Brand_Model IS NOT NULL THEN Motocycle_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Motocycle_Brand,

                                CASE
                                    WHEN Motocycle_TBL.Color IS NOT NULL THEN Motocycle_TBL.Color
                                    ELSE '----------------'
                                END AS Motocycle_color,
                                 
                                CASE WHEN Motocycle_TBL.PlateNo IS NOT NULL THEN Motocycle_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Motocycle_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL    ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL     ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Motocycle_TBL   ON Customer_Contract.CustomerID = Motocycle_TBL.CustomerID 
                            WHERE
                                Motocycle_TBL.Brand_Model IS NOT NULL
                            ORDER BY
                                RoomNo, VehicleType;


                """)

            elif filter_var.get() == "Show_only_room_have_car" :
                cursor.execute("""
                           SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName  || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Car' AS VehicleType,

                                CASE 
                                    WHEN Car_TBL.Brand_Model IS NOT NULL THEN Car_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Car_Brand,

                                CASE
                                    WHEN Car_TBL.Color IS NOT NULL THEN Car_TBL.Color
                                    ELSE '----------------'
                                END AS Car_color,
                                 
                                CASE WHEN Car_TBL.PlateNo IS NOT NULL THEN Car_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Car_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Car_TBL      ON Customer_Contract.CustomerID = Car_TBL.CustomerID
                            
                            WHERE
                                Car_TBL.Brand_Model IS NOT NULL
                           
                            ORDER BY
                                RoomNo, VehicleType;
                """)

            elif filter_var.get() == "Show_only_free_room" :
                cursor.execute("""
                           SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName  || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Car' AS VehicleType,

                                CASE 
                                    WHEN Car_TBL.Brand_Model IS NOT NULL THEN Car_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Car_Brand,

                                CASE
                                    WHEN Car_TBL.Color IS NOT NULL THEN Car_TBL.Color
                                    ELSE '----------------'
                                END AS Car_color,
                                 
                                CASE WHEN Car_TBL.PlateNo IS NOT NULL THEN Car_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Car_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Car_TBL      ON Customer_Contract.CustomerID = Car_TBL.CustomerID
                            
                            WHERE
                                (Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active') OR
                                (Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active')

                            UNION

                            SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Motorcycle' AS VehicleType,

                                CASE 
                                    WHEN Motocycle_TBL.Brand_Model IS NOT NULL THEN Motocycle_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Motocycle_Brand,

                                CASE
                                    WHEN Motocycle_TBL.Color IS NOT NULL THEN Motocycle_TBL.Color
                                    ELSE '----------------'
                                END AS Motocycle_color,
                                 
                                CASE WHEN Motocycle_TBL.PlateNo IS NOT NULL THEN Motocycle_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Motocycle_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL    ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL     ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Motocycle_TBL   ON Customer_Contract.CustomerID = Motocycle_TBL.CustomerID 
                            WHERE
                                (Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active') OR
                                (Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active')

                            ORDER BY
                                RoomNo, VehicleType;

                """)

            else :
                cursor.execute("""
                            SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName  || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Car' AS VehicleType,

                                CASE 
                                    WHEN Car_TBL.Brand_Model IS NOT NULL THEN Car_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Car_Brand,

                                CASE
                                    WHEN Car_TBL.Color IS NOT NULL THEN Car_TBL.Color
                                    ELSE '----------------'
                                END AS Car_color,
                                 
                                CASE WHEN Car_TBL.PlateNo IS NOT NULL THEN Car_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Car_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Car_TBL      ON Customer_Contract.CustomerID = Car_TBL.CustomerID
                            
                            WHERE
                                (Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active') OR
                                (Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active')

                            UNION

                            SELECT
                                Apartment_Info_TBL.RoomNo,
                                Apartment_Info_TBL.Building,
                                Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Small'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'Big'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                'Motorcycle' AS VehicleType,

                                CASE 
                                    WHEN Motocycle_TBL.Brand_Model IS NOT NULL THEN Motocycle_TBL.Brand_Model
                                    ELSE '----------------'
                                END AS Motocycle_Brand,

                                CASE
                                    WHEN Motocycle_TBL.Color IS NOT NULL THEN Motocycle_TBL.Color
                                    ELSE '----------------'
                                END AS Motocycle_color,
                                 
                                CASE WHEN Motocycle_TBL.PlateNo IS NOT NULL THEN Motocycle_TBL.PlateNo
                                    ELSE '----------------'
                                END AS Motocycle_plateno

                            FROM
                                Apartment_Info_TBL
                                LEFT JOIN Contract_TBL    ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                LEFT JOIN Booking_TBL     ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                LEFT JOIN Customer_TBL    AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                LEFT JOIN Motocycle_TBL   ON Customer_Contract.CustomerID = Motocycle_TBL.CustomerID 
                            WHERE
                                (Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active') OR
                                (Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active')

                            ORDER BY
                                RoomNo, VehicleType;

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