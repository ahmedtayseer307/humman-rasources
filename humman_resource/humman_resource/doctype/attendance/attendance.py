# Copyright (c) 2023, ahmed and contributors
# For license information, please see license.txt
from datetime import datetime, timedelta

import frappe
from frappe.model.document import Document


class Attendance(Document):
    def on_submit(self):
        self.get_hours_work()
        self.update_status_value_in_attendance()

    def get_hours_work(self):
        if self.check_out and self.check_in:
            # late entry grace period
            late_entry_grace_period_in_minits = frappe.db.get_single_value('Attendance Settings',
                                                                           'late_entry_grace_period')

            # early exit grace period
            early_exit_grace_period = frappe.db.get_single_value('Attendance Settings', 'early_exit_grace_period')

            # H,M,S to 24h format...
            # h,m,s to 12h format...
            start_time = frappe.db.get_single_value('Attendance Settings', 'start_time')
            start_time = datetime.strptime(str(start_time), '%H:%M:%S')
            end_time = frappe.db.get_single_value('Attendance Settings', 'end_time')
            end_time = datetime.strptime(str(end_time), '%H:%M:%S')

            # check in
            check_in = datetime.strptime(self.check_in, '%H:%M:%S')

            # check out
            check_out = datetime.strptime(self.check_out, '%H:%M:%S')

            # late come
            late_come_in_hours = start_time.hour - check_in.hour
            late_in_minutes = start_time.minute - check_in.minute + late_entry_grace_period_in_minits
            late_entry = late_come_in_hours + (late_in_minutes / 60)
            if late_entry > 0:
                late_entry = 0

            # early leave
            early_leave_hours = check_out.hour - end_time.hour
            early_leave_minutes = end_time.minute - check_out.minute - early_exit_grace_period
            early_leave = early_leave_hours - (early_leave_minutes / 60)
            if early_leave > 0:
                early_leave = 0

            self.late_hours = -(late_entry + early_leave)
            self.work_hours = 8 - self.late_hours

    def update_status_value_in_attendance(self):
        working_hours_threshold_for_absent = \
            frappe.db.get_single_value('Attendance Settings', 'working_hours_threshold_for_absent')
        if self.work_hours <= working_hours_threshold_for_absent:
            self.status = "Absent"
        else:
            self.status = "Present"

@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out):
    if not attendance_date or not check_in or not check_out:
        frappe.throw("Attendance Date, Check In, and Check Out are required")

    new_attendance = frappe.new_doc("Attendance")
    new_attendance.employee = frappe.get_doc("Employee", {"user": frappe.session.user}).name
    new_attendance.attendance_date = attendance_date
    new_attendance.check_in = check_in
    new_attendance.check_out = check_out
    new_attendance.insert()
    return {"message": "Attendance created successfully"}
