import sqlite3

from Config.Config  import *
from tkinter        import messagebox

####################################################
# Get information from Database
####################################################
def get_customer_info_submit_form(self) :
    ####################################################
    # Get information from text box
    ####################################################
    selected_room         = self.room
    prefix                = self.prefix_entry.get()
    first_name            = self.first_name_entry.get()
    last_name             = self.last_name_entry.get()
    nick_name             = self.nick_name_entry.get()
    thai_national_id      = self.national_ID_entry.get()
    birth_day             = self.birthday_entry.get()
    address_number        = self.address_entry.get()
    address_cont          = self.address_cont_entry.get()
    address_road          = self.address_road_entry.get()
    address_sub_province  = self.address_sub_province_entry.get()
    address_province      = self.address_province_entry.get()
    address_city          = self.address_city_entry.get()
    phone                 = self.phone_entry.get()
    line_id               = self.lineID_entry.get()
    job                   = self.job_entry.get()
    emergency             = self.emergency_entry.get()
    register_date         = self.register_date_entry.get()
    register_end_date     = self.register_end_date_entry.get()

    ####################################################
    # Get information from text box : Column2
    ####################################################       
    employee              = self.selected_employee.get()
    room_fee              = self.room_fee_entry.get()  
    internet              = self.internet_fee_entry.get()
    maintenance           = self.maintenance_fee_entry.get()
    parking               = self.parking_fee_entry.get()
    remark                = self.remark_entry.get()

    return selected_room,     \
           prefix,            \
           first_name,        \
           last_name,         \
           nick_name,         \
           thai_national_id,  \
           birth_day,         \
           address_number,    \
           address_cont,      \
           address_road,      \
           address_sub_province,    \
           address_province,        \
           address_city,            \
           phone,             \
           line_id,           \
           job,               \
           emergency,         \
           register_date,     \
           register_end_date, \
           employee,          \
           room_fee,          \
           internet,          \
           maintenance,       \
           parking,           \
           remark