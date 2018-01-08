from iris.base import Capability
from pprint import pprint
import iris.database as db
import iris.request as request
import iris.utils as utils

class Subsystem(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				self.__subsystem_request(directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(obj, fn_name, fn)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

	#def GetAttribute(self, **kwargs):
	#	request.get_attributes(client=self, method="GetAttribute", **kwargs)

	#def SetAttribute(self, **kwargs):
	#	request.set_attributes(client=self, method="SetAttribute", **kwargs)

	def __subsystem_request(self, **kwargs):
		content = utils.method_validator(client=self, **kwargs)
		if self.success:
			payload = self.__payload(
				method=content["method"],
				namespace=content["namespace"]
			)
			payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
			for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
			request.send(client=self, namespace=content["namespace"], method=content["method"], payload=payload, debug=self.debug)
		else:
			print(self.response)

	def __payload(self, namespace=None, method=None):
		return {
			"type": "{}:{}".format(namespace, method),
			"headers": {
				"destination": "SERV:{}:".format(namespace),
				"correlationId": "78f7d29a-222e-4976-9d2b-d1f553cf8881",
				"isRequest" :True
			},
			"payload": {
				"messageType":  "{}:{}".format(namespace, method),
				"attributes": {}
			}
		}

class Alarm(Capability):
	def __init__(self, iris):
		self.namespace = "subalarm"
		Subsystem.__init__(self, iris)

class Cameras(Capability):
	def __init__(self, iris):
		self.namespace = "subcameras"
		Subsystem.__init__(self, iris)

class Care(Capability):
	def __init__(self, iris):
		self.namespace = "subcare"
		Subsystem.__init__(self, iris)

class CellBackup(Capability):
	def __init__(self, iris):
		self.namespace = "cellbackup"
		Subsystem.__init__(self, iris)

class Climate(Capability):
	def __init__(self, iris):
		self.namespace = "subclimate"
		Subsystem.__init__(self, iris)

class DoorsAndLocks(Capability):
	def __init__(self, iris):
		self.namespace = "subdoorsnlocks"
		Subsystem.__init__(self, iris)

class LawnAndGarden(Capability):
	def __init__(self, iris):
		self.namespace = "sublawnngarden"
		Subsystem.__init__(self, iris)

class LightsAndSwitches(Capability):
	def __init__(self, iris):
		self.namespace = "sublightsnswitches"
		Subsystem.__init__(self, iris)

class PlaceMonitor(Capability):
	def __init__(self, iris):
		self.namespace = "subplacemonitor"
		Subsystem.__init__(self, iris)

class Presence(Capability):
	def __init__(self, iris):
		self.namespace = "subpres"
		Subsystem.__init__(self, iris)

class Safety(Capability):
	def __init__(self, iris):
		self.namespace = "subsafety"
		Subsystem.__init__(self, iris)

class Security(Capability):
	def __init__(self, iris):
		self.namespace = "subsecurity"
		Subsystem.__init__(self, iris)

class SecurityAlarmMode(Capability):
	def __init__(self, iris):
		self.namespace = "subsecuritymode"
		Subsystem.__init__(self, iris)

class Water(Capability):
	def __init__(self, iris):
		self.namespace = "subwater"
		Subsystem.__init__(self, iris)

class Weather(Capability):
	def __init__(self, iris):
		self.namespace = "subweather"
		Subsystem.__init__(self, iris)
