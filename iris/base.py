import iris.database as db
import iris.exception as exception
import iris.request as request
import iris.utils as utils

class Capability(object):
	def __init__(self, iris):
		self.success = True
		self.response = {}
		self.classname = utils.classname(self)
		self.response = {"status": "success", "message": "Empty message"}

		if not iris:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="iris")

		iris_type = utils.classname(iris)
		if iris_type == "iris.core.Iris":
			self.iris = iris
			self.websocket = self.iris.websocket
			self.logger = self.iris.logger
			self.debug = self.iris.debug
			self.websocket = self.iris.websocket
			self.event_ready = self.iris.event_ready
		else:
			raise exception.NotAnIrisCoreObject(classname=self.classname, got=iris_type)

class Account(Capability):
	def __init__(self, init):
		self.namespace = "account"
		Capability.__init__(self, init)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.account_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

class Place(Capability):
	def __init__(self, init):
		self.namespace = "place"
		Capability.__init__(self, init)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)


		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.place_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

class ProductCatalog(Capability):
	def __init__(self, init):
		self.namespace = "prodcat"
		Capability.__init__(self, init)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.prodcat_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

class Rule(Capability):
	def __init__(self, init):
		self.namespace = "rule"
		Capability.__init__(self, init)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.rule_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

class Scene(Capability):
	def __init__(self, init):
		self.namespace = "scene"
		Capability.__init__(self, init)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.scene_request(client=self, namespace=self.namespace, directory=directory,method=method, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)

class Schedule(Capability):
	def __init__(self, init):
		self.namespace = "schedule"
		Capability.__init__(self, init)

		capabilities = [self.namespace]
		methods = db.fetch_methods("capability", capabilities)

		def generate_method_fn(obj, directory, namespace, method):
			fn_name = method
			def fn(self, **kwargs):
				request.schedule_request(client=self, directory=directory, namespace=namespace, method=method, **kwargs)
			setattr(self.__class__, fn_name, fn)

		for namespace_name, namespace_obj in methods.items():
			for method_name in namespace_obj:
				generate_method_fn(self.__class__, "capability", namespace_name, method_name)
