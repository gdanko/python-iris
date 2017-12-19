import iris.utils as utils
from iris.capabilities.device import Device

class CameraPTZ(Device):
	def __init__(self, **kwargs):
		Device.__init__(self, **kwargs)
		self.namespace = "cameraptz"
		self.device_type = "CameraPTZ"

		module_capabilities = ["cameraptz"]
		capabilities = sorted(module_capabilities)
		readable = utils.fetch_readable_attributes(self.iris.validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)
		methods = utils.fetch_methods(self.namespace, self.iris.validator)

		def generate_method_fn(method, enabled, required, oneof, valid):
			if enabled == True:
				fn_name = method
				def fn(self, **kwargs):
					request.device_method_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
				setattr(self.__class__, fn_name, fn)

		if self.iris.validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])
