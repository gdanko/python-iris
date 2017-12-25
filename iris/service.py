import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability
from pprint import pprint
import sys

class Service(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

class Account(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "account"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Alarm(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "alarm"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Bridge(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "bridgesvc"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Device(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "device"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class EasCode(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "eascode"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class I18N(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "i18n"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Invitation(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "invite"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class IPCD(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "ipcd"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class NwsSameCode(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "nswsamecode"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Person(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "person"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Place(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "place"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class ProductCatalog(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "prodcat"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Rule(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "rule"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Scene(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "scene"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Scheduler(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "scheduler"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Session(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "sess"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Subsystem(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "subs"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class SupportSearch(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "supportsearch"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class SupportSession(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "supcustsession"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

class Video(Service):
	def __init__(self, init):
		Service.__init__(self, init)
		self.namespace = "video"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.service_validator, capabilities)

		for method_name, obj in methods.items():
			generate_method_fn(self.__class__, method_name, obj["required"], obj["oneof"], obj["valid"])

def generate_method_fn(obj, method, required, oneof, valid):
	fn_name = method
	def fn(self, **kwargs):
		request.session_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
	setattr(obj, fn_name, fn)

def get_rwm(validator, capabilities):
	readable = utils.fetch_readable_attributes(validator, capabilities)
	writable = utils.fetch_writable_attributes(readable)
	methods = utils.fetch_methods(validator, capabilities)
	return readable, writable, methods