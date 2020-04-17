from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Tools"),
			"icon": "octicon octicon-briefcase",
			"items": [
				{
					"type": "doctype",
					"name": "Password Management",
					"label": _("Password Management"),
					"description": _("Password Management"),
					"onboard": 1,
				}
			]
		}
	]
