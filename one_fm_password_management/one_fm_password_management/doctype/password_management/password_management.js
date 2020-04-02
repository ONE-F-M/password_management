// Copyright (c) 2020, ONE FM and contributors
// For license information, please see license.txt

frappe.ui.form.on('Password Management', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.set_df_property('password', 'read_only', true);
		}
	},
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
	},
	password_category: function(frm) {
		if(frm.doc.password_category){
			frappe.db.get_value('Password Category', frm.doc.password_category, 'ensure_strong_password', function(r) {
				if(r && r.ensure_strong_password){
					frm.set_value('ensure_strong_password', r.ensure_strong_password);
				}
				else{
					frm.set_value('ensure_strong_password', false);
				}
			})
		}
		else{
			frm.set_value('ensure_strong_password', false);
		}
	},
	create_new_password: function(frm) {
		create_new_password_dialog(frm);
	},
	go_to_url: function(frm) {
		window.location.href = frm.doc.url;
	}
});

var create_new_password_dialog = function(frm) {
	var d = new frappe.ui.Dialog({
		title: __("Create New Strong Password"),
		fields: [
			{ fieldtype: 'Password', reqd: 1, fieldname: 'password', label: 'Password'},
			{ fieldtype: 'Button', fieldname: 'generate_password', label: 'Generate Password',
				click: function() {
					generate_password(frm, d);
				}
			},
			{ fieldtype: 'Data', reqd: 1, read_only: 1, fieldname: 'new_password', label: 'New Password'},
			{ fieldtype: 'Check', reqd: 1, fieldname: 'make_sure_password_copied', label: 'Make sure the password is copied'},
		],
		primary_action_label: __("Update Password"),
		primary_action: function() {
			if(d.get_value('make_sure_password_copied') == 1){
				frappe.call({
					doc: frm.doc,
					method: 'set_new_password',
					args: {'new_password': d.get_value('new_password')},
					callback: function(r) {
						if(!r.exc){
							d.hide();
						}
					},
					freeze: true,
					freeze_message: __("Updating Password......")
				});
			}
			else{
				frappe.msgprint(__("Make sure the password is copied"));
			}
		}
	});
	d.show();
};

var generate_password = function(frm, d) {
	frappe.call({
		doc: frm.doc,
		method: 'generate_password',
		args: {'old_password': d.get_value('password')},
		callback: function(r) {
			if(r && r.message){
				d.set_values({'new_password': r.message});
			}
			else{
				d.set_values({'new_password': ''});
			}
		}
	});
};
