from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Tools"),
			"items": [
				{
					"type": "doctype",
					"name": "Password Management",
					"onboard": 1,
				},{
					"type": "doctype",
					"name": "Password Category",
					"onboard": 1,
				},
			]
		}
	]
