import calendar
import datetime
import json
import logging
import os
import re
import requests
import sys
import time
import yaml

import iris.exception as exception
import iris.utils as utils
from pprint import pprint

class Authenticator(object):
	def __init__(self, **kwargs):
		self.response = {}
		self.success = True
		self.token = None

		if "account" in kwargs:
			self.account = kwargs["account"]
		else:
			raise exception.MissingConstructorParameter(parameter="account")

		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.logger = utils.configure_logger(debug=self.debug)
		self.authenticate()

	def authenticate(self, **kwargs):
		regenerate = False
		config_path = "{}/.iris.yml".format(os.path.expanduser("~"))
		config = utils.parse_config(account=self.account)
		account = config["accounts"][self.account]
		if "token" in account:
			if "timestamp" in account:
				now = int(time.time())
				if (now - account["timestamp"]) < 3550:
					self.token = account["token"]
					self.response = {"success": True, "body": account}
				else:
					regenerate = True
			else:
				regenerate = True
		else:
			regenerate = True

		if regenerate == True:
			self.get_credentials(config=config)
			if self.response["status"] == "success":
				self.token = self.response["token"]
				config["accounts"][self.account]["token"] = self.response["token"]
				config["accounts"][self.account]["timestamp"] = self.response["timestamp"]
				with os.fdopen(os.open(config_path, os.O_WRONLY | os.O_CREAT, 0o600), "w") as handle:
					handle.write(yaml.dump(config, default_flow_style=False, explicit_start=True))

	def get_credentials(self, config=None):
		account = config["accounts"][self.account]
		login_uri = "https://bc.irisbylowes.com/login"
		payload = {"user": account["username"], "password": account["password"], "public": "false"}
		session = requests.Session()
		# Wrap in a try/except
		res = session.post(login_uri, data=payload)

		status_code = res.status_code
		content_type = res.headers.get("content-type")

		# First check the HTML stuff
		body = res.content
		if len(body) <= 0: body = ""

		if res.headers.get("content-length"):
			content_length = int(res.headers.get("content-length"))
		else:
			content_length = len(body) if len(body) > 0 else 0

		try:
			if isinstance(body, str):
				json_body = utils.validate_json(body)
			elif isinstance(body, bytes):
				json_body = utils.validate_json(body.decode("utf-8"))
		except:
			raise exception.InvalidJsonError(status_code=status_code, body=body)

		if "status" in json_body:
			if json_body["status"] != "success":
				raise exception.AuthenticationError()

		# Now look for the Cookie
		if "Set-Cookie" in res.headers:
			cookies = self.__get_cookies(raw=res.headers["Set-Cookie"])
		else:
			raise exception.NoCookieError()

		if isinstance(cookies, dict):
			if "irisAuthToken" in cookies:
				date = datetime.datetime.strptime(cookies["Expires"],"%a, %d %b %Y %H:%M:%S %Z")
				timestamp = calendar.timegm(date.utctimetuple())
				self.success = True
				self.response = {
					"status": "success",
					"token": cookies["irisAuthToken"],
					"timestamp": timestamp
				}
			else:
				raise exception.NoTokenInCookieError()
		else:
			raise exception.CookieParseError()

	def __get_cookies(self, raw=None):
		cookies = {}
		pieces = re.split("\s*;\s*", raw)
		for piece in pieces:
			bits = re.split("\s*=\s*", piece)
			if len(bits) == 1:
				cookies[bits[0]] = None
			elif len(bits) == 2:
				cookies[bits[0]] = bits[1]
		return cookies