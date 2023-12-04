import sqlite3
from tkinter       import ttk, messagebox
from Config.Config import *

class RoomFunctions:
    @staticmethod

    def display_show_all_room(tree, filter_var):
        if DEBUG == True :
            print("display_show_all_room => Oasis_database_full_path", Oasis_database_full_path)
            
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if filter_var.get() == "Show_all_room" :
                if DEBUG == True :
                    print("Show_all_room")

                cursor.execute("""
                                    WITH RoomStatusCTE AS (
                                        SELECT
                                            Apartment_Info_TBL.RoomNo,
                                            Apartment_Info_TBL.Building,
                                            Apartment_Info_TBL.Floor,
                                            CASE
                                                WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                                WHEN Apartment_Info_TBL.RoomType = 'BigType'   THEN 'GardenView Room'
                                                ELSE '-'
                                            END AS RoomType,
                                            CASE
                                                WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                                WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                                ELSE 'ว่าง'
                                            END AS RoomStatus,
                                            COALESCE(Customer_Contract.FirstName || ' ' || Customer_Contract.LastName || "(" || Customer_Contract.NickName || ")" , Customer_Booking.FirstName || ' ' || Customer_Booking.LastName ||  "(" || Customer_Booking.NickName || ")", '----------------') AS CustomerName,
                                            COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate, '----------------') AS StartDate,
                                            COALESCE(Contract_TBL.EndDate, Booking_TBL.EndDate, '----------------') AS EndDate,
                                            ROW_NUMBER() OVER (PARTITION BY Apartment_Info_TBL.RoomID ORDER BY COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate) DESC) AS RowNum
                                        FROM
                                            Apartment_Info_TBL
                                            LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                            LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                    )
                                    SELECT
                                        RoomNo,
                                        Building,
                                        Floor,
                                        RoomType,
                                        RoomStatus,
                                        CustomerName,
                                        StartDate,
                                        EndDate
                                    FROM RoomStatusCTE
                                    WHERE RowNum = 1
                                    ORDER BY RoomNo;
                               """)


            elif filter_var.get() == "Show_only_occupied_room" :
                if DEBUG == True :
                    print("Show_only_occupied_room")

                cursor.execute("""
                                    WITH RoomStatusCTE AS (
                                        SELECT
                                            Apartment_Info_TBL.RoomNo,
                                            Apartment_Info_TBL.Building,
                                            Apartment_Info_TBL.Floor,
                                            CASE
                                                WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                                WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'GardenView Room'
                                                ELSE '-'
                                            END AS RoomType,
                                            CASE
                                                WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                                WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN 'จอง'
                                                ELSE 'ว่าง'
                                            END AS RoomStatus,
                                            COALESCE(Customer_Contract.FirstName || ' ' || Customer_Contract.LastName || "(" || Customer_Contract.NickName || ")" , Customer_Booking.FirstName || ' ' || Customer_Booking.LastName ||  "(" || Customer_Booking.NickName || ")", '----------------') AS CustomerName,                                            COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate, '----------------') AS StartDate,
                                            COALESCE(Contract_TBL.EndDate, Booking_TBL.EndDate, '----------------') AS EndDate,
                                            ROW_NUMBER() OVER (PARTITION BY Apartment_Info_TBL.RoomID ORDER BY COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate) DESC) AS RowNum
                                        FROM
                                            Apartment_Info_TBL
                                            LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                            LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                    )
                                    SELECT
                                        RoomNo,
                                        Building,
                                        Floor,
                                        RoomType,
                                        RoomStatus,
                                        CustomerName,
                                        StartDate,
                                        EndDate
                                    FROM RoomStatusCTE
                                    WHERE RoomStatus IN ('เช่า')
                                    ORDER BY RoomNo;
                                """)

            elif filter_var.get() == "Show_only_booked_room" :
                if DEBUG == True :
                    print("Show_only_booked_room")

                cursor.execute("""
                                    WITH RoomStatusCTE AS (
                                        SELECT
                                            Apartment_Info_TBL.RoomNo,
                                            Apartment_Info_TBL.Building,
                                            Apartment_Info_TBL.Floor,
                                            CASE
                                                WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                                WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'GardenView Room'
                                                ELSE '-'
                                            END AS RoomType,
                                            CASE
                                                WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                                WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN 'จอง'
                                                ELSE 'ว่าง'
                                            END AS RoomStatus,
                                            COALESCE(Customer_Contract.FirstName || ' ' || Customer_Contract.LastName || "(" || Customer_Contract.NickName || ")" , Customer_Booking.FirstName || ' ' || Customer_Booking.LastName ||  "(" || Customer_Booking.NickName || ")", '----------------') AS CustomerName,                                            COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate, '----------------') AS StartDate,
                                            COALESCE(Contract_TBL.EndDate, Booking_TBL.EndDate, '----------------') AS EndDate,
                                            ROW_NUMBER() OVER (PARTITION BY Apartment_Info_TBL.RoomID ORDER BY COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate) DESC) AS RowNum
                                        FROM
                                            Apartment_Info_TBL
                                            LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                            LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                    )
                                    SELECT
                                        RoomNo,
                                        Building,
                                        Floor,
                                        RoomType,
                                        RoomStatus,
                                        CustomerName,
                                        StartDate,
                                        EndDate
                                    FROM RoomStatusCTE
                                    WHERE RoomStatus IN ('จอง')
                                    ORDER BY RoomNo;

                                """)

            elif filter_var.get() == "Show_free_room" :
                if DEBUG == True :
                    print("Show_free_room")

                cursor.execute("""
     
                                    WITH RoomStatusCTE AS (
                                        SELECT
                                            Apartment_Info_TBL.RoomNo,
                                            Apartment_Info_TBL.Building,
                                            Apartment_Info_TBL.Floor,
                                            CASE
                                                WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                                WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'GardenView Room'
                                                ELSE '-'
                                            END AS RoomType,
                                            CASE
                                                WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                                WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN 'จอง'
                                                ELSE 'ว่าง'
                                            END AS RoomStatus,
                                            COALESCE(Customer_Contract.FirstName || ' ' || Customer_Contract.LastName || "(" || Customer_Contract.NickName || ")" , Customer_Booking.FirstName || ' ' || Customer_Booking.LastName ||  "(" || Customer_Booking.NickName || ")", '----------------') AS CustomerName,                                            COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate, '----------------') AS StartDate,
                                            COALESCE(Contract_TBL.EndDate, Booking_TBL.EndDate, '----------------') AS EndDate,
                                            ROW_NUMBER() OVER (PARTITION BY Apartment_Info_TBL.RoomID ORDER BY COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate) DESC) AS RowNum
                                        FROM
                                            Apartment_Info_TBL
                                            LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                            LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                    )
                                    SELECT
                                        RoomNo,
                                        Building,
                                        Floor,
                                        RoomType,
                                        RoomStatus,
                                        CustomerName,
                                        StartDate,
                                        EndDate
                                    FROM RoomStatusCTE
                                    WHERE RoomStatus = 'ว่าง'
                                    ORDER BY RoomNo;
                                """)

            else :
                if DEBUG == True :
                    print("Show_all_room")

                cursor.execute("""
                                    WITH RoomStatusCTE AS (
                                        SELECT
                                            Apartment_Info_TBL.RoomNo,
                                            Apartment_Info_TBL.Building,
                                            Apartment_Info_TBL.Floor,
                                            CASE
                                                WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                                WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'GardenView Room'
                                                ELSE '-'
                                            END AS RoomType,
                                            CASE
                                                WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                                WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                                ELSE 'ว่าง'
                                            END AS RoomStatus,
                                            COALESCE(Customer_Contract.FirstName || ' ' || Customer_Contract.LastName || "(" || Customer_Contract.NickName || ")" , Customer_Booking.FirstName || ' ' || Customer_Booking.LastName ||  "(" || Customer_Booking.NickName || ")", '----------------') AS CustomerName,                                            COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate, '----------------') AS StartDate,
                                            COALESCE(Contract_TBL.EndDate, Booking_TBL.EndDate, '----------------') AS EndDate,
                                            ROW_NUMBER() OVER (PARTITION BY Apartment_Info_TBL.RoomID ORDER BY COALESCE(Contract_TBL.StartDate, Booking_TBL.StartDate) DESC) AS RowNum
                                        FROM
                                            Apartment_Info_TBL
                                            LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                            LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                            LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID
                                    )
                                    SELECT
                                        RoomNo,
                                        Building,
                                        Floor,
                                        RoomType,
                                        RoomStatus,
                                        CustomerName,
                                        StartDate,
                                        EndDate
                                    FROM RoomStatusCTE
                                    WHERE RowNum = 1
                                    ORDER BY RoomNo;
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