from shutil import copyfile
import os

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

copyfile(
	"{}/data/iris.db".format(PACKAGE_ROOT),
	"{}/.iris.db".format(os.path.expanduser("~"))
)

from iris.base import Account
from iris.base import Place
from iris.service import Rule
from iris.service import Scene
from iris.service import Session
from lomond import WebSocket
from pprint import pprint, pformat
import iris.authenticator as authenticator
import iris.base as base
import iris.database as db
import iris.exception as exception
import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
import json
import re
import sys
import threading

class Iris(object):
	def __init__(self, **kwargs):
		self.success = None
		self.classname = utils.classname(self)
		self.websocket_uri = "wss://bc.irisbylowes.com/websocket"

		if not "account" in kwargs:
			raise exception.MissingConstructorParameter(parameter="account")

		if "place_name" in kwargs:
			self.place_name = kwargs["place_name"]
		else:
			raise exception.MissingConstructorParameter(parameter="place_name")

		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.logger = utils.configure_logger(loggerid=self.classname, debug=self.debug)

		auth = authenticator.Authenticator(
			account=kwargs["account"],
			debug=self.debug
		)
		auth.authenticate()
		self.init("irisAuthToken={}".format(auth.token))

	def process_event(self, content):
		response = utils.validate_json(content)
		if response:
			
			self.response = None
			if response["type"] == "base:ValueChange":
				if "source" in response["headers"]:
					name = db.name_from_address(address=response["headers"]["source"])
					if name != None:
						response["headers"]["name"] = name

			self.logger.debug(pformat(response))
			#if "correlationId" in response["headers"]:
			#	namespace, method = db.namespace_and_method_from_cid(response["headers"]["correlationId"])
			#	print(namespace)
			#	print(method)
			if "type" in response:
				if response["type"] == "SessionCreated":
					self.init_session(content)

				elif response["type"] == "Error":
					self.response = response
					self.method_ready.set()

				elif response["type"] == "base:ValueChange":
					pass

				elif response["type"] == "base:Added":
					pass

				elif response["type"] == "EmptyMessage":
					self.response = response
					self.method_ready.set()

				elif response["type"] == "base:SetAttributes":
					self.response = response
					self.method_ready.set()

				elif re.search("Response$", response["type"]):
					self.response = response
					self.method_ready.set()
				else:
					print(response["type"])

	def socket_run(self):
		for event in self.websocket:
			if event.name == "connecting":
				self.logger.debug("Connecting to {}".format(event.url))

			elif event.name == "connect_fail":
				raise exception.WebSocketConnectionFailed(message=event.reason)

			elif event.name == "rejected":
				raise exception.WebSocketUpgradeRejected(message=event.reason)

			elif event.name == "connected":
				self.logger.debug("Connected")

			elif event.name == "ready":
				self.logger.debug(event.response)

			if event.name == "text":
				self.process_event(event.text)

			elif event.name == "disconnected":
				if event.graceful == True:
					message = "The websocket disconnected gracefully."
				else:
					message = "The websocket disconnected unexpectedly: {}".format(event.reason)

				self.logger.debug(message)

			elif event.name == "closing":
				self.logger.debug("The websocket is closing: {}".format(event.reason))

			elif event.name == "closed":
				self.logger.debug("The websocket closed: {}".format(event.reason))

	def init(self, cookie):
		self.websocket = WebSocket(self.websocket_uri)
		self.websocket.add_header("Cookie".encode("utf-8"), cookie.encode("utf-8"))
		self.socket_ready = threading.Event()
		self.method_ready = threading.Event()

		t = threading.Thread(name="iris_listener", target=self.socket_run)
		t.start()
		if self.socket_ready.wait(5):
				session = Session(self)
				session.SetActivePlace(placeId=self.place_id)
				if session.success:
					db.prepare_database()
					self.configure_database()

	def init_session(self, content):
		response = utils.validate_json(content)
		request.validate_response(client=self, response=response)
		if self.success:
			places = [place for place in self.response["payload"]["attributes"]["places"] if place["placeName"] == self.place_name]
			if len(places) == 1:
				place = places[0]
				self.account_id = place["accountId"]
				self.account_address = "SERV:account:{}".format(self.account_id)
				self.place_id = place["placeId"]
				self.place_address = "SERV:place:{}".format(self.place_id)
				self.socket_ready.set()

	def configure_database(self):
		account = Account(self)
		place = Place(self)
		rule = Rule(self)
		scene = Scene(self)

		account.ListPlaces()
		if self.method_ready.wait(5):
			if account.success:
				request.validate_response(client=account, response=self.response)
				self.places = account.response["payload"]["attributes"]["places"]
				db.populate_places(self.places)
		
		place.ListDevices()
		if self.method_ready.wait(5):
			if place.success:
				request.validate_response(client=place, response=self.response)
				self.devices = place.response["payload"]["attributes"]["devices"]
				db.populate_devices(self.devices)

		place.ListPersons()
		if self.method_ready.wait(5):
			if place.success:
				request.validate_response(client=place, response=self.response)
				self.people = place.response["payload"]["attributes"]["persons"]
				db.populate_people(self.people)		

		rule.ListRules()
		if self.method_ready.wait(5):
			if rule.success:
				request.validate_response(client=rule, response=self.response)
				self.rules = rule.response["payload"]["attributes"]["rules"]
				db.populate_rules(self.rules)

		scene.ListScenes()
		if self.method_ready.wait(5):
			if scene.success:
				request.validate_response(client=scene, response=self.response)
				self.scenes = scene.response["payload"]["attributes"]["scenes"]
				db.populate_scenes(self.scenes)

	def stop(self):
		self.websocket.close()

	def disconnect(self):
		self.stop()