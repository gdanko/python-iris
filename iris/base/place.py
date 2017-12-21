import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.base.capability import Capability

from pprint import pprint

class Place(Capability):
	def __init__(self, **kwargs):
		Capability.__init__(self, **kwargs)
		self.namespace = "place"

		capabilities = [self.namespace]
		readable = utils.fetch_readable_attributes(self.iris.validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)
		methods = utils.fetch_methods(self.namespace, self.iris.validator)

		def generate_method_fn(method, required, oneof, valid):
			fn_name = method
			def fn(self, **kwargs):
				request.place_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for method_name, obj in methods.items():
			generate_method_fn(method_name, obj["required"], obj["oneof"], obj["valid"])

