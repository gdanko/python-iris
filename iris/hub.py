import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.base import Capability

class Hub(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.common_capabilities = ["dev", "devadv", "devconn", "devpow"]

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

class Hub4G(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hub4g"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Advanced(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubadv"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Alarm(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubalarm"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Backup(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubbackup"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Base(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hub"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Chime(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubchime"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Connection(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubconn"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Debug(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubdebug"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Hue(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubhue"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Info(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hub"

		capabilities = ["hub", "hub4g", "hubadv", "hubalarm", "hubav", "hubbackup", "hubchime",
			"hubconn", "hubdebug", "hubhue", "hubdebug", "hubmetric", "hubnet", "hubpow",
			"hubrflx", "hubsercomm", "hubsounds", "hubvol", "hubzigbee", "hubzwave"]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Metrics(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubmetric"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Network(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubnet"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Power(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubpow"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Reflex(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubrflx"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class SerComm(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubsercomm"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Sounds(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubsounds"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Volume(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubvol"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Zigbee(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubzigbee"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

class Zwave(Capability):
	def __init__(self, **kwargs):
		Hub.__init__(self, **kwargs)
		self.namespace = "hubzwave"

		capabilities = [self.namespace]
		readble, writable, methods = get_rwm(self.iris.capability_validator, capabilities)

		if self.iris.capability_validator[self.namespace]["is_device"] == True:
			for method_name, obj in methods.items():
				generate_method_fn(self.__class__, method_name, obj["enabled"], obj["required"], obj["oneof"], obj["valid"])

def generate_method_fn(obj, method, enabled, required, oneof, valid):
	if enabled == True:
		fn_name = method
		def fn(self, **kwargs):
			pprint(fn_name)
			request.hub_request(client=self, namespace=self.namespace, method=method, required=required, oneof=oneof, valid=valid, **kwargs)
		setattr(obj, fn_name, fn)

def get_rwm(validator, capabilities):
	readable = utils.fetch_readable_attributes(validator, capabilities)
	writable = utils.fetch_writable_attributes(readable)
	methods = utils.fetch_methods(validator, capabilities)
	return readable, writable, methods