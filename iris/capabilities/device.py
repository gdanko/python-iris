import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability

class Device(Capability):
	def __init__(self, **kwargs):
		Capability.__init__(self, **kwargs)
		self.namespace = "device"
		self.common_capabilities = ["dev", "devadv", "devconn", "devpow"]

	def get_attribute(self, **kwargs):
		request.get_attributes(client=self, method="get_attribute", **kwargs)

	def set_attribute(self, **kwargs):
		request.set_attributes(client=self, method="set_attribute", **kwargs)