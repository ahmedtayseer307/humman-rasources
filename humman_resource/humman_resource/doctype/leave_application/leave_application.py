# Copyright (c) 2023, ahmed and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.data import date_diff


class LeaveApplication(Document):
    def validate(self):
        self.check_the_date()
        self.set_total_leave_days()
        self.get_total_leaves_allocated()
        self.check_balance_leave()
        self.check_for_negative_balance()
        self.check_for_max_continuous_days_allowed()

    def on_submit(self):
        self.update_balance_allocation_after_submit()
        self.check_for_applicable_after()

    def on_cancel(self):
        self.update_balance_altocation_after_cancel()

    def check_the_date(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                frappe.throw(_("From date cannot be after To date"))
            else:
                pass
        else:
            frappe.throw(_("you must select From and To Date"))

    def set_total_leave_days(self):
        if self.to_date and self.from_date:
            total_leave_day = date_diff(self.to_date, self.from_date) + 1
            if total_leave_day >= 0:
                self.total_leave_days = total_leave_day
            else:
                frappe.throw(("The total leave days can not be less 0"))
        else:
            frappe.throw(("Please enter To Date and From Date"))

    def check_balance_leave(self):
        if self.total_leave_days and self.leave_balance_before_application:
            if float(self.total_leave_days) > float(self.leave_balance_before_application):
                frappe.throw(_("you dont have more leave days balance at leave type ") + self.leave_type)

    def update_balance_allocation_after_submit(self):
        new_balance_days = float(self.leave_balance_before_application) - float(self.total_leave_days)
        frappe.db.sql(""" update `tableave Allocation` set total_leaves_allocated = {0}
	        WHERE employee = "{1}" AND leave_type ="{2}" AND to_date >= "{3}" And from_date <= "{4}" """
                      .format(new_balance_days, self.employee, self.leave_type, self.from_date, self.to_date),
                      as_dict=1)

    def get_total_leaves_allocated(self):
        if self.employee and self.to_date and self.from_date and self.leave_type:
            leave_allocatted = frappe.db.sql(""" select total_leaves_allocated from `tableave Allocation`
	        WHERE employee = "{0}" AND leave_type ="{1}" AND to_date >= "{2}" And from_date <= "{3}" """
                                             .format(self.employee, self.leave_type, self.from_date, self.to_date),
                                             as_dict=1)
            if leave_allocatted:
                self.leave_balance_before_application = str(leave_allocatted[0].total_leaves_allocated)
                return str(leave_allocatted[0].total_leaves_allocated)

    def check_for_applicable_after(self):
        # Assuming that working days must be zero
        leave_type = frappe.get_doc("Leave Type", self.leave_type)
        if leave_type.applicable_after:
            if float(leave_type.applicable_after) > 0:
                frappe.throw(
                    _("This leave type can only be applied after {0} working days").format(leave_type.applicable_after))
    def update_balance_altocation_after_cancel(self):
            leave_allocatted = frappe.db.sql(""" select total_leaves_allocated from `tableave Allocation`
            WHERE employee = "{0}" AND leave_type ="{1}" AND to_date >= "{2}" And from_date <= "{3}" """
            .format(self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
            if leave_allocatted:
                leave_balance_before_application = str(leave_allocatted[0].total_leaves_allocated)
                new_leave_allocatted = float(leave_balance_before_application) + float(self.total_leave_days)

                frappe.db.sql(""" update `tableave Allocation` set total_leaves_allocated = {0}
                    WHERE employee = "{1}" AND leave_type ="{2}" AND to_date >= "{3}" And from_date <= "{4}" """
                    .format(new_leave_allocatted, self.employee, self.leave_type , self.from_date, self.to_date), as_dict=1)

    def check_for_negative_balance(self):
        leave_type = frappe.get_doc("Leave Type", self.leave_type)
        if not leave_type.allow_negative_balance and float(self.leave_balance_before_application) < 0:
            frappe.throw(_("Leave balance cannot be negative for this leave type"))

    def check_for_max_continuous_days_allowed(self):
        leave_type = frappe.get_doc("Leave Type", self.leave_type)
        if leave_type.max_continuous_days_allowed:
            if float(self.total_leave_days) > float(leave_type.max_continuous_days_allowed):
                frappe.throw(
                    _("Total leave days cannot be more than the maximum continuous days allowed for this leave type"))


@frappe.whitelist(allow_guest=True)
def get_total_leaves(employee, leave_type, from_date, to_date):
    if employee and to_date and from_date and leave_type:

        leave_allocatted = frappe.db.sql(""" 
        select 
          total_leaves_allocated 
        from 
          `tableave Allocation` 
        WHERE 
          employee = '{0}' 
          AND leave_type = '{1}' 
          AND to_date >= '{2}' 
          And from_date <= '{3}'
        """.format(
            employee,
            leave_type,
            from_date,
            to_date), as_dict=1)
        if leave_allocatted:
            return float(leave_allocatted[0].total_leaves_allocated)


@frappe.whitelist()
def det_diff_date(from_date, to_date):
    if to_date and from_date:
        total_leave_day = date_diff(to_date, from_date) + 1
        if total_leave_day >= 0:
            total_leave_days = total_leave_day
            return int(total_leave_days)