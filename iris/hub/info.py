import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
from iris.capabilities.capability import Capability

class HubInfo(Capability):
	def __init__(self, **kwargs):
		Capability.__init__(self, **kwargs)

		capabilities = ["hub", "hub4g", "hubadv", "hubalarm", "hubav", "hubbackup", "hubchime",
			"hubconn", "hubdebug", "hubhue", "hubdebug", "hubmetric", "hubnet", "hubpow",
			"hubrflx", "hubsercomm", "hubsounds", "hubvol", "hubzigbee", "hubzwave"]
		readable = utils.fetch_readable_attributes(self.iris.validator, capabilities)
		writable = utils.fetch_writable_attributes(readable)

		def generate_get_fn(attr_name, attr_namespace, attr_obj):
			fn_name = "get_{}_{}".format(attr_namespace, attr_name)
			print(fn_name)
			def fn(self, **kwargs):
				kwargs.update({"namespace": attr_namespace, "attribute": attr_name, "parameter_attributes": attr_obj})
				request.get_attributes(client=self, **kwargs)
			setattr(self.__class__, fn_name, fn)

		def generate_set_fn(attr_name, attr_namespace, attr_obj):
			fn_name = "set_{}_{}".format(attr_namespace, attr_name)
			def fn(self, **kwargs):
				kwargs.update({"namespace": attr_namespace, "attribute": attr_name, "parameter_attributes": attr_obj})
				request.set_attributes(client=self, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for attr_namespace in readable.keys():
			for attr_name, attr_obj in readable[attr_namespace].items():
				generate_get_fn(attr_name, attr_namespace, attr_obj)

		for attr_namespace in writable.keys():
			for attr_name, attr_obj in writable[attr_namespace].items():
				generate_set_fn(attr_name, attr_namespace, attr_obj)
