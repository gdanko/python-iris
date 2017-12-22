import iris.exception as exception
import iris.utils as utils
import json
import os

class Service(object):
	def __init__(self, iris):
		self.success = True
		self.response = {}
		self.classname = utils.classname(self)
		self.response = {"status": "success", "message": "Empty message"}

		if not iris:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="iris")

		#data = pkgutil.get_data("iris", "data/method-validator.json")
		#print(data)
		# This is a hack to get it to work until I can get python data to work
		pwd = os.path.dirname(os.path.realpath(__file__))
		path = "{}/../data/services.json".format(pwd)
		self.validator = json.loads(open(path, "r").read())


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
