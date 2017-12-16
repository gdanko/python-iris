import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.device import Device
from pprint import pprint

class Dimmer(Device):
	def __init__(self, **kwargs):
		Device.__init__(self, **kwargs)
		self.namespace = "Dimmer"
		self.device_type = "Dimmer"

		devices = [item for item in self.iris.devices if item["dev:devtypehint"] == self.device_type]
		pprint(devices)