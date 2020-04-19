from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Tools"),
			"icon": "fa fa-star",
            "items": [
				{
					"color": "grey",
					"icon": "octicon octicon-key",
					"type": "doctype",
					"name": "Password Management",
					"label": _("Password Management")
				},
				{
					"color": "grey",
					"icon": "octicon octicon-key",
					"type": "doctype",
					"name": "Password Category",
					"label": _("Password Category")
				}
            ]
		}
	]
