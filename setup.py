# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in one_fm_password_management/__init__.py
from one_fm_password_management import __version__ as version

setup(
	name='one_fm_password_management',
	version=version,
	description='Password Management',
	author='ONE FM',
	author_email='develop@one-fm.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
