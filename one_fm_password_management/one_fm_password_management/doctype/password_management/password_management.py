# -*- coding: utf-8 -*-
# Copyright (c) 2020, ONE FM and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, re
from frappe.model.document import Document
from frappe import _
from frappe.utils.password import get_decrypted_password, set_encrypted_password

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

	def generate_password(self, old_password):
		if get_decrypted_password(self.doctype, self.name, 'password', raise_exception=True) == old_password:
			return create_new_password()
		else:
			frappe.msgprint(_("Incorrect Password.!!"))

	def set_new_password(self, new_password):
		set_encrypted_password(self.doctype, self.name, new_password, 'password')
		self.reload()

	def get_my_password(self):
		if check_user_exist_in_list(self):
			return get_decrypted_password(self.doctype, self.name, 'password', raise_exception=True)
		else:
			frappe.throw(_("You have no permission to view the password."))

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

@frappe.whitelist()
def create_new_password():
	# generate a password with length "passlen" with no duplicate characters in the password
	import random
	str = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
	pwd = "".join(random.sample(str, 8))
	if check_password_strength(pwd) == "Strong":
		return pwd
	else:
		create_new_password()

def check_user_exist_in_list(doc):
	if doc.user_list:
		for user in doc.user_list:
			if user.user == frappe.session.user:
				return True
	return True if (frappe.session.user == 'Administrator') else False
