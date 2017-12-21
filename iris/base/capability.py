import iris.exception as exception
import iris.utils as utils
from iris.websocket import WebSocket
from pprint import pprint

class Capability(object):
	def __init__(self, **kwargs):
		self.success = True
		self.response = {}
		self.classname = utils.classname(self)
		self.response = {"status": "success", "message": "Empty message"}

		ws = WebSocket(
			account="gd",
			place_name="My Home",
			#debug=True
		)
		self.websocket = ws.websocket
		pprint(self.websocket)
		print(0)

		if "account" in kwargs:
			self.account = kwargs["account"]
		else:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="account")

		if "place" in kwargs:
			self.place = kwargs["place"]
		else:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="place")


		#iris_type = utils.classname(self.iris)
		#if iris_type == "iris.core.Iris":
		#	self.ws = self.iris.ws
		#	self.logger = self.iris.logger
		#else:
		#	raise exception.NotAnIrisCoreObject(classname=self.classname, got=iris_type)
