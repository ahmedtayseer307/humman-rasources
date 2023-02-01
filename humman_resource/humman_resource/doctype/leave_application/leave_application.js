// Copyright (c) 2023, ahmed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Application', {

employee:function(frm){
    frm.trigger("get_total_leaves");
},
leave_type:function(frm){
    frm.trigger("get_total_leaves");
},
from_date:function(frm){
    frm.trigger("get_total_leaves");
    frm.trigger("det_diff_date");
},
to_date:function(frm){
    frm.trigger("get_total_leaves");
    frm.trigger("det_diff_date");
},
get_total_leaves:function(frm){
    if (!frm.doc.employee |!frm.doc.leave_type |!frm.doc.from_date|!frm.doc.to_date ){
        return;
    }
    frappe.call({
        method:"humman_resource.humman_resource.doctype.leave_application.leave_application.get_total_leaves",
        args:{
            employee:frm.doc.employee,
            leave_type:frm.doc.leave_type,
            from_date:frm.doc.from_date,
            to_date:frm.doc.to_date

        },
        callback:(r) => {
            frm.doc.leave_balance_before_application = r.message;
            frm.refresh()
        }
    })
},

det_diff_date:function(frm){
    if (!frm.doc.from_date|!frm.doc.to_date){
        return;
    }
    frappe.call({
        method:"humman_resource.humman_resource.doctype.leave_application.leave_application.det_diff_date",
        args:{
            from_date:frm.doc.from_date,
            to_date:frm.doc.to_date
        },
        callback:(r) => {
            frm.doc.total_leave_days = r.message;
            frm.refresh()
        }
    })
}
});
