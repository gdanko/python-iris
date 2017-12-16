import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.device import Device
from pprint import pprint

class DoorLock(Device):
	def __init__(self, **kwargs):
		Device.__init__(self, **kwargs)
		self.namespace = "doorlock"
		self.device_type = "Lock"

		methods = utils.fetch_methods(self.namespace, self.iris.validator)

		def generate_method_fn(method, enabled, required, oneof, valid):
			if enabled == True:
				fn_name = method
				def fn(self, **kwargs):
					request.device_method_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
				setattr(self.__class__, fn_name, fn)

		for method_name, obj in methods.items():
			generate_method_fn(method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])		