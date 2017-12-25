import iris.exception as exception
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
			self.method_ready = self.iris.method_ready
		else:
			raise exception.NotAnIrisCoreObject(classname=self.classname, got=iris_type)
