import os
import sys
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Django requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "iris",
	version = "0.3.2",
	author = "Gary Danko",
	author_email = "gdanko@gmail.com",
	url = "https://github.com/gdanko/python-iris",
	license = "GPLv3",
	description = "A Python based SDK for the Lowe's Iris 2nd generation API",
	packages = ["iris"],
	package_dir = {"iris": "iris"},
	package_data = {
		"iris": ["data/iris.db"],
	},
	install_requires = [
		"requests",
		"lomond",
		"pyyaml",
	],

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
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
	],
)

