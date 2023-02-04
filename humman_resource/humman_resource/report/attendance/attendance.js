// Copyright (c) 2023, ahmed and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance"] = {
	"filters": [
		{
            fieldname: 'Employee',
            label: __('Employee'),
            fieldtype: 'Link',
            options: 'Employee',
        },
		{
            fieldname: 'attendance_date',
            label: __('Attendance Date'),
            fieldtype: 'Date',
        }
	]
};
