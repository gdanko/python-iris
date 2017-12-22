import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability

class Device(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.namespace = "device"
		self.common_capabilities = ["dev", "devadv", "devconn", "devpow"]

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)
