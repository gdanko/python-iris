import os
from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "iris",
	version = "0.1.2",
	author = "Gary Danko",
	author_email = "gdanko@gmail.com",
	url = "https://github.com/gdanko/python-iris",
	license = "GPLv3",
	description = "A Python based SDK for the Lowe's Iris 2nd generation API",
	packages = ["iris", "iris/devices"],
	package_dir = {
		"iris": "iris",
		"devices": "iris/devices"
	},
	install_requires = [
		"requests",
		"websocket-client",
		"pyyaml"
	],
	include_package_data = True,
	package_data = {
		"iris": [
			"data/method_validator.json"
		],
		"iris/devices": [
			"data/method_validator.json"
		]
	},
	#scripts = ["scripts/iris"],

	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers = [
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"Intended Audience :: System Administrators",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Natural Language :: English",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSIX :: Linux",
		"Operating System :: POSIX :: Other",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Topic :: Software Development :: Build Tools"
	],
)

