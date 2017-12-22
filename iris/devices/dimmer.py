import iris.utils as utils
from iris.capabilities.device import Device
import iris.request as request
from pprint import pprint

class Dimmer(Device):
	def __init__(self, iris):
		Device.__init__(self, iris)
		self.namespace = "dim"
		self.device_type = "Dimmer"

		module_capabilities = ["dim", "indicator", "swit"]
		capabilities = sorted(self.common_capabilities + module_capabilities)
		readable = utils.fetch_readable_attributes(self.validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)
		methods = utils.fetch_methods(self.validator, capabilities)

		def generate_method_fn(method, enabled, required, oneof, valid):
			if enabled == True:
				fn_name = method
				def fn(self, **kwargs):
					request.device_method_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
				setattr(self.__class__, fn_name, fn)

		if self.validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])
