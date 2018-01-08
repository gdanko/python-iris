from distutils.version import LooseVersion, StrictVersion
from pprint import pprint
from uuid import UUID
import datetime
import inspect
import iris.database as db
import iris.exception as exception
import json
import logging
import os
import platform
import random
import re
import sys
import time
import uuid
import yaml

NEEDS_ADDRESS = ["device", "place", "person", "scene", "schedule", "rule"]

# Set up the logger
def configure_logger(loggerid=None, debug=False):
	if loggers.get(loggerid):
		return loggers.get(loggerid)
	else:
		level = logging.DEBUG if debug == True else logging.INFO

		logger = logging.getLogger(loggerid)
		handler = logging.StreamHandler()
		#formatter = logging.Formatter("%(levelname)s %(message)s")
		formatter = logging.Formatter("%(asctime)s.%(msecs)06d [%(levelname)s] %(message)s", "%s")
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		logger.setLevel(level)
		logger.propagate = False
		loggers[loggerid] = logger
	return logger

# Config file functions
def read_config(config_path=None):
	try:
		contents = open(config_path, "r").read()
		return contents
	except OSError as e:
		if e.errno == 2:
			raise exception.ConfigFileRead(path=config_path, message="No such file or directory")
		elif e.errno == 13:
			raise exception.ConfigFileRead(path=config_path, message="Permission denied")
		elif e.errno == 21:
			raise exception.ConfigFileRead(path=config_path, message="Is a directory")
		else:
			raise exception.ConfigFileRead(path=config_path, message=str(s))

def parse_config(account=None):
	config_path = "{}/.iris.yml".format(os.path.expanduser("~"))
	contents = open(config_path, "r").read()

	if len(contents) <= 0:
		raise exception.InvalidConfigFile(path=config_path, message="Zero-length file")

	config = validate_yaml(contents)
	if config:
		if not "accounts" in config:
			raise exception.InvalidConfigFile(path=config_path, message="Missing accounts section")
	else:
		raise exception.InvalidConfigFile(path=config_path, message="File contains invalid YAML")

	if account in config["accounts"]:
		if not "username" in config["accounts"][account]:
			raise exception.Invalidaccount(account=account, message="No username specified in the account")

		if not "password" in config["accounts"][account]:
			raise exception.Invalidaccount(account=account, message="No placeId specified in the password")

		return config
	else:
		raise exception.MissingAccount(account=account)

# Validators
def validate_yaml(string):
	if string:
		try:
			hash = yaml.load(string)
			return hash
		except:
			return None
	else:
		return None

def validate_json(string):
	if string:
		try:
			hash = json.loads(string)
			return hash
		except:
			return None
	else:
		return None

def is_uuid(string):
	if string:
		try:
			val = UUID(string, version=4)
			return True
		except:
			return False
	else:
		return False

# Conversion functions
def date_to_timestamp(date=None):
	try:
		return int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
	except:
		# create an exception
		raise(e)

def farenheit_to_celsius(temp):
	return (((temp - 32) * 5) / 9)

def celsius_to_farenheit(temp):
	return (((temp * 9) / 5) + 32)

# Miscellaneous functions
def now():
	return time.time()

def classname(c):
	try:
		module = c.__class__.__module__
		name = c.__class__.__name__
		return "{}.{}".format(module, name)
	except:
		print("need a 'not a class' exception")
		sys.exit(1)

def payload(namespace=None, method=None):
	return {
		"type": "{}:{}".format(namespace, method),
		"headers": {
			"correlationId": str(uuid.uuid4()),
			"isRequest": True,
		},
		"payload": {
			"attributes": {},
			"messageType": "{}:{}".format(namespace, method),
		}
	}

def generate_random(length=8):
	return "".join(random.choice("0123456789abcdef") for x in range(length))

def make_success(client=None, content_key=None, content=None, namespace=None, method=None):
	make_response(client=client, success=True, content_key=content_key, content=content, namespace=namespace, method=method)

def make_error(client=None, content_key=None, content=None, namespace=None, method=None):
	make_response(client=client, success=False, content_key=content_key, content=content, namespace=namespace, method=method)

