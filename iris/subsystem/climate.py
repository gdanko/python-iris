import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability

class Climate(Capability):
	def __init__(self, **kwargs):
		Capability.__init__(self, **kwargs)
		self.namespace = "subclimate"

		capabilities = [self.namespace]
		readable = utils.fetch_readable_attributes(self.validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)
		methods = utils.fetch_methods(self.validator, capabilities)

		def generate_method_fn(method, required, oneof, valid):
			fn_name = method
			def fn(self, **kwargs):
				request.subsystem_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for method_name, obj in methods.items():
			generate_method_fn(method_name, obj["required"], obj["oneof"], obj["valid"])