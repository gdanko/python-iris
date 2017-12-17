import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.device import Device
from pprint import pprint

class SmokeCoDetector(Device):
	def __init__(self, **kwargs):
		Device.__init__(self, **kwargs)
		self.namespace = "smoke"
		self.device_type = "Smoke"

		module_capabilities = ["co", "smoke", "test"]
		capabilities = sorted(self.common_capabilities + module_capabilities)
		readable = utils.fetch_readable_attributes(self.iris.validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)
		methods = utils.fetch_methods(self.namespace, self.iris.validator)

		def generate_get_fn(namespace, attribute, obj):
			fn_name = "get_{}_{}".format(namespace, attribute)
			def fn(self, **kwargs):
				request.get_attributes(client=self, namespace=namespace, method=fn_name, attribute=attribute, settngs=obj, **kwargs)
			setattr(self.__class__, fn_name, fn)

		def generate_set_fn(namespace, attribute, obj):
			fn_name = "set_{}_{}".format(namespace, attribute)
			def fn(self, **kwargs):
				request.set_attributes(client=self, namespace=namespace, method=fn_name, attribute=attribute, settings=obj, **kwargs)
			setattr(self.__class__, fn_name, fn)

		def generate_method_fn(method, enabled, required, oneof, valid):
			if enabled == True:
				fn_name = method
				def fn(self, **kwargs):
					request.device_method_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
				setattr(self.__class__, fn_name, fn)

		if self.iris.validator[self.namespace]["is_device"] == True:
			for namespace in readable.keys():
				for attribute, obj in readable[namespace].items():
					generate_get_fn(namespace, attribute, obj)

			for namespace in writable.keys():
				for attribute, obj in writable[namespace].items():
					generate_set_fn(namespace, attribute, obj)

			for method_name, obj in methods.items():
				generate_method_fn(method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])