def make_response(client=None, success=None, content_key=None, content=None, namespace=None, method=None):
	client.success = success
	status = "success" if success == True else "error"

	if content_key:	
		response = {"status": status, content_key: content}
	else:
		if content:
			if isinstance(content, dict):
				response = content
				response["status"] = status
			elif isinstance(content, list):
				response = {"status": status, "message": content}
			elif isinstance(content, str):
				response = {"status": status, "message": content}
		else:
			response = {"status": status, "message": "Unknown"}

	if namespace:
		response["namespace"] = namespace
	if method:
		response["method"] = method
	client.response = response

# Method and set/get attribute validation
# These will eventually be combined
def __missing_attributes_error(method, missing):
	return "the following required {0} parameters are missing: {1}".format(method, ", ".join(missing))

def __missing_optional_error(method, oneof):
	return "the {0} method requires one of the following parameters: {1}".format(method, ", ".join(oneof))

def __too_many_optional_error(method, oneof):
	return "the {0} method will accept only one of the following parameters: {1}".format(method, ", ".join(oneof))

def method_validator(client=None, **kwargs):
	# This is where it is tricky.
	# You cannot pass invalid attributes in the attributes block of the payload
	# but sometimes I need a device Id or person Id
	# I need to make sure only valid attributes go in the attributes block

	attribute = kwargs["attribute"] if "attribute" in kwargs else None
	directory = kwargs["directory"] if "directory" in kwargs else None
	method = kwargs["method"] if "method" in kwargs else None
	namespace = kwargs["namespace"] if "namespace" in kwargs else None
	errors = []

	params = db.fetch_method_parameters(directory, namespace, method)

	content = {
		"addresses": {},
		"attribute": attribute,
		"attributes": {},
		"method": method,
		"namespace": namespace,
	}

	if len(params.keys()) > 0:
		valid = {"params": params}
		required = [name for name, obj in valid["params"].items() if obj["required"] == 1]
		for name, obj in valid["params"].items():
			if obj["valid"] is not None:
				valid[name] = re.split("\s*,\s*", obj["valid"])
	else:
		# do this better
		client.success = True
		return content

	
	method = kwargs["method"] if "method" in kwargs else "unknown method"
	type_map = {"boolean": bool, "enum": str, "int": int, "string": str, "uuid": str, "double": float}

	filtered = {k: v for k, v in kwargs.items() if v is not None}
	kwargs.clear()
	kwargs.update(filtered)

	if isinstance(required, list) and len(required) > 0:
		missing = list( set(required) - set(kwargs.keys()) )
		if (len(missing) != 0):
			errors.append(__missing_attributes_error(method, missing))

		needs_address = {}
		keys = list(set(required).intersection(NEEDS_ADDRESS))
		for k in keys:
			needs_address[k] = kwargs[k]
			kwargs.pop(k)

	for param, obj in valid["params"].items():
		if param in kwargs and param in valid["params"]:
			required_type = obj["type"]
			if required_type in type_map:
				required_type = type_map[required_type]
			else:
				required_type = str

			#if not isinstance(kwargs[param], required_type):
			#	message = "The parameter {} is supposed to be of type {} but is actually of type {}".format(param, required_type, type(kwargs[param]))
			#	errors.append(message)

			if param in valid:
				lower = [e.lower() for e in valid[param]]
				if kwargs[param].lower() in lower:
					content["attributes"][param] = kwargs[param]
				else:
					errors.append("{0} is an invalid {1}. valid options for the \"{2}\" parameter are: {3}".format(kwargs[param], param, param, ", ".join(valid[param])))
			else:
				content["attributes"][param] = kwargs[param]

	get_addresses(content, needs_address, errors)

	# For functions that require a personId in the attributes
	if "personId" in content["attributes"]:
		if not is_uuid(content["attributes"]["personId"]):
			personId = db.find_id(table="people", name=content["attributes"]["personId"])

			if personId:
				content["attributes"]["personId"] = personId
			else:
				errors.append("The person with the name of {} was not found.".format(content["attributes"]["personId"]))

	# For functions that require a placeId in the attributes
	if "placeId" in content["attributes"]:
		if not is_uuid(content["attributes"]["placeId"]):
			placeId = db.find_place_id(table="places", name=content["attributes"]["placeId"])
			if placeId:
				content["attributes"]["placeId"] = placeId
			else:
				errors.append("The place with the name of {} was not found.".format(content["attributes"]["placeId"]))

	if len(errors) <= 0:
		make_success(client=client, content=content)
		return content
	else:
		make_error(client=client, content=errors)

