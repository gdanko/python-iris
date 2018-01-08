import os
import sqlite3
import re
import sys
from pprint import pprint

# Create exceptions

def prepare_database():
	for table_name, table_cols in columns.items():
		drop = "DROP TABLE IF EXISTS {}".format(table_name)
		res = cursor.execute(drop)
		conn.commit()

		create = "CREATE TABLE {} ({})".format(table_name, ", ".join( [(k + " " + v) for k,v in table_cols.items()] ))
		res = cursor.execute(create)
		conn.commit()

def populate_places(places):
	for place in places:
		insert = "INSERT OR REPLACE INTO places (id,name,address,account_id) VALUES (?,?,?,?)"
		cursor.execute(insert, (
			place["base:id"],
			place["place:name"],
			place["base:address"],
			place["place:account"],
		))
		conn.commit()

def populate_devices(devices):
	for device in devices:
		insert = "INSERT OR REPLACE INTO devices (id,name,address,vendor,model,type,protocol,account_id,place_id) VALUES (?,?,?,?,?,?,?,?,?)"
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
		))
		conn.commit()

def populate_people(people):
	for person in people:
		name = "{} {}".format(person["person:firstName"], person["person:lastName"])
		insert = "INSERT OR REPLACE INTO people (id,name,address) VALUES (?,?,?)"
		cursor.execute(insert, (
			person["base:id"],
			name,
			person["base:address"],
		))
		conn.commit()

def populate_rules(rules):
	for rule in rules:
		insert = "INSERT OR REPLACE INTO rules (id,name,address) VALUES (?,?,?)"
		cursor.execute(insert, (
			rule["base:id"],
			rule["rule:name"],
			rule["base:address"],
		))
		conn.commit()

def populate_scenes(scenes):
	for scene in scenes:
		insert = "INSERT OR REPLACE INTO scenes (id,name,address) VALUES (?,?,?)"
		cursor.execute(insert, (
			scene["base:id"],
			scene["scene:name"],
			scene["base:address"],
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

def name_from_address(address=None):
	unions = ["SELECT name, address FROM {}".format(t) for t in columns.keys()]
	select = "SELECT * FROM ({}) WHERE address='{}'".format(" UNION ".join(unions), address)
	cursor.execute(select)
	result = cursor.fetchone()
	if result:
		if "name" in result:
			return result["name"]

	return None

def fetch_readable_attributes(directory, capabilities):
	readable = {
		"base": {
			"address": {
				"description": "Address of the device in the format DRIV::namespace::id.",
				"readonly": True,
				"required": True,
				"type": "string"
			},
			"id": {
				"description": "UUID of the device.",
				"readonly": True,
				"required": True,
				"type": "uuid"
			}
		}
	}
	select = "SELECT * FROM attributes WHERE directory='{}' AND namespace IN ({})".format(directory, quote_list(capabilities))
	res = cursor.execute(select)
	conn.commit()
	for row in res:
		namespace = row["namespace"]
		name = row["name"]
		if not namespace in readable:
			readable[namespace] = {}
		readable[namespace][name] = row
	return readable

def fetch_writable_attributes(directory, capabilities):
	writable = {}
	select = "SELECT * FROM attributes WHERE directory='{}' AND namespace IN ({}) AND writable=1".format(directory, quote_list(capabilities))
	res = cursor.execute(select)
	conn.commit()
	for row in res:
		namespace = row["namespace"]
		name = row["name"]
		if not namespace in writable:
			writable[namespace] = {}
		writable[namespace][name] = row
	return writable

def fetch_methods(directory, capabilities):
	methods = {}
	select = "SELECT * FROM methods WHERE directory='{}' AND namespace IN ({})".format(directory, quote_list(capabilities))
	res = cursor.execute(select)
	conn.commit()
	for row in res:
		namespace = row["namespace"]
		method = row["method"]
		if not namespace in methods:
			methods[namespace] = []
		if not method in methods[namespace]:
			methods[namespace].append(method)
	return methods

def fetch_method_parameters(directory, namespace, method):
	parameters = {}
	select = "SELECT method_parameters.* FROM methods JOIN method_parameters on methods.directory=method_parameters.directory AND methods.namespace=method_parameters.namespace AND methods.method=method_parameters.method WHERE methods.directory='{}' AND methods.namespace='{}' AND methods.method='{}' AND methods.enabled=1".format(directory, namespace, method)
	res = cursor.execute(select)
	conn.commit()
	for row in res:
		name = row["name"]
		parameters[name] = row

	return parameters

def fetch_attribute(directory, namespace, attribute):
	select = "SELECT * FROM attributes WHERE directory='{}' AND namespace='{}' AND name='{}'".format(directory, namespace, attribute)
	cursor.execute(select)
	result = cursor.fetchone()
	return result if result else None

# Fix this, it's ghetto
def fetch_attribute2(namespace, attribute):
	select = "SELECT * FROM attributes WHERE namespace='{}' AND name='{}'".format(namespace, attribute)
	cursor.execute(select)
	result = cursor.fetchone()
	return result if result else None

def _dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def quote_list(l):
	return ",".join(["\'{}\'".format(x) for x in l])

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
	},
	"places": {
		"id": "TEXT UNIQUE NOT NULL",
		"name": "TEXT NOT NULL",
		"address": "TEXT NOT NULL",
		"account_id": "TEXT NOT NULL",
	},
	"people": {
		"id": "TEXT UNIQUE NOT NULL",
		"name": "TEXT NOT NULL",
		"address": "TEXT NOT NULL",
	},
	"rules": {
		"id": "TEXT UNIQUE NOT NULL",
		"name": "TEXT NOT NULL",
		"address": "TEXT NOT NULL",
	},
	"scenes": {
		"id": "TEXT UNIQUE NOT NULL",
		"name": "TEXT NOT NULL",
		"address": "TEXT NOT NULL",
	},
}

dbfile = "{}/{}".format(os.path.expanduser("~"), ".iris.db")
conn = sqlite3.connect(dbfile, check_same_thread=False)
conn.row_factory = _dict_factory
cursor = conn.cursor()