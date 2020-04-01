// Copyright (c) 2020, ONE FM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Password Management', {
	password: function(frm) {
    console.log(frm.doc.password);
	}
});
