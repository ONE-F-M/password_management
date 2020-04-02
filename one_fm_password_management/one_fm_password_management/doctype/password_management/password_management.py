# -*- coding: utf-8 -*-
# Copyright (c) 2020, ONE FM and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, re
from frappe.model.document import Document
from frappe import _

class PasswordManagement(Document):
	def validate(self):
		self.set_valid_url()
		self.validate_strong_password()

	def check_my_password_strength(self):
		if self.password:
			return check_password_strength(self.password)
		return False

	def validate_my_url(self):
		if self.url:
			return validate_url(self.url)
		return False

	def set_valid_url(self):
		if self.url:
			if not validate_url(self.url):
				frappe.throw(_("The Given Url is not Valid."))
			else:
				self.valid_url = True

	def validate_strong_password(self):
		if self.password:
			strength = check_password_strength(self.password)
			if self.ensure_strong_password and strength != "Strong":
				frappe.throw(_("Password is not good, Include symbols, numbers, lowercase and uppercase letters in the password"))
			self.password_strength = strength

@frappe.whitelist()
def check_password_strength(pwd):
	# ref: https://www.codespeedy.com/check-the-password-strength-in-python/
	if(len(pwd)>=8):
		# must contain one digit similarly we say that for lowercase, uppercase and special characters
		if(bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', pwd))==True):
			return 'Strong'
		elif(bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})', pwd))==True):
			return 'Good'
	else:
		return 'Week'

@frappe.whitelist()
def validate_url(url):
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	if(bool(re.match(regex, url))==True):
		return True
	return False
