from iris.base import Capability
import iris.database as db
import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
import sys

class Service(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.classname = utils.classname(self)

		def generate_method_fn(obj, directory, method):
			fn_name = method
			def fn(self, **kwargs):
				request.session_request(client=self, namespace=self.namespace, directory=directory,method=method, **kwargs)
			setattr(obj, fn_name, fn)

		capabilities = [self.namespace]
		readable = db.fetch_readable_attributes("service", capabilities)
		writable = db.fetch_writable_attributes("service", capabilities)
		methods = db.fetch_methods("service", capabilities)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "service", method_name)

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

class Account(Service):
	def __init__(self, init):
		self.namespace = "account"
		Service.__init__(self, init)

class Alarm(Service):
	def __init__(self, init):
		self.namespace = "alarm"
		Service.__init__(self, init)

class Bridge(Service):
	def __init__(self, init):
		self.namespace = "bridgesvc"
		Service.__init__(self, init)

class Device(Service):
	def __init__(self, init):
		self.namespace = "device"
		Service.__init__(self, init)

class EasCode(Service):
	def __init__(self, init):
		self.namespace = "eascode"
		Service.__init__(self, init)

class I18N(Service):
	def __init__(self, init):
		self.namespace = "i18n"
		Service.__init__(self, init)

class Invitation(Service):
	def __init__(self, init):
		self.namespace = "invite"
		Service.__init__(self, init)

class IPCD(Service):
	def __init__(self, init):
		self.namespace = "ipcd"
		Service.__init__(self, init)

class NwsSameCode(Service):
	def __init__(self, init):
		self.namespace = "nswsamecode"
		Service.__init__(self, init)

class Person(Service):
	def __init__(self, init):
		self.namespace = "person"
		Service.__init__(self, init)

class Place(Service):
	def __init__(self, init):
		self.namespace = "place"
		Service.__init__(self, init)

class ProductCatalog(Service):
	def __init__(self, init):
		self.namespace = "prodcat"
		Service.__init__(self, init)

class Rule(Service):
	def __init__(self, init):
		self.namespace = "rule"
		Service.__init__(self, init)

class Scene(Service):
	def __init__(self, init):
		self.namespace = "scene"
		Service.__init__(self, init)

class Scheduler(Service):
	def __init__(self, init):
		self.namespace = "scheduler"
		Service.__init__(self, init)

class Session(Service):
	def __init__(self, init):
		self.namespace = "sess"
		Service.__init__(self, init)

class Subsystem(Service):
	def __init__(self, init):
		self.namespace = "subs"
		Service.__init__(self, init)

class SupportSearch(Service):
	def __init__(self, init):
		self.namespace = "supportsearch"
		Service.__init__(self, init)

class SupportSession(Service):
	def __init__(self, init):
		self.namespace = "supcustsession"
		Service.__init__(self, init)

class Video(Service):
	def __init__(self, init):
		self.namespace = "video"
		Service.__init__(self, init)
