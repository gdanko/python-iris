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
import yaml

# Set up the logger
def configure_logger(loggerid=None, debug=False):
	if loggers.get(loggerid):
		return loggers.get(loggerid)
	else:
		level = logging.DEBUG if debug == True else logging.INFO

		logger = logging.getLogger(loggerid)
		handler = logging.StreamHandler()
		formatter = logging.Formatter("%(levelname)s %(message)s")
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
def classname(c):
	try:
		module = c.__class__.__module__
		name = c.__class__.__name__
		return "{}.{}".format(module, name)
	except:
		print("need a 'not a class' exception")
		sys.exit(1)

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
	directory = kwargs["directory"] if "directory" in kwargs else None
	method = kwargs["method"] if "method" in kwargs else None
	namespace = kwargs["namespace"] if "namespace" in kwargs else None
	attribute = kwargs["attribute"] if "attribute" in kwargs else None

	params = db.fetch_method_parameters(directory, namespace, method)

	content = {
		"attributes": {},
		"destination": None,
		"method": method,
		"namespace": namespace,
		"attribute": attribute,
	}
	if len(params.keys()) > 0:
		valid = {"params": params}
		required = [name for name, obj in valid["params"].items() if obj["required"] == 1]
		for name, obj in valid["params"].items():
			if obj["valid"] is not None:
				valid[name] = re.split("\s*,\s*", obj["valid"])
	else:
		return content

	errors = []
	method = kwargs["method"] if "method" in kwargs else "unknown method"
	type_map = {"boolean": bool, "enum": str, "int": int, "string": str, "uuid": str, "double": float}

	filtered = {k: v for k, v in kwargs.items() if v is not None}
	kwargs.clear()
	kwargs.update(filtered)

	if isinstance(required, list) and len(required) > 0:
		missing = list( set(required) - set(kwargs.keys()) )
		if (len(missing) != 0):
			errors.append(__missing_attributes_error(method, missing))

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

	get_destination(content, errors)

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

	# I'm not happy with this but for now it works.
	# It is only used for set attribute functions.
	if "settings" in kwargs:
		settings = kwargs["settings"]
		if "min" in settings and "max" in settings:
			if int(content["attributes"]["value"]) < int(settings["min"]):
				errors.append("The value \"{}\" specified for the \"{}\" attribute is lower than the minimum allowed value of {}.".format(content["attributes"]["value"], kwargs["attribute"], settings["min"]))
			if int(content["attributes"]["value"]) > int(settings["max"]):
				errors.append("The value \"{}\" specified for the \"{}\" attribute is higher than the maximum allowed value of {}.".format(content["attributes"]["value"], kwargs["attribute"], settings["max"]))

		elif "valid" in settings:
			lower = [e.lower() for e in settings["valid"]]
			if not str(content["attributes"]["value"]).lower() in lower:
				errors.append("\"{}\" is an invalid valid for the \"{}\" attribute. Valid values are: {}.".format(content["attributes"]["value"], kwargs["attribute"], ", ".join(settings["valid"])))
			else:
				content["value"] = block["value"]

	if len(errors) > 0:
		make_response(client=client, success=False, content="; ".join(errors))
	else:
		return content

def attribute_validator(client=None, **kwargs):
	attribute = kwargs["attribute"] if "attribute" in kwargs else None
	device = kwargs["device"] if "device" in kwargs else None
	directory = kwargs["directory"] if "directory" in kwargs else None
	method = kwargs["method"] if "method" in kwargs else None
	namespace = kwargs["namespace"] if "namespace" in kwargs else None
	value = kwargs["value"] if "value" in kwargs else None
	errors = []

	content = {
		"attribute": attribute,
		"destination": None,
		"method": method,
		"namespace": namespace,
	}

	required = ["attribute", "device", "namespace"]
	if method == "SetAttribute": required.append("value")

	if isinstance(required, list) and len(required) > 0:
		missing = list( set(required) - set(kwargs.keys()) )
		if (len(missing) != 0):
			errors.append(__missing_attributes_error(method, missing))

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
				if (attr["min"] is not None) and (attr["max"] is not None):
					if value < attr["min"]:
						errors.append("The value \"{}\" specified for the \"{}\" attribute is lower than the minimum allowed value of {}.".format(value, attribute, attr["min"]))
					if value > attr["max"]:
						errors.append("The value \"{}\" specified for the \"{}\" attribute is higher than the maximum allowed value of {}.".format(value, attribute, attr["max"]))

			content["value"] = value	

	else:
		errors.append("The attribute \"{}\" does not exist in the namespace \"{}\".".format(attribute, namespace))

	get_destination(content, errors)

	if len(errors) > 0:
		make_response(client=client, success=False, content="; ".join(errors))
	else:
		return content

def get_destination(content, errors):
	if "device" in content:
		device_address = None
		if is_uuid(content["device"]):
			identifier_type = "uuid"
			device_address = db.find_address(table="devices", id=content["device"])
		else:
			identifier_type = "name"
			device_address = db.find_address(table="devices", name=content["device"])

		if device_address:
			content["destination"] = device_address
		else:
			errors.append("The device with the {} of {} was not found.".format(identifier_type, content["device"]))

	if "person" in content:
		person_address = None
		if is_uuid(content["person"]):
			identifier_type = "uuid"
			person_address = db.find_address(table="people", id=content["person"])
		else:
			identifier_type = "name"
			person_address = db.find_address(table="people", name=content["person"])

		if person_address:
			content["destination"] = person_address
		else:
			errors.append("The person with the {} of {} was not found.".format(identifier_type, content["person"]))

	if "place" in content:
		place_address = None
		if is_uuid(content["place"]):
			identifier_type = "uuid"
			place_address = db.find_address(table="places", id=content["place"])
		else:
			identifier_type = "name"
			place_address = db.find_address(table="places", name=content["place"])

		if place_address:
			content["destination"] = place_address
		else:
			errors.append("The place with the {} of {} was not found.".format(identifier_type, content["place"]))

# Begin python-specific
def __check_python_version(req_version):
	cur_version = sys.version_info
	if cur_version <= req_version:
		logger.fatal("Your Python interpreter is too old. Please upgrade to {}.{} or greater.".format(req_version[0], req_version[1]))
		sys.exit(1)

def check_environment():
	__check_python_version((3, 0))
# End python-specific

version = sys.version_info
major = version[0]
loggers = {}
logger = configure_logger(loggerid="logger-{}".format(generate_random(length=32)), debug=False)
