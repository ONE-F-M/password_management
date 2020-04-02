// Copyright (c) 2020, ONE FM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Password Management', {
	password: function(frm) {
    frappe.call({
      doc: frm.doc,
      method: 'check_my_password_strength',
      callback: function(r) {
        frm.set_value('password_strength', r.message?r.message:'');
      }
    });
	},
  password_strength: function(frm) {
    let strength_list = {'Week': 'red', 'Good': 'orange', 'Strong': 'green'};
    let description = '';
    if(frm.doc.password_strength){
      description = '<font color="'+strength_list[frm.doc.password_strength]+'">'+__(frm.doc.password_strength)+'</font>';
    }
    frm.set_df_property('password', 'description', description);
  },
  url: function(frm) {
    frappe.call({
      doc: frm.doc,
      method: 'validate_my_url',
      callback: function(r) {
        if(r.message){
          frm.set_value("valid_url", true);
        }
        if(!r.message && frm.doc.url){
          frm.set_value("valid_url", false);
          frappe.throw(__("The Given Url is not Valid."));
        }
      }
    });
	}
});
