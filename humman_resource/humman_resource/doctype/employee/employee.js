// Copyright (c) 2023, ahmed and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", "validate", function(frm) {
    frm.doc.full_name = frm.doc.first_name +" "+ frm.doc.middle_name +" "+ frm.doc.last_name
    frm.set_df_property("full_name", "read_only", 1);
}
);


frappe.ui.form.on("Employee", "validate", function(frm) {
    if (!/^059\d{7}$/.test(frm.doc.mobile)) {
        frappe.throw(("Mobile number must be 10 digits and start with 059"));
    }
});

frappe.ui.form.on("Employee", "validate", function(frm) {
        if (frm.doc.status === "Active") {
            frappe.throw("Cannot save employee with active status ");
        }
    });



frappe.ui.form.on('Employee',{
    validate: function(frm) {
    var total_education = 0;
    $.each(frm.doc.employee_education,  function(i,  d) {
    if (d.university){
    total_education += 1; }
    }); 
    if (total_education < 2 ){
        frappe.throw( "Employee Education must be have at least Two Education")
      } else{
        frm.doc.count_education = total_education; 

      }
   
   }
    });
