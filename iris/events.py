from pprint import pprint, pformat
import inspect
import iris.database as db
import iris.utils as utils
import re
import sys
import time

USE_FARENEHEIT = True

class Event(object):
	def __init__(self, **kwargs):
		self.success = True
		global logger

		classname = utils.classname(self)
		debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		logger = utils.configure_logger(loggerid=classname, debug=debug)

		event = kwargs["event"]
		event_class = utils.classname(event)
		lomond_classes = ["Closed", "Closing", "Connected", "ConnectFail", "Connecting", "Disconnected",
			"Ping", "Poll", "Pong", "Ready", "Rejected", "Text", "UnknownMessage"]
		valid_classes = ["lomond.events.{}".format(c) for c in lomond_classes]

		if not event_class in valid_classes:
			logger.fatal("An invalid lomond event was passed. The object is of type \"{}\".".format(event_class))
			sys.exit()

		self.type = event.__class__.__name__
		self.time = now()

		if self.type == "Connecting":
			self.url = event.url
			self.body = "Connecting to {}".format(event.url)

		elif self.type == "ConnectFail":
			self.success = False
			self.reason = event.reason
			self.body = self.reason

		elif self.type == "Rejected":
			self.success = False
			self.response = event.response
			self.reason = event.reason
			self.body = self.reason

		elif self.type == "Connected":
			self.body = "Successfully connected"

		elif self.type == "Ready":
			self.response = event.response
			self.protocol = event.protocol
			self.extensions = event.extensions
			self.body = event.response

		if self.type == "Text":
			self.body = event.text

		elif self.type == "Disconnected":
			self.graceful = event.graceful
			self.success = self.graceful
			self.reason = event.reason
			if self.graceful == True:
				self.body = "The websocket disconnected gracefully."
			else:
				self.success = False
				self.body = "The websocket disconnected unexpectedly: {}".format(self.reason)

		elif self.type == "Closing":
			self.code = event.code
			self.reason = event.reason
			self.body = "The websocket is closing: {}".format(self.reason)

		elif self.type == "Closed":
			self.code = event.code
			self.reason = event.reason
			self.body = "The websocket closed: {}".format(self.reason)

		elif self.type == "Poll":
			self.body = "websocket poll."

		elif self.type == "Ping":
			self.data = event.data
			self.body = "websocket ping"

		elif self.type == "Pong":
			self.data = event.data
			self.body = "websocket pong"

