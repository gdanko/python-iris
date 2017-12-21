from pprint import pprint
import iris.authenticator as authenticator
import iris.exception as exception
import iris.payloads as payloads
import iris.request as request
import iris.utils as utils
import sys
import websocket

class Iris(object):
	def __init__(self, **kwargs):
		global cookie
		global token

		self.success = None
		self.places = {}
		self.websocket_uri = "wss://bc.irisbylowes.com/websocket"

		if not "account" in kwargs:
			raise exception.MissingConstructorParameter(parameter="account")

		if "place_name" in kwargs:
			self.place_name = kwargs["place_name"]
		else:
			raise exception.MissingConstructorParameter(parameter="place_name")

		self.debug = kwargs["debug"] if ("debug" in kwargs and isinstance(kwargs["debug"], bool)) else False
		self.logger = utils.configure_logger(debug=self.debug)

		auth = authenticator.Authenticator(
			account=kwargs["account"],
			debug=self.debug
		)
		auth.authenticate()
		token = auth.token
		cookie = "irisAuthToken={}".format(token)
		self.init()

	def init(self, **kwargs):
		self.websocket = websocket.create_connection(
			self.websocket_uri,
			cookie=cookie
		)

		response = utils.validate_json(self.websocket.recv())
		request.validate_response(client=self, response=response)
		if self.success:
			places = [place for place in self.response["payload"]["attributes"]["places"] if place["placeName"] == self.place_name]
			if len(places) == 1:
				place = places[0]
				self.account_id = place["accountId"]
				self.account_address = "SERV:account:{}".format(self.account_id)
				self.place_id = place["placeId"]
				self.place_address = "SERV:place:{}".format(self.place_id)

				payload = payloads.set_active_place(place_id=self.place_id)
				request.send(client=self, payload=payload, debug=self.debug)
