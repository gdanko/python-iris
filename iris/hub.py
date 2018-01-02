from iris.base import Capability
import iris.database as db
import iris.request as request
import iris.utils as utils

class Hub(Capability):
	def __init__(self, iris):
		Capability.__init__(self, iris)
		self.classname = utils.classname(self)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.hub_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(obj, fn_name, fn)

		common_capabilities = ["dev", "devadv", "devconn", "devpow"]
		module_capabilities = [self.namespace]
		capabilities = sorted(common_capabilities + module_capabilities)
		readable = db.fetch_readable_attributes("capability", capabilities)
		writable = db.fetch_writable_attributes("capability", capabilities)
		methods = db.fetch_methods("capability", capabilities)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

	def GetAttribute(self, **kwargs):
		request.get_attributes(client=self, method="GetAttribute", **kwargs)

	def SetAttribute(self, **kwargs):
		request.set_attributes(client=self, method="SetAttribute", **kwargs)

class Hub4G(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hub4g"
		Hub.__init__(self, **kwargs)

class Advanced(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubadv"
		Hub.__init__(self, **kwargs)

class Alarm(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubalarm"
		Hub.__init__(self, **kwargs)

class Backup(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubbackup"
		Hub.__init__(self, **kwargs)

class Base(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hub"
		Hub.__init__(self, **kwargs)

class Chime(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubchime"
		Hub.__init__(self, **kwargs)

class Connection(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubconn"
		Hub.__init__(self, **kwargs)

class Debug(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubdebug"
		Hub.__init__(self, **kwargs)

class Hue(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubhue"
		Hub.__init__(self, **kwargs)

class Metrics(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubmetric"
		Hub.__init__(self, **kwargs)

class Network(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubnet"
		Hub.__init__(self, **kwargs)

class Power(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubpow"
		Hub.__init__(self, **kwargs)

class Reflex(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubrflx"
		Hub.__init__(self, **kwargs)

class SerComm(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubsercomm"
		Hub.__init__(self, **kwargs)

class Sounds(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubsounds"
		Hub.__init__(self, **kwargs)

class Volume(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubvol"
		Hub.__init__(self, **kwargs)

class Zigbee(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubzigbee"
		Hub.__init__(self, **kwargs)

class Zwave(Capability):
	def __init__(self, **kwargs):
		self.namespace = "hubzwave"
		Hub.__init__(self, **kwargs)
