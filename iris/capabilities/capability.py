import iris.exception as exception
import iris.utils as utils

class Capability(object):
	def __init__(self, **kwargs):
		self.success = True
		self.response = {}
		self.classname = utils.classname(self)
		self.response = {"status": "success", "message": "Empty message"}

		if "iris" in kwargs:
			self.iris = kwargs["iris"]
		else:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="iris")

		iris_type = utils.classname(self.iris)
		if iris_type == "iris.core.Iris":
			self.ws = self.iris.ws
			self.logger = self.iris.logger
		else:
			raise exception.NotAnIrisCoreObject(classname=self.classname, got=iris_type)
