from iris.base import Capability
import iris.database as db
import iris.request as request
import iris.utils as utils

class Hub(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.classname = utils.classname(self)
		self.success = None

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.hub_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(obj, fn_name, fn)

		common_capabilities = ["dev", "devadv", "devconn", "devpow"]
		module_capabilities = [self.namespace]
		capabilities = sorted(common_capabilities + module_capabilities)
		methods = db.fetch_methods("capability", capabilities)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

class Hub4G(Capability):
	def __init__(self, iris):
		self.namespace = "hub4g"
		Hub.__init__(self, iris)

class Advanced(Capability):
	def __init__(self, iris):
		self.namespace = "hubadv"
		Hub.__init__(self, iris)

class Alarm(Capability):
	def __init__(self, iris):
		self.namespace = "hubalarm"
		Hub.__init__(self, iris)

class Backup(Capability):
	def __init__(self, iris):
		self.namespace = "hubbackup"
		Hub.__init__(self, iris)

class Base(Capability):
	def __init__(self, iris):
		self.namespace = "hub"
		Hub.__init__(self, iris)

class Chime(Capability):
	def __init__(self, iris):
		self.namespace = "hubchime"
		Hub.__init__(self, iris)
		#super().__init__(iris)

class Connection(Capability):
	def __init__(self, iris):
		self.namespace = "hubconn"
		Hub.__init__(self, iris)

class Debug(Capability):
	def __init__(self, iris):
		self.namespace = "hubdebug"
		Hub.__init__(self, iris)

class Hue(Capability):
	def __init__(self, iris):
		self.namespace = "hubhue"
		Hub.__init__(self, iris)

class Metrics(Capability):
	def __init__(self, iris):
		self.namespace = "hubmetric"
		Hub.__init__(self, iris)

class Network(Capability):
	def __init__(self, iris):
		self.namespace = "hubnet"
		Hub.__init__(self, iris)

class Power(Capability):
	def __init__(self, iris):
		self.namespace = "hubpow"
		Hub.__init__(self, iris)

class Reflex(Capability):
	def __init__(self, iris):
		self.namespace = "hubrflx"
		Hub.__init__(self, iris)

class SerComm(Capability):
	def __init__(self, iris):
		self.namespace = "hubsercomm"
		Hub.__init__(self, iris)

class Sounds(Capability):
	def __init__(self, iris):
		self.namespace = "hubsounds"
		Hub.__init__(self, iris)

class Volume(Capability):
	def __init__(self, iris):
		self.namespace = "hubvol"
		Hub.__init__(self, iris)

class Zigbee(Capability):
	def __init__(self, iris):
		self.namespace = "hubzigbee"
		Hub.__init__(self, iris)

class Zwave(Capability):
	def __init__(self, iris):
		self.namespace = "hubzwave"
		Hub.__init__(self, iris)
