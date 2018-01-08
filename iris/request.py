from pprint import pprint, pformat
import iris.database as db
import iris.exception as exception
import iris.utils as utils
import json
import os
import sys
import uuid

# #Valid destination
# namespace:group:id
# DRIV:dev:3347d9ec-0140-4957-a300-d2706eb9007d

# namespace::id
# DRIV::3347d9ec-0140-4957-a300-d2706eb9007d

# namespace:group:
# DRIV:dev:

## Type is in the form of namespace:method
# sess:SetActivePlaceResponse
# scene:Fire
#

def get_attributes(client=None, **kwargs):
	content = utils.attribute_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload("base", "GetAttributes")
		if "device" in content["addresses"]:
			payload["headers"]["destination"] = content["addresses"]["device"]
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)
		if client.success:
			attribute = "{}:{}".format(content["namespace"], content["attribute"])
			if attribute in client.iris.event_response.body["payload"]["attributes"]:
				client.iris.event_response.body["payload"]["attributes"] = {
					"dev:name": client.iris.event_response.body["payload"]["attributes"]["dev:name"],
					"base:address": client.iris.event_response.body["payload"]["attributes"]["base:address"],
					attribute: client.iris.event_response.body["payload"]["attributes"][attribute]
				}
				utils.make_success(client=client, content=client.iris.event_response.body)
			else:
				utils.make_error(client=client, content="Attribute {}:{} not found for device \"{}\".".format(content["namespace"], content["attribute"], kwargs["device"]),)

def set_attributes(client=None, **kwargs):
	content = utils.attribute_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload("base", "SetAttributes")
		if "device" in content["addresses"]:
			payload["headers"]["destination"] = content["addresses"]["device"]
		payload["payload"]["attributes"] = {
			"{}:{}".format(content["namespace"], content["attribute"]): content["value"]
		}
		#for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def account_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		payload["headers"]["destination"] = client.iris.account_address
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def device_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		if "device" in content["addresses"]:
			payload["headers"]["destination"] = content["addresses"]["device"]
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def hub_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		payload["headers"]["destination"] = client.iris.hub_address
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def place_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success: 
		payload = utils.payload(content["namespace"], content["method"])
		payload["headers"]["destination"] = client.iris.place_address
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def prodcat_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		payload["headers"]["destination"] = client.iris.place_address
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def rule_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		if "rule" in content["addresses"]:
			payload["headers"]["destination"] = content["addresses"]["rule"]
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def scene_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		if "scene" in content["addresses"]:
			payload["headers"]["destination"] = content["addresses"]["scene"]
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def schedule_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = utils.payload(content["namespace"], content["method"])
		if "schedule" in content["addresses"]:
			payload["headers"]["destination"] = content["addresses"]["schedule"]
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def send(client=None, namespace=None, method=None, payload=None, debug=False):
	#client.logger.debug("Websocket state: {}".format(pformat(client.websocket.state.__dict__)))
	client.logger.debug("Executing method {}".format(method))
	client.logger.debug("Sending payload: {}".format(pformat(payload)))
	payload = json.dumps(payload)
	client.event_ready.clear()
	client.websocket.send_text(payload)
	if client.event_ready.wait(10):
		if client.iris.event_response.success == True:
			utils.make_success(client=client, content=client.iris.event_response.body)
		else:
			utils.make_error(client=client, content=client.iris.event_response.errors)
