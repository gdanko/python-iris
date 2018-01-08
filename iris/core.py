from shutil import copyfile
import os

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

copyfile(
	"{}/data/iris.db".format(PACKAGE_ROOT),
	"{}/.iris.db".format(os.path.expanduser("~"))
)

from iris.base import Account, Place
from iris.events import Event, Response
from iris.service import Rule, Scene, Session
from lomond import WebSocket
from pprint import pprint, pformat
import inspect
import iris.authenticator as authenticator
import iris.base as base
import iris.database as db
import iris.exception as exception
import iris.request as request
import iris.utils as utils
import json
import re
import signal
import sys
import threading
import time

DB_REFRESH_INTERVAL = 60

class SignalHandler(object):
	stopper = None
	workers = None
	def __init__(self, stopper, workers):
		self.stopper = stopper
		self.workers = workers

	def __call__(self, signum, frame):
		pprint(self.workers)
		self.stopper.set()
		for worker in self.workers:
			worker.join()
		sys.exit(0)

class Iris(object):
	def __init__(self, **kwargs):
		self.time_init = utils.now()
		self.success = None
		self.classname = utils.classname(self)
		self.websocket_uri = "wss://bc.irisbylowes.com/websocket"
		self.db_locked = False
		self.db_refresh_required = False

		if not "account" in kwargs:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="account")

		if "place_name" in kwargs:
			self.place_name = kwargs["place_name"]
		else:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="place_name")

		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.logger = utils.configure_logger(loggerid=self.classname, debug=self.debug)

		auth = authenticator.Authenticator(
			account=kwargs["account"],
			debug=self.debug
		)
		auth.authenticate()
		self.__init("irisAuthToken={}".format(auth.token))

	def stop(self):
		self.websocket.close()

	def disconnect(self):
		self.stop()

	def __lock_db(self):
		self.db_locked = True

	def __unlock_db(self):
		self.db_locked = False

	def __db_locked(self):
		return self.db_locked

	def __socket_run(self):
		while self.websocket.state.closed == False and self.websocket.state.closing == False:
			for e in self.websocket:
				event = Event(event=e, debug=self.debug)
				self.logger.debug("New \"{}\" event received: {}".format(event.type, pformat(event.__dict__)))
				self.__process_event(event)
		self.logger.debug("The state of the websocket is closed or closing. Exiting the event listener thread.")

	def __process_event(self, event):
		self.event_response = Response(event=event, debug=self.debug)
		self.event_ready.set()
		if self.event_response.event_type == "Text":
			self.logger.debug("Response type: {}".format(self.event_response.type))
			self.logger.debug("Event type: {}".format(self.event_response.event_type))
			self.logger.debug(pformat(self.event_response.__dict__))
			if self.event_response.type == "SessionCreated":
				self.__init_session(self.event_response)

			if self.event_response.db_refresh_required:
				self.db_refresh_required = True

	def signal_handler(self, signal, frame):
		print('You pressed Ctrl+C!')
		sys.exit(0)

	def __init(self, cookie):
		self.websocket = WebSocket(self.websocket_uri)
		self.websocket.add_header("Cookie".encode("utf-8"), cookie.encode("utf-8"))
		self.socket_ready = threading.Event()
		self.event_ready = threading.Event()
		self.stopper = threading.Event()

		t = threading.Thread(name="iris_listener", target=self.__socket_run)
		r = threading.Timer(1.0, self.__refresh_database)
		self.workers = [t, r]

		#handler = SignalHandler(self.stopper, self.workers)
		#signal.signal(signal.SIGINT, handler)

		for i, worker in enumerate(self.workers):
			print('Starting worker {}'.format(i))
			worker.start()

		if self.socket_ready.wait(5):
			session = Session(self)
			session.SetActivePlace(placeId=self.place_id)
			if session.success:
				self.account = Account(self)
				self.place = Place(self)
				self.rule = Rule(self)
				self.scene = Scene(self)
				db.prepare_database()
				self.__configure_database()
				self.place.GetHub()
				if self.place.success:
					self.hub_address = self.place.response["payload"]["attributes"]["hub"]["base:address"]
					self.time_ready = utils.now()
				else:
					# use an exception
					print("failed to get the hub's address")
					self.stop()

	def __init_session(self, event_response):
		places = [place for place in event_response.body["payload"]["attributes"]["places"] if place["placeName"] == self.place_name]
		if len(places) == 1:
			place = places[0]
			self.account_id = place["accountId"]
			self.account_address = "SERV:account:{}".format(self.account_id)
			self.place_id = place["placeId"]
			self.place_address = "SERV:place:{}".format(self.place_id)
			self.socket_ready.set()

	def __refresh_database(self):
		while self.websocket.state.closed == False and self.websocket.state.closing == False:
			if self.db_refresh_required == True:
				self.logger.debug("Initiating a refresh of the database.")
				self.__configure_database()
				self.db_refresh_required = False
				time.sleep(DB_REFRESH_INTERVAL)
			else:
				self.logger.debug("A database refresh is not needed at this time.")
				time.sleep(DB_REFRESH_INTERVAL)
		self.logger.debug("The state of the websocket is closed or closing. Exiting the database refresh thread.")

	def __configure_database(self):
		if self.db_locked == True:
			self.logger.error("The DB is currently locked. I am not able to update it. I will try again in {} seconds.".format(DB_REFRESH_INTERVAL))
		else:
			self.__lock_db()
			self.__populate_places()
			self.__populate_devices()
			self.__populate_people()
			self.__populate_rules()
			self.__populate_scenes()
			self.__unlock_db()

	def __populate_places(self):
		self.logger.debug(pformat(self.account))
		self.account.ListPlaces()
		if self.account.success:
			while not hasattr(self.event_response, "body"):
				print("sleeping")
				time.sleep(1)
			places = self.event_response.body["payload"]["attributes"]["places"]
			db.populate_places(places)
		else:
			raise exception.PopulateDatabaseError(table="places")
		
	def __populate_devices(self):
		self.logger.debug(pformat(self.place))
		self.place.ListDevices()
		if self.place.success:
			while not hasattr(self.event_response, "body"):
				print("sleeping")
				time.sleep(1)
			devices = self.event_response.body["payload"]["attributes"]["devices"]
			db.populate_devices(devices)
		else:
			raise exception.PopulateDatabaseError(table="devices")

	def __populate_people(self):
		self.logger.debug(pformat(self.place))
		self.place.ListPersons()
		if self.place.success:
			while not hasattr(self.event_response, "body"):
				print("sleeping")
				time.sleep(1)
			people = self.event_response.body["payload"]["attributes"]["persons"]
			db.populate_people(people)
		else:
			raise exception.PopulateDatabaseError(table="people")

	def __populate_rules(self):
		self.logger.debug(pformat(self.rule))
		self.rule.ListRules(placeId=self.place_id)
		if self.rule.success:
			while not hasattr(self.event_response, "body"):
				print("sleeping")
				time.sleep(1)
			rules = self.event_response.body["payload"]["attributes"]["rules"]
			db.populate_rules(rules)
		else:
			raise exception.PopulateDatabaseError(table="rules")

	def __populate_scenes(self):
		self.logger.debug(pformat(self.scene))
		self.scene.ListScenes(placeId=self.place_id)
		if self.scene.success:
			while not hasattr(self.event_response, "body"):
				print("sleeping")
				time.sleep(1)
			scenes = self.event_response.body["payload"]["attributes"]["scenes"]
			db.populate_scenes(scenes)
		else:
			raise exception.PopulateDatabaseError(table="scenes")

def whoami():
	return inspect.stack()[1][3]

def whosmydaddy():
	return inspect.stack()[2][3]

def now():
	return time.time()
