import inspect
import iris.database as db
import iris.payloads as payloads
import iris.utils as utils
import json
import os
import sys
from pprint import pprint

def get_attributes(client=None, **kwargs):
	kwargs.update({
		"required": ["device"],
		"oneof": [],
		"valid": {
			"params": {
				"device": {"type": "string"}
			}
		}
	})
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.get_attributes(
			destination=content["destination"],
			namespace=content["namespace"]
		)
		send(client=client, payload=payload, debug=client.iris.debug)
		if client.success:
			attribute = "{}:{}".format(content["namespace"], content["attribute"])
			if attribute in client.response["payload"]["attributes"]:
				response = {
					"name": client.response["payload"]["attributes"]["dev:name"],
					"address": client.response["payload"]["attributes"]["base:address"],
					"namespace": content["namespace"],
					"attribute": content["attribute"],
					"value": client.response["payload"]["attributes"][attribute]
				}
				utils.make_response(
					client=client,
					success=True,
					content=response
				)
			else:
				utils.make_response(
					client=client,
					success=False,
					content="Attribute {}:{} not found for device \"{}\".".format(content["namespace"], content["attribute"], kwargs["device"]),
				)

def set_attributes(client=None, **kwargs):
	kwargs.update({
		"required": ["device"],
		"oneof": [],
		"valid": {
			"params": {
				"device": {"type": "string"},
				"value": {"type": "string"},
			}
		}
	})
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.set_attributes(
			destination=content["destination"],
			namespace=content["namespace"],
			attribute=content["attribute"],
			value=content["attributes"]["value"],
		)
		pprint(payload)
		send(client=client, payload=payload, debug=client.iris.debug)
		print("")
		pprint(client.response)

def device_method_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=content["destination"],
			method=content["method"],
			namespace=content["namespace"]
		)
	for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
	send(client=client, method=content["method"], payload=payload, debug=client.iris.debug)

def account_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=client.iris.account_address,
			method=content["method"],
			namespace=content["namespace"]
		)
	for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
	send(client=client, method=content["method"], payload=payload, debug=client.iris.debug)

def place_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=client.iris.place_address,
			method=content["method"],
			namespace=content["namespace"]
		)
	for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
	send(client=client, method=content["method"], payload=payload, debug=client.iris.debug)

def hub_request(client=None, **kwargs):
	method = kwargs["method"]
	namespace = kwargs["namespace"]
	client.response = {}
	required, oneof, valid = utils.fetch_parameters(namespace, method, client.iris.validator)
	content = utils.method_validator(client=client, opts=kwargs, required=required, oneof=oneof, valid=valid)
	if isinstance(content, dict):
		payload = payloads.method(
			namespace=namespace,
			destination=client.iris.hub_address,
			method=method,
		)
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, payload=payload, debug=client.iris.debug)

def send(client=None, method=None, payload=None, debug=False):
	payload = json.dumps(payload)
	client.response = {}
	client.logger.debug("Executing method: {0}".format(method))
	client.logger.debug("Sending payload: {}".format(payload))
	client.ws.send(payload)
	response = utils.validate_json(client.ws.recv())

	if "Error" in response["type"]:
		errors = []
		if "payload" in response and "attributes" in response["payload"]:
			attributes = response["payload"]["attributes"]
			if "errors" in attributes and isinstance(attributes["errors"], list):
				errors = ["code: {}, message: {}".format(e["attributes"]["code"], e["attributes"]["message"]) for e in attributes["errors"]]
			elif "code" in attributes and "message" in attributes:
				errors.append("code: {}, message: {}".format(attributes["code"], attributes["message"]))
		
		if len(errors) > 0:
			message = "; ".join(errors)
		else:
			message = "The method {} failed with an unknown error.".format(method)

		utils.make_response(client=client, success=False, content_key="message", content=message)
	else:
		utils.make_response(client=client, success=True, content=response)
