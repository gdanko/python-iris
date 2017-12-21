import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.base.capability import Capability
from iris.core import Iris

class Device(Capability):
	def __init__(self, **kwargs):
		Capability.__init__(self, **kwargs)
		self.namespace = "device"
		self.common_capabilities = ["dev", "devadv", "devconn", "devpow"]
		from pprint import pprint
		pprint(self.websocket)
		print(1)

	def get_attribute(self, **kwargs):
		request.get_attributes(client=self, method="get_attribute", **kwargs)

	def set_attribute(self, **kwargs):
		request.set_attributes(client=self, method="set_attribute", **kwargs)


