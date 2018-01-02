from pprint import pprint, pformat
import inspect
import iris.database as db
import iris.payloads as payloads
import iris.utils as utils
import json
import os
import sys

def get_attributes(client=None, **kwargs):
	content = utils.attribute_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.get_attributes(
			destination=content["destination"],
			namespace=content["namespace"]
		)
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)
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
	content = utils.attribute_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.set_attributes(
			destination=content["destination"],
			namespace=content["namespace"],
			attribute=content["attribute"],
			value=content["value"].upper(),
		)
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

# Generic request for device methods
def device_method_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=content["destination"],
			method=content["method"],
			namespace=content["namespace"]
		)
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)


# Requests for account, place, prodcat, rule, scene, schedule
def account_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=client.iris.account_address,
			method=content["method"],
			namespace=content["namespace"]
		)
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def place_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=client.iris.place_address,
			method=content["method"],
			namespace=content["namespace"]
		)
		cid = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def prodcat_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.method(
			destination=client.iris.account_address,
			method=content["method"],
			namespace=content["namespace"]
		)
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def rule_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.rule(
			method=content["method"],
			namespace=content["namespace"]
		)
		payload["payload"]["attributes"]["placeId"] = client.iris.place_id
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

def scene_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.scene(
			method=content["method"],
			namespace=content["namespace"]
		)
		payload["payload"]["attributes"]["placeId"] = client.iris.place_id
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)


# Hub requests
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
		cid = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

# Service requests
def service_request(client=None, **kwargs):
	content = utils.method_validator(client=client, **kwargs)
	if client.success:
		payload = payloads.service(
			destination="SERV:{}:".format(kwargs["namespace"]),
			method=content["method"],
			namespace=content["namespace"]
		)
		payload["headers"]["correlationId"] = db.find_correlation_id(namespace=content["namespace"], method=content["method"])
		for k, v in content["attributes"].items(): payload["payload"]["attributes"][k] = v
		send(client=client, namespace=content["namespace"], method=content["method"], payload=payload, debug=client.debug)

# Generic send for all request methods and response validator
def send(client=None, namespace=None, method=None, payload=None, debug=False):
	client.logger.debug("Executing method: {0}".format(method))
	client.logger.debug("Sending payload: {}".format(pformat(payload)))
	payload = json.dumps(payload)
	client.method_ready.clear()

	client.websocket.send_text(payload)
	if client.method_ready.wait(5):
		validate_response(client=client, namespace=namespace, method=method, response=client.iris.response)

def validate_response(client=None, namespace=None, method=None, response=None):
	if "error" in response["type"].lower():
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

		utils.make_error(client=client, content_key="message", content=message, namespace=namespace, method=method)
	else:
		utils.make_success(client=client, content=response, namespace=namespace, method=method)
