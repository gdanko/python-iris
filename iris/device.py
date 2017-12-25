import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability
from pprint import pprint

class Device(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.classname = utils.classname(self)

		def generate_method_fn(obj, method, enabled, required, oneof, valid):
			if enabled == True:
				fn_name = method
				def fn(self, **kwargs):
					pprint(fn_name)
					request.device_method_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
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
		readable = utils.fetch_readable_attributes(self.iris.capability_validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)
		methods = utils.fetch_methods(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

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
