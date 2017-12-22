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

from pprint import pprint

class Iris(object):
	def __init__(self, **kwargs):
		self.success = None
		self.websocket_uri = "wss://bc.irisbylowes.com/websocket"

		if not "account" in kwargs:
			raise exception.MissingConstructorParameter(parameter="account")

		if "place_name" in kwargs:
			self.place_name = kwargs["place_name"]
		else:
			raise exception.MissingConstructorParameter(parameter="place_name")

		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.logger = utils.configure_logger(debug=self.debug)

		#data = pkgutil.get_data("iris", "data/method-validator.json")
		#print(data)
		# This is a hack to get it to work until I can get python data to work
		pwd = os.path.dirname(os.path.realpath(__file__))
		path = "{}/data/validator.json".format(pwd)
		self.validator = json.loads(open(path, "r").read())

		auth = authenticator.Authenticator(
			account=kwargs["account"],
			debug=self.debug
		)
		auth.authenticate()
		self.init("irisAuthToken={}".format(auth.token))

	def init(self, cookie):
		self.websocket = websocket.create_connection(
			self.websocket_uri,
			cookie=cookie
		)
		print(self.websocket)

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

	def configure_database(self):
		db.prepare_database()

		method_obj = self.validator["account"]["methods"]["ListPlaces"]
		request.account_request(client=self
			, namespace="account", method="ListPlaces", required=method_obj["required"],
			oneof=method_obj["oneof"], valid=method_obj["valid"])
		if self.success:
			db.populate_places(self.response["payload"]["attributes"]["places"])

		method_obj = self.validator["place"]["methods"]["ListDevices"]
		request.place_request(client=self, namespace="place", method="ListDevices", required=method_obj["required"],
			oneof=method_obj["oneof"], valid=method_obj["valid"])
		if self.success:
			db.populate_devices(self.response["payload"]["attributes"]["devices"])

		method_obj = self.validator["place"]["methods"]["ListPersons"]
		request.place_request(client=self, namespace="place", method="ListPersons", required=method_obj["required"],
			oneof=method_obj["oneof"], valid=method_obj["valid"])
		if self.success:
			db.populate_people(self.response["payload"]["attributes"]["persons"])

		method_obj = self.validator["rule"]["methods"]["ListRules"]
		request.rule_request(client=self, namespace="rule", method="ListRules", required=method_obj["required"],
			oneof=method_obj["oneof"], valid=method_obj["valid"])
		if self.success:
			db.populate_rules(self.response["payload"]["attributes"]["rules"])

		method_obj = self.validator["scene"]["methods"]["ListScenes"]
		request.rule_request(client=self, namespace="scene", method="ListScenes", required=method_obj["required"],
			oneof=method_obj["oneof"], valid=method_obj["valid"])
		if self.success:
			db.populate_scenes(self.response["payload"]["attributes"]["scenes"])
		