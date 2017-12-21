from iris.socket import Iris
from pprint import pprint
import iris.database as db
import iris.exception as exception
import iris.request as request
import iris.utils as utils
import json
import os
import sys

class Capability(object):
	def __init__(self, **kwargs):
		self.success = True
		self.response = {}
		self.classname = utils.classname(self)
		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.response = {"status": "success", "message": "Empty message"}
		self.logger = utils.configure_logger(debug=self.debug)

		if "account" in kwargs:
			self.account = kwargs["account"]
		else:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="account")

		if "place" in kwargs:
			self.place = kwargs["place"]
		else:
			raise exception.MissingConstructorParameter(classname=self.classname, parameter="place")

		self.iris = Iris(
			account=self.account,
			place_name=self.place
		)

		if utils.classname(self.iris.websocket) == "websocket._core.WebSocket":
			self.websocket = self.iris.websocket
		else:
			raise exception.NotAValidWebSocket(classname=self.classname, got=utils.classname(self.websockets[self.account][self.place]))

		pprint(self.websocket)
		#data = pkgutil.get_data("iris", "data/method-validator.json")
		#print(data)
		# This is a hack to get it to work until I can get python data to work
		pwd = os.path.dirname(os.path.realpath(__file__))
		path = "{}/../data/validator.json".format(pwd)
		self.validator = json.loads(open(path, "r").read())

		method_obj = self.validator["account"]["methods"]["ListPlaces"]
		request.account_request(
			client=self,
			namespace=self.namespace,
			method="ListPlaces",
			required=method_obj["required"],
			oneof=method_obj["oneof"],
			valid=method_obj["valid"],
			**kwargs
		)

