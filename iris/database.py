import os
import sqlite3
import re
import sys
from pprint import pprint

# Create exceptions

def prepare_database():
	columns = {
		"devices": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL",
			"vendor": "TEXT NOT NULL",
			"model": "TEXT NOT NULL",
			"type": "TEXT NOT NULL",
			"protocol": "TEXT NOT NULL",
			"account_id": "TEXT NOT NULL",
			"place_id": "TEXT NOT NULL",
			"capabilities": "TEXT NOT NULL",
		},
		"places": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL",
			"account_id": "TEXT NOT NULL",
			"capabilities": "TEXT NOT NULL",
		},
		"people": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL",
			"capabilities": "TEXT NOT NULL",
		},
		"rules": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL",
			"capabilities": "TEXT NOT NULL",
		},
		"scenes": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL",
			"capabilities": "TEXT NOT NULL",
		},
		"correlation": {
			"id": "TEXT UNIQUE NOT NULL",
			"namespace": "TEXT NOT NULL",
			"method": "TEXT NOT NULL",
		},
	}
	for table_name, table_cols in columns.items():
		drop = "DROP TABLE IF EXISTS {}".format(table_name)
		res = cursor.execute(drop)
		conn.commit()

		create = "CREATE TABLE {} ({})".format(table_name, ", ".join( [(k + " " + v) for k,v in table_cols.items()] ))
		res = cursor.execute(create)
		conn.commit()

def populate_devices(devices):
	for device in devices:
		insert = "INSERT OR REPLACE INTO devices (id,name,address,vendor,model,type,protocol,account_id,place_id,capabilities) VALUES (?,?,?,?,?,?,?,?,?,?)"
		cursor.execute(insert, (
			device["base:id"],
			device["dev:name"],
			device["base:address"],
			device["dev:vendor"],
			device["dev:model"],
			device["dev:devtypehint"],
			device["devadv:protocol"],
			device["dev:account"],
			device["dev:place"],
			",".join([c for c in device["base:caps"] if c != "base"]),
		))
		conn.commit()

def populate_people(people):
	for person in people:
		name = "{} {}".format(person["person:firstName"], person["person:lastName"])
		insert = "INSERT OR REPLACE INTO people (id,name,address,capabilities) VALUES (?,?,?,?)"
		cursor.execute(insert, (
			person["base:id"],
			name,
			person["base:address"],
			",".join([c for c in person["base:caps"] if c != "base"]),
		))
		conn.commit()

def populate_places(places):
	for place in places:
		insert = "INSERT OR REPLACE INTO places (id,name,address,account_id,capabilities) VALUES (?,?,?,?,?)"
		cursor.execute(insert, (
			place["base:id"],
			place["place:name"],
			place["base:address"],
			place["place:account"],
			",".join([c for c in place["base:caps"] if c != "base"]),
		))
		conn.commit()

def populate_rules(rules):
	for rule in rules:
		insert = "INSERT OR REPLACE INTO rules (id,name,address,capabilities) VALUES (?,?,?,?)"
		cursor.execute(insert, (
			rule["base:id"],
			rule["rule:name"],
			rule["base:address"],
			",".join([c for c in rule["base:caps"] if c != "base"]),
		))
		conn.commit()

def populate_scenes(scenes):
	for scene in scenes:
		insert = "INSERT OR REPLACE INTO scenes (id,name,address,capabilities) VALUES (?,?,?,?)"
		cursor.execute(insert, (
			scene["base:id"],
			scene["scene:name"],
			scene["base:address"],
			",".join([c for c in scene["base:caps"] if c != "base"]),
		))
		conn.commit()

def populate_capabilities(validator):
	for namespace, namespace_obj in validator.items():
		if ("methods" in namespace_obj) and (len(namespace_obj["methods"]) > 0):
			for method_name, method_obj in namespace_obj["methods"].items():
				insert = "INSERT OR REPLACE INTO correlation (id, namespace, method) VALUES (?,?,?)"
				cursor.execute(insert, (
					method_obj["correlation_id"],
					namespace,
					method_name
				))
				conn.commit()

def populate_services(validator):
	for namespace, namespace_obj in validator.items():
		if ("methods" in namespace_obj) and (len(namespace_obj["methods"]) > 0):
			for method_name, method_obj in namespace_obj["methods"].items():
				insert = "INSERT OR REPLACE INTO correlation (id, namespace, method) VALUES (?,?,?)"
				cursor.execute(insert, (
					method_obj["correlation_id"],
					namespace,
					method_name
				))
				conn.commit()

def find_address(table=None, name=None, id=None):
	selector = None
	selected = None
	if name:
		selector = "name"
		selected = name
	elif id:
		selector = "id"
		selected = id
	select = "SELECT address FROM {} WHERE {}='{}'".format(table, selector, selected)
	cursor.execute(select)
	result = cursor.fetchone()
	return result["address"] if ((result) and ("address" in result)) else None

def find_id(table=None, name=None):
	select = "SELECT id FROM {} WHERE name='{}'".format(table, name)
	cursor.execute(select)
	result = cursor.fetchone()
	return result["id"] if ((result) and ("id" in result)) else None

def find_correlation_id(namespace=None, method=None):
	select = "SELECT id FROM correlation WHERE namespace='{}' AND method='{}'".format(namespace, method)
	cursor.execute(select)
	result = cursor.fetchone()
	return result["id"] if ((result) and ("id" in result)) else None	

def namespace_and_method_from_cid(cid=None):
	select = "SELECT namespace,method FROM correlation WHERE id='{}'".format(cid)
	cursor.execute(select)
	result = cursor.fetchone()
	if result:
		if ("namespace" in result) and ("method" in result):
			return result["namespace"], result["method"]
	
	return None, None

def _dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

dbfile = "{}/{}".format(os.path.expanduser("~"), ".iris.db")
conn = sqlite3.connect(dbfile, check_same_thread=False)
conn.row_factory = _dict_factory
cursor = conn.cursor()