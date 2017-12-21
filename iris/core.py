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
from iris.capabilities.account import Account
from iris.capabilities.place import Place
from iris.capabilities.rule import Rule
from iris.capabilities.scene import Scene

import sys
from pprint import pprint

class Iris(object):
	def __init__(self, **kwargs):
		global cookie
		global token

		self.success = None
		self.places = {}
		self.websocket_uri = "wss://bc.irisbylowes.com/websocket"

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
		self.websocket = websocket.create_connection(
			self.websocket_uri,
			cookie=cookie
		)

		response = utils.validate_json(self.websocket.recv())
		request.validate_response(client=self, response=response)
		if self.success:
			places = [place for place in self.response["payload"]["attributes"]["places"] if place["placeName"] == self.place_name]
			if len(places) == 1:
				place = places[0]
				self.account_id = place["accountId"]
				self.account_address = "SERV:account:{}".format(self.account_id)
				self.place_id = place["placeId"]
				self.place_address = "SERV:place:{}".format(self.place_id)

				payload = payloads.set_active_place(place_id=self.place_id)
				request.send(client=self, method="SetActivePlace", payload=payload, debug=self.debug)
				if self.success:
					self.configure_database()

	def configure_database(self, **kwargs):
		db.configure_database()

		account = Account(iris=self)
		account.ListPlaces()
		if account.success:
			db.populate_places(places=account.response["payload"]["attributes"]["places"])
		else:
			print("places failure")
			sys.exit(1)

		place = Place(iris=self)
		place.ListDevices()
		if place.success:
			self.devices = place.response["payload"]["attributes"]["devices"]
			db.populate_devices(devices=self.devices)
		else:
			print("devices failure")
			sys.exit(1)

		place.ListPersons()
		if place.success:
			self.people = place.response["payload"]["attributes"]["persons"]
			db.populate_people(people=self.people)
		else:
			print("people failure")
			sys.exit(1)

		rule = Rule(iris=self)
		rule.ListRules()
		if rule.success:
			self.rules = rule.response["payload"]["attributes"]["rules"]
			db.populate_rules(rules=self.rules)
		else:
			print("rule failure")
			sys.exit(1)

		scene = Scene(iris=self)
		scene.ListScenes()
		if scene.success:
			self.scenes = scene.response["payload"]["attributes"]["scenes"]
			pprint(self.scenes)
			db.populate_scenes(scenes=self.scenes)
		else:
			print("scene failure")
			sys.exit(1)			
