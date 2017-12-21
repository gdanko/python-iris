import os
import sqlite3
import re
import sys
from pprint import pprint

# Create exceptions

def configure_database():
	columns = {
		"devices": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL",
			"vendor": "TEXT NOT NULL",
			"model": "TEXT NOT NULL",
			"type": "TEXT NOT NULL",
			"protocol": "TEXT NOT NULL"
		},
		"places": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL"
		},
		"people": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL"
		},
		"rules": {
			"id": "TEXT UNIQUE NOT NULL",
			"name": "TEXT NOT NULL",
			"address": "TEXT NOT NULL"
		},
	}
	for table_name, table_cols in columns.items():
		drop = "DROP TABLE IF EXISTS {}".format(table_name)
		res = cursor.execute(drop)
		conn.commit()

		create = "CREATE TABLE {} ({})".format(table_name, ", ".join( [(k + " " + v) for k,v in table_cols.items()] ))
		res = cursor.execute(create)
		conn.commit()

def populate_devices(devices=None):
	for device in devices:
		insert = "INSERT OR REPLACE INTO devices (id,name,address,vendor,model,type,protocol) VALUES (?,?,?,?,?,?,?)"
		cursor.execute(insert, (
			device["base:id"],
			device["dev:name"],
			device["base:address"],
			device["dev:vendor"],
			device["dev:model"],
			device["dev:devtypehint"],
			device["devadv:protocol"],
		))
		conn.commit()

def populate_people(people=None):
	for person in people:
		name = "{} {}".format(person["person:firstName"], person["person:lastName"])
		insert = "INSERT OR REPLACE INTO people (id,name,address) VALUES (?,?,?)"
		cursor.execute(insert, (
			person["base:id"],
			name,
			person["base:address"],
		))
		conn.commit()

def populate_places(places=None):
	for place in places:
		insert = "INSERT OR REPLACE INTO places (id,name,address) VALUES (?,?,?)"
		cursor.execute(insert, (
			place["base:id"],
			place["place:name"],
			place["base:address"]
		))
		conn.commit()

def populate_rules(rules=None):
	for rule in rules:
		insert = "INSERT OR REPLACE INTO rules (id,name,address) VALUES (?,?,?)"
		cursor.execute(insert, (
			rule["base:id"],
			rule["rule:name"],
			rule["base:address"]
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

def _dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

dbfile = "{}/{}".format(os.path.expanduser("~"), ".iris.db")
conn = sqlite3.connect(dbfile, check_same_thread=False)
conn.row_factory = _dict_factory
cursor = conn.cursor()