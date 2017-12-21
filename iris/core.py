import asyncio
import inspect
import json
import os
import pkgutil
import re
import sys
import websocket
import iris.authenticator as authenticator
import iris.database as db
import iris.exception as exception
import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.base.account import Account
from iris.base.place import Place
from iris.base.rule import Rule

import sys
from pprint import pprint

# Types
# MotionSensor: Motion
# Smoke/CO Detector: Smoke/CO
# Thermostat: Thermostat
# Door lock: Lock
# Smart Plug: Switch
# Key fob: KeyFob
# Contact Sensor: Contact
# Door sensor: Contact
# Tilt sensor: Tilt

# Capabilities
# Common = ['dev', 'devadv', 'devconn', 'devpow']
# Motion: ['dev', 'devadv', 'devconn', 'devpow', 'mot', 'temp']
# Smoke/CO: ['co', 'dev', 'devadv', 'devconn', 'devpow', 'smoke', 'test']
# Thermostat: ["clock", "dev", "devadv", "devconn", "devpow", "humid", "indicator", "temp", "therm"]
# Door lock: ['dev', 'devadv', 'devconn', 'devpow', 'doorlock']
# Smart plug 1st gen: ['centralitesmartplug', 'dev', 'devadv', 'devconn', 'devota', 'devpow', 'ident', 'pow', 'swit']
# Smart plug 2nd gen: ['centralitesmartplug', 'dev', 'devadv', 'devconn', 'devota', 'devpow', 'ident', 'pow', 'swit']
# Key fob: ['dev', 'devadv', 'devconn', 'devpow', 'pres']
# Contact sensor: ['cont', 'dev', 'devadv', 'devconn', 'devpow', 'temp']
# Door sensor: ['cont', 'dev', 'devadv', 'devconn', 'devpow']
# Light switch: ['dev', 'devadv', 'devconn', 'devpow', 'indicator', 'swit']
# Tilt sensor ['cont', 'dev', 'devadv', 'devconn', 'devpow', 'tilt']
# Dimmer ['dev', devadv', 'devconn','devpow','dim','indicator','swit']


# 1) Login to websocket
# 2) See if the selected place is in result
# 3) If it is, get account ID and place ID
# 4) Instantiate account and place to generate everything

class Iris(object):
	def __init__(self, **kwargs):
		global cookie
		global token

		self.success = None
		self.places = {}
		self.ws_uri = "wss://bc.irisbylowes.com/websocket"

		if not "account" in kwargs:
			raise exception.MissingConstructorParameter(parameter="account")

		if "place_name" in kwargs:
			self.place_name = kwargs["place_name"]
		else:
			raise exception.MissingConstructorParameter(parameter="place_name")

		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.logger = utils.configure_logger(debug=self.debug)

		auth = authenticator.Authenticator(
			account=kwargs["account"],
			debug=self.debug
		)
		auth.authenticate()
		token = auth.token
		cookie = "irisAuthToken={}".format(token)

		#data = pkgutil.get_data("iris", "data/method-validator.json")
		#print(data)
		# This is a hack to get it to work until I can get python data to work
		pwd = os.path.dirname(os.path.realpath(__file__))
		path = "{}/data/validator.json".format(pwd)
		self.validator = json.loads(open(path, "r").read())
		self.init()

	def init(self, **kwargs):
		self.ws = websocket.create_connection(
			self.ws_uri,
			cookie=cookie
		)

		result = utils.validate_json(self.ws.recv())
		self.process_result(result)

		payload = payloads.set_active_place(place_id=self.place_id)
		request.send(client=self, payload=payload, debug=self.debug)

		self.configure_database()

	def process_result(self, result):
		if "type" in result:
			if result["type"] == "SessionCreated":
				if "payload" in result and "attributes" in result["payload"]:
					if "places" in result["payload"]["attributes"]:
						places = [place for place in result["payload"]["attributes"]["places"] if place["placeName"] == self.place_name]
						if len(places) == 1:
							place = places[0]
							self.account_id = place["accountId"]
							self.account_address = "SERV:account:{}".format(self.account_id)
							self.place_id = place["placeId"]
							self.place_address = "SERV:place:{}".format(self.place_id)				
						else:
							print("place not found. please create a proper exception.")
							sys.exit(1)
					else:
						print("no places returned. please create a proper exception.")
						sys.exit(1)
				else:
					print("no payload returned. please create a proper exception.")
					sys.exit(1)
			else:
				print("something went wrong. please create a proper exception.")
				sys.exit(1)

	def configure_database(self, **kwargs):
		db.configure_database()
		# Places
		account = Account(iris=self)
		account.ListPlaces()
		if account.success:
			db.populate_places(places=account.response["payload"]["attributes"]["places"])
		else:
			print("places failure")
			sys.exit(1)

		# Devices
		place = Place(iris=self)
		place.ListDevices()
		if place.success:
			self.devices = place.response["payload"]["attributes"]["devices"]
			db.populate_devices(devices=self.devices)
		else:
			print("devices failure")
			sys.exit(1)

		# People
		place.ListPersons()
		if place.success:
			self.people = place.response["payload"]["attributes"]["persons"]
			db.populate_people(people=self.people)
		else:
			print("people failure")
			sys.exit(1)

		# Rules
		rule = Rule(iris=self)
		rule.ListRules()
		if rule.success:
			self.rules = rule.response["payload"]["attributes"]["rules"]
			db.populate_rules(rules=self.rules)
		else:
			print("rule failure")
			sys.exit(1)