class Response(object):
	def __init__(self, **kwargs):
		self.success = True
		global logger

		classname = utils.classname(self)
		debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		logger = utils.configure_logger(loggerid=classname, debug=debug)

		event = kwargs["event"]
		event_class = utils.classname(event)
		valid_classes = ["iris.events.Event"]

		if not event_class in valid_classes:
			logger.fatal("An invalid event was passed. The object is of type \"{}\".".format(event_class))
			sys.exit()

		self.event = event
		self.event_type = event.type
		self.success = self.event.success
		self.db_refresh_required = False
		self.time = now()

		dispatch = {
			"Closed": self.__process_closed_event,
			"Closing": self.__process_closing_event,
			"Connected": self.__process_connected_event,
			"ConnectFail": self.__process_connectfail_event,
			"Connecting": self.__process_connecting_event,
			"Disconnected": self.__process_dicsonnected_event,
			"Ping": self.__process_ping_event,
			"Poll": self.__process_poll_event,
			"Pong": self.__process_pong_event,
			"Ready": self.__process_ready_event,
			"Rejected": self.__process_rejected_event,
			"Text": self.__process_text_event,
			"UnknownMessage": self.__process_unknownmessage_event,
		}

		if event.type in dispatch:
			dispatch.get(event.type)()
		else:
			logger.debug("Unknown event type received: {}".format(event.type))

	def __process_closed_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_closing_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_connected_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_connectfail_event(self):
		logger.debug("in {}".format(whoami()))
		if self.success == False:
			self.errors = [self.event.body]
			# Need to kill the thread on dirty disconnect

	def __process_connecting_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_dicsonnected_event(self):
		logger.debug("in {}".format(whoami()))
		if self.success == False:
			self.errors = [self.event.body]
			# Need to kill the thread on dirty disconnect

	def __process_ping_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_poll_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_pong_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_ready_event(self):
		logger.debug("in {}".format(whoami()))

	def __process_rejected_event(self):
		logger.debug("in {}".format(whoami()))
		if self.success == False:
			self.errors = [self.event.body]
			#if self.event.response:
			if hasattr(self.event, "response"):
				print(999)
				self.errors.append("status={}".format(self.event.response.status))
			# handle response object
			# Need to kill the thread on dirty disconnect

	def __process_text_event(self):
		logger.debug("in {}".format(whoami()))

		def validate_schema(schema, event):
			logger.debug("beginning schema validation")
			if isinstance(schema, dict) and isinstance(event_object, dict):
				return all(k in event_object and self.__validate_schema(schema[k], event_object[k]) for k in schema)
			else:
				return isinstance(event_object, schema)

		schema = {"headers": dict, "payload": {"attributes": dict, "messageType": str}, "type": str}
		logger.debug("validating event body")
		event_body = utils.validate_json(self.event.body)

		if event_body:
			logger.debug("valid event body")

			self.type = event_body["type"]

			dispatch = {
				"Error": self.__error_handler,
				"base:ValueChange": self.__value_change_handler,
			}

			if self.success == False or self.type == "Error":
				self.__error_handler(event_body)
			elif self.type in dispatch:
				dispatch.get(self.type)(event_body)
			else:
				self.__event_handler(event_body)
		else:
			logger.fatal("Invalid JSON received from Iris.")
			sys.exit(1)

	def __process_unknownmessage_event(self):
		logger.debug("in {}".format(whoami()))

	def __error_handler(self, event_body):
		self.success = False
		logger.debug("in {}".format(whoami()))
		errors = []
		attributes = event_body["payload"]["attributes"]
		if "errors" in attributes and isinstance(attributes["errors"], list):
			errors = ["code: {}, message: {}".format(e["attributes"]["code"], e["attributes"]["message"]) for e in attributes["errors"]]
		elif "message" in attributes:
			errors = [attributes["message"]]

		if len(errors) > 0:
			self.errors = "; ".join(errors)
		else:
			self.errors = ["An unknown error has occurred."]

	def __value_change_handler(self, event_body):
		logger.debug("in {} for a {} event".format(whoami(), self.event_type))
		# Get device name from headers. Experimental.
		if "source" in event_body["headers"]:
			name = db.name_from_address(address=event_body["headers"]["source"])
			if name:
				event_body["headers"]["name"] = name

		# Deal with temperatures and F/C
		if "temp:temperature" in event_body["payload"]["attributes"]:
			temp = event_body["payload"]["attributes"]["temp:temperature"]
			if USE_FARENEHEIT == True:
				temp = utils.celsius_to_farenheit(temp)
			temp = "{0:.2f}".format(temp)
			event_body["payload"]["attributes"]["temp:temperature"] = temp

		# Create enhanced attributes to show the description of the attributes being changed.
		if "attributes" in event_body["payload"]:
			enhanced_attributes = {}
			for key, value in event_body["payload"]["attributes"].items():
				matches = re.match("^([^:]+):([^:]+)$", key)
				if matches:
					namespace = matches[1]
					attribute = matches[2]
					attribute_obj = db.fetch_attribute2(namespace=namespace, attribute=attribute)
					if attribute_obj:
						enhanced_attributes[key] = {
							"description": attribute_obj["description"],
							"new_value": value,
						}
					else:
						enhanced_attributes[key] = value
			event_body["payload"]["enhanced_attributes"] = enhanced_attributes

		# Look for device name changes and rey to rebuild device table as needed
		keys = [k for k, v in event_body["payload"]["attributes"].items()]
		db_change = ["dev:name", "person:firstName", "person:lastName", "rule:name", "scene:name"]
		intersections = list(set(keys).intersection(db_change))
		if len(intersections) > 0:
			self.db_refresh_required = True

		self.body = event_body

	def __event_handler(self, event_body):
		logger.debug("in {} for a {} event".format(whoami(), self.event_type))
		self.body = event_body

def whoami():
	return inspect.stack()[1][3]

def whosmydaddy():
	return inspect.stack()[2][3]

def now():
	return time.time()