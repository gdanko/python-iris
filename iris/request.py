import inspect
import iris.payloads as payloads
import iris.utils as utils
import json
import os
import sys
from pprint import pprint

def get_attributes(client=None, **kwargs):
	client.success = None
	client.response = {"status": "success", "message": "Empty message"}
	oneof = [["device_name", "device_id"]]
	valid = {
		"params": {
			"device_name": {"type": "string"},
			"device_id": {"type": "uuid"},
			"namespace": {"type": "string"},
			"attribute": {"type": "string"},
		}
	}
	content = utils.process_parameters(client=client, opts=kwargs, oneof=oneof, valid=valid)
	if isinstance(content, dict):
		address = utils.get_address(client=client, type="device", name=content["device_name"])
		if address:
			payload = payloads.get_attributes(
				destination_address=address,
				namespace=content["namespace"],
			)
			send(client=client, payload=payload, debug=client.iris.debug)
			if client.success:
				attribute = "{}:{}".format(content["namespace"], content["attribute"])
				if attribute in client.response["payload"]["attributes"]:
					response = {
						"name": client.response["payload"]["attributes"]["dev:name"],
						"address": address,
						"namespace": content["namespace"],
						"attribute": content["attribute"],
						"value": client.response["payload"]["attributes"][attribute]
					}
					client.response = utils.make_response(
						client=client,
						success=True,
						content=response,
					)

def set_attributes(client=None, **kwargs):
	content = utils.validate_attributes(client=client, block=kwargs)
	if isinstance(content, dict):
		payload = payloads.set_device_attributes(
			place_id=client.iris.place_id,
			destination_address=content["destination_address"],
			namespace=content["namespace"],
			key=content["attribute"],
			value=content["value"]
		)
		send(client=client, payload=payload, debug=client.iris.debug)


def device_method_request(client=None, **kwargs):
	content = utils.process_attributes(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=content["destination"],
			method=content["method"],
			namespace=content["namespace"]
		)
	for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
	send(client=client, method=content["method"], payload=payload, debug=client.iris.debug)

def account_request(client=None, **kwargs):
	content = utils.process_attributes(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=client.iris.account_address,
			method=content["method"],
			namespace=content["namespace"]
		)
	for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
	send(client=client, method=content["method"], payload=payload, debug=client.iris.debug)

def place_request(client=None, **kwargs):
	content = utils.process_attributes(client=client, **kwargs)
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
	content = utils.process_parameters(client=client, opts=kwargs, required=required, oneof=oneof, valid=valid)
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
