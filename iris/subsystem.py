import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability
from pprint import pprint
import sys

class Subsystem(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

class Alarm(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subalarm"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Cameras(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subcameras"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Care(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subcare"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class CellBackup(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "cellbackup"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Climate(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subclimate"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class DoorsAndLocks(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subdoorsnlocks"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class LawnAndGarden(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "sublawnngarden"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class LightsAndSwitches(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "sublightsnswitches"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class PlaceMonitor(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subplacemonitor"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Presence(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subpres"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Safety(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subsafety"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Security(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subsecurity"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class SecurityAlarmMode(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subsecuritymode"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Water(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subwater"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Weather(Capability):
	def __init__(self, **kwargs):
		Subsystem.__init__(self, **kwargs)
		self.namespace = "subweather"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

def generate_method_fn(obj, method, required, oneof, valid):
	fn_name = method
	print(fn_name)
	def fn(self, **kwargs):
		request.subsystem_request(obj, client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
	setattr(obj, fn_name, fn)

def get_rwm(validator, capabilities):
	readable = utils.fetch_readable_attributes(validator, capabilities)
	writable = utils.fetch_writable_attributes(readable)
	methods = utils.fetch_methods(validator, capabilities)
	return readable, writable, methods