def attribute_validator(client=None, **kwargs):
	attribute = kwargs["attribute"] if "attribute" in kwargs else None
	directory = kwargs["directory"] if "directory" in kwargs else None
	method = kwargs["method"] if "method" in kwargs else None
	namespace = kwargs["namespace"] if "namespace" in kwargs else None
	value = kwargs["value"] if "value" in kwargs else None
	errors = []

	content = {
		"addresses": {},
		"attribute": attribute,
		"method": method,
		"namespace": namespace,
	}

	required = ["attribute", "device", "namespace"]
	if method == "SetAttribute": required.append("value")

	if isinstance(required, list) and len(required) > 0:
		missing = list( set(required) - set(kwargs.keys()) )
		if (len(missing) != 0):
			errors.append(__missing_attributes_error(method, missing))

		needs_address = {}
		keys = list(set(required).intersection(NEEDS_ADDRESS))
		for k in keys:
			needs_address[k] = kwargs[k]
			kwargs.pop(k)

	for key, value in kwargs.items():
		if (key in required) and (key != "value"):
			content[key] = value

	attr = db.fetch_attribute(directory=directory, namespace=namespace, attribute=attribute)
	if attr:
		if method == "SetAttribute":
			if ("valid" in attr) and (attr["valid"]is not None):
				attr["valid"] = re.split("\s*,\s*", attr["valid"])
			
			if ("valid" in attr) and (isinstance(attr["valid"], list)):
				lower = [valid.lower() for valid in attr["valid"]]
				quoted = ["'{}'".format(valid) for valid in lower]
				if isinstance(value, str):
					value = value.lower()
				if not value in lower:
					errors.append("\"{}\" is an invalid valid for the \"{}\" attribute. Valid values are: {}.".format(value, attribute, ", ".join(quoted)))

			elif ("min" in attr) and ("max" in attr):
				floated = None
				try:
					floated = float(value)
					if (attr["min"] is not None) and (attr["max"] is not None):
						if float(value) < float(attr["min"]):
							errors.append("The value \"{}\" specified for the \"{}\" attribute is lower than the minimum allowed value of {}.".format(value, attribute, attr["min"]))
						if float(value) > float(attr["max"]):
							errors.append("The value \"{}\" specified for the \"{}\" attribute is higher than the maximum allowed value of {}.".format(value, attribute, attr["max"]))
				except ValueError:
					errors.append("The attribute \"{}\" expects a number. You supplied \"{}\".".format(attribute, value))

			content["value"] = value

	else:
		errors.append("The attribute \"{}\" does not exist in the namespace \"{}\".".format(attribute, namespace))

	get_addresses(content, needs_address, errors)

	if len(errors) <= 0:
		make_success(client=client, content=content)
		return content
	else:
		make_error(client=client, content=errors)

def get_addresses(content, needs_address, errors):
	tables = {"devices": "device", "places": "place", "people": "person", "rules": "rule", "scenes": "scene"}

	for table, key in tables.items():
		if key in needs_address:
			address = None
			if is_uuid(needs_address[key]):
				identifier_type = "UUID"
				address = db.find_address(table=table, id=needs_address[key])
			else:
				identifier_type = "name"
				address = db.find_address(table=table, name=needs_address[key])
			if address:
				content["addresses"][key] = address
			else:
				errors.append("The {} with the {} of {} was not found.".format(key, identifier_type, needs_address[key]))

def __check_python_version(req_version):
	cur_version = sys.version_info
	if cur_version <= req_version:
		logger.fatal("Your Python interpreter is too old. Please upgrade to {}.{} or greater.".format(req_version[0], req_version[1]))
		sys.exit(1)

def check_environment():
	__check_python_version((3, 0))

version = sys.version_info
major = version[0]
loggers = {}
logger = configure_logger(loggerid="logger-{}".format(generate_random(length=32)), debug=False)
