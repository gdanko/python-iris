from iris.base import Capability
import iris.database as db
import iris.request as request
import iris.utils as utils

class Service(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				self.__service_request(directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(obj, fn_name, fn)

		capabilities = [self.namespace]
		methods = db.fetch_methods("service", capabilities)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "service", namespace_name, method_name)

	#def GetAttribute(self, **kwargs):
	#	request.get_attributes(client=self, method="GetAttribute", **kwargs)

	#def SetAttribute(self, **kwargs):
	#	request.set_attributes(client=self, method="SetAttribute", **kwargs)

	def __service_request(self, **kwargs):
		content = utils.method_validator(client=self, **kwargs)
		if self.success:
			payload = self.__payload(
				method=content["method"],
				namespace=content["namespace"]
			)
			for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
			request.send(client=self, namespace=content["namespace"], method=content["method"], payload=payload, debug=self.debug)
		else:
			print(self.response)
	
	def __payload(self, namespace=None, method=None):
		return {
			"type": "{}:{}".format(namespace, method),
			"headers": {
				"destination": "SERV:{}:".format(namespace),
				"correlationId": db.find_correlation_id(namespace=namespace, method=method),
				"isRequest" :True
			},
			"payload": {
				"messageType":  "{}:{}".format(namespace, method),
				"attributes": {
					"placeId": self.iris.place_id
				}
			}
		}

class Account(Service):
	def __init__(self, iris):
		self.namespace = "account"
		Service.__init__(self, iris)

class Alarm(Service):
	def __init__(self, iris):
		self.namespace = "alarm"
		Service.__init__(self, iris)

class Bridge(Service):
	def __init__(self, iris):
		self.namespace = "bridgesvc"
		Service.__init__(self, iris)

class Device(Service):
	def __init__(self, iris):
		self.namespace = "device"
		Service.__init__(self, iris)

class EasCode(Service):
	def __init__(self, iris):
		self.namespace = "eascode"
		Service.__init__(self, iris)

class I18N(Service):
	def __init__(self, iris):
		self.namespace = "i18n"
		Service.__init__(self, iris)

class Invitation(Service):
	def __init__(self, iris):
		self.namespace = "invite"
		Service.__init__(self, iris)

class IPCD(Service):
	def __init__(self, iris):
		self.namespace = "ipcd"
		Service.__init__(self, iris)

class NwsSameCode(Service):
	def __init__(self, iris):
		self.namespace = "nswsamecode"
		Service.__init__(self, iris)

class Person(Service):
	def __init__(self, iris):
		self.namespace = "person"
		Service.__init__(self, iris)

class Place(Service):
	def __init__(self, iris):
		self.namespace = "place"
		Service.__init__(self, iris)

class ProductCatalog(Service):
	def __init__(self, iris):
		self.namespace = "prodcat"
		Service.__init__(self, iris)

class Rule(Service):
	def __init__(self, iris):
		self.namespace = "rule"
		Service.__init__(self, iris)

class Scene(Service):
	def __init__(self, iris):
		self.namespace = "scene"
		Service.__init__(self, iris)

#class Scheduler(Service):
#	def __init__(self, iris):
#		self.namespace = "scheduler"
#		Service.__init__(self, iris)

class Session(Service):
	def __init__(self, iris):
		self.namespace = "sess"
		Service.__init__(self, iris)

class Subsystem(Service):
	def __init__(self, iris):
		self.namespace = "subs"
		Service.__init__(self, iris)

class SupportSearch(Service):
	def __init__(self, iris):
		self.namespace = "supportsearch"
		Service.__init__(self, iris)

class SupportSession(Service):
	def __init__(self, iris):
		self.namespace = "supcustsession"
		Service.__init__(self, iris)

class Video(Service):
	def __init__(self, iris):
		self.namespace = "video"
		Service.__init__(self, iris)
