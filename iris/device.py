from iris.base import Capability
from pprint import pprint
import iris.database as db
import iris.request as request
import iris.utils as utils

class Device(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.classname = utils.classname(self)
		self.destination = {
			"namespace": "DRIV",
			"group": "dev",
			"id": None,
		}

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.device_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(obj, fn_name, fn)

		devices = {
			"iris.device.Camera": { "namespace": "camera", "capabilities": ["dim", "indicator", "swit"] },
			"iris.device.CameraPTZ": { "namespace": "cameraptz", "capabilities": ["camera", "camerastatus"] },
			"iris.device.Dimmer": { "namespace": "dim", "capabilities": ["dim", "indicator", "swit"] },
			"iris.device.DoorLock": { "namespace": "dim", "capabilities": ["doorlock"] },
			"iris.device.Motion": { "namespace": "dim", "capabilities": ["mot", "temp"] },
			"iris.device.Shade": { "namespace": "dim", "capabilities": ["shade"] },
			"iris.device.SmartPlug1G": { "namespace": "dim", "capabilities": ["ident", "pow", "swit"] },
			"iris.device.SmartPlug2G": { "namespace": "dim", "capabilities": ["centralitesmartplug", "devota", "ident", "pow", "swit"] },
			"iris.device.SmokeCoDetector": { "namespace": "dim", "capabilities": ["co", "smoke", "test"] },
			"iris.device.SmokeDetector": { "namespace": "dim", "capabilities": ["smoke", "test"] },
			"iris.device.Switch": { "namespace": "dim", "capabilities": ["indicator", "swit"] },
			"iris.device.Thermostat": { "namespace": "dim", "capabilities": ["clock", "humid", "indicator", "temp", "therm"] },
			"iris.device.Tilt": { "namespace": "dim", "capabilities": ["tilt"] },
			"iris.device.Valve": { "namespace": "dim", "capabilities": ["valv"] },
			"iris.device.Vent": { "namespace": "dim", "capabilities": ["vent"] },
			"iris.device.WaterSoftener": { "namespace": "dim", "capabilities": ["watersoftener"] },
			"iris.device.WeatherRadio": { "namespace": "dim", "capabilities": ["noaa"] },
		}
		namespace = devices[self.classname]["namespace"]
		common_capabilities = ["dev", "devadv", "devconn", "devpow"]
		module_capabilities = devices[self.classname]["capabilities"]
		capabilities = sorted(common_capabilities + module_capabilities)
		methods = db.fetch_methods("capability", capabilities)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, directory="capability", method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, directory="capability", method="SetAttribute", **kwargs)

class Camera(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class CameraPTZ(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Dimmer(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class DoorLock(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Motion(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Shade(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class SmartPlug1G(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class SmartPlug2G(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class SmokeCoDetector(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class SmokeDetector(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Switch(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Thermostat(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Tilt(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Valve(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class Vent(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class WaterSoftener(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)

class WeatherRadio(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)
