import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.device import Device
from pprint import pprint

class Switch(Device):
	def __init__(self, **kwargs):
		Device.__init__(self, **kwargs)
		self.namespace = "swit"
		self.device_type = "Switch"

		devices = [item for item in self.iris.devices if item["dev:devtypehint"] == self.device_type]
		#pprint(devices)