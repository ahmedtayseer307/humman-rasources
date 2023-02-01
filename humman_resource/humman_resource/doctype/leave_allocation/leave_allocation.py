# Copyright (c) 2023, ahmed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from frappe import _


class leaveAllocation(Document):
	def validate(self):
		self.check_the_date()
		self.check_existing_allocation()

	def check_the_date(self):
		if self.from_date and self.to_date:
			if self.from_date > self.to_date:
				frappe.throw(_("From date cannot be after To date"))
			else:
				return 1
		else:
			frappe.throw(_("you must select From and To Date"))
	def check_existing_allocation(self):
		existing_allocation = frappe.db.exists("leave Allocation", {
			"employee": self.employee,
			"leave_type": self.leave_type,
			"from_date": ["<=", self.from_date],
			"to_date": [">=", self.to_date]
		})
		if existing_allocation:
			frappe.throw(_("Leave allocation already exists for the selected dates, employee and leave type"))
