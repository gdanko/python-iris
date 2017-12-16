def set_active_place(place_id=None):
	return {
		"type": "sess:SetActivePlace",
		"headers": {
			"destination":"SERV:sess:",
			"correlationId": "78f7d29a-222e-4976-9d2b-d1f553cf8881",
			"isRequest" :True
		},
		"payload": {
			"messageType": "sess:SetActivePlace",
			"attributes": {
				"placeId": place_id
			}
		}
	}

def get_attributes(destination_address=None, namespace=None, key=None):
	return {
		"type": "base:GetAttributes",
		"headers": {
			"destination": destination_address,
			"correlationId": "74cb2fe5-3c80-4294-bf36-e6a6a5faf08a",
			"isRequest": True
		},
		"payload":{
			"messageType": "base:GetAttributes",
			"attributes": {
				namespace: key,
			}
		}
	}

def set_attributes(place_id: None, destination_address: None, namespace: None, key: None, value: None):
	return {
		"type": "base:SetAttributes",
		"headers": {
			"destination": destination_address,
			"correlationId": "790525f5-171f-4533-a952-0dcafb9b5310",
			"isRequest": True
		},
		"payload": {
			"messageType": "base:SetAttributes",
			"attributes": {
				"{}:{}".format(namespace, key): value
			}
		}
	}

def method(destination=None, namespace=None, method=None):
	return {
		"type": "{}:{}".format(namespace, method),
		"headers": {
			"destination": destination,
			"correlationId": "78cd5c7c-f5f7-4dba-9032-99ad183e64be",
			"isRequest": True
		},
		"payload": {
			"messageType": "{}:{}".format(namespace, method),
			"attributes": {}
		}
	}

def place(account_id=None, method=None):
	return {
		"type": "place:{}".format(method),
		"headers": {
			"destination": "SERV:place:{}".format(place_id),
			"correlationId": "79cd5c7c-f5f7-4dba-9032-99ad183e64be",
			"isRequest": True
		},
		"payload": {
			"messageType": "place:{}".format(method),
			"attributes": {}
		}
	}

def place(place_id=None, method=None):
	return {
		"type": "place:{}".format(method),
		"headers": {
			"destination": "SERV:place:{}".format(place_id),
			"correlationId": "79cd5c7c-f5f7-4dba-9032-99ad183e64be",
			"isRequest": True
		},
		"payload": {
			"messageType": "place:{}".format(method),
			"attributes": {}
		}
	}
