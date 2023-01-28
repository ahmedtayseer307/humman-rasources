# Copyright (c) 2023, ahmed and contributors
# For license information, please see license.txt

# from frappe.model.document import Document
import frappe
from datetime import datetime
from frappe.model.document import Document


class Employee(Document):
    def validate(self):
        if self.dob:
            today = datetime.now()
            date_of_brith = datetime.strptime(self.dob, '%Y-%m-%d')
            self.age = today.year - date_of_brith.year - ((today.month, today.day) < (date_of_brith.month, date_of_brith.day))
            if self.age > 60:
                frappe.throw("age cannot be more than 60 years.")
        else:
            frappe.throw("choose your birthday")
