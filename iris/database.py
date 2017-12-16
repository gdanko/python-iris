import os
from tinydb import TinyDB, Query
import re
import sys
from pprint import pprint

# Create exceptions

def configure_database():
	try:
		os.remove(dbfile)
	except:
		print("db file not found")

def populate_devices(devices=None):
	db = TinyDB(dbfile)
	table = db.table("devices")
	for device in devices:
		row = {}
		for key, value in device.items():
			key = key.replace(":", "_")
			row[key] = value
		table.insert(row)

def populate_people(people=None):
	db = TinyDB(dbfile)
	table = db.table("people")
	for person in people:
		person["person_name"] = "{} {}".format(person["person:firstName"], person["person:lastName"])
		row = {}
		for key, value in person.items():
			key = key.replace(":", "_")
			row[key] = value
		table.insert(row)

def populate_places(places=None):
	db = TinyDB(dbfile)
	table = db.table("places")
	for place in places:
		place["address"] = "SERV:place:{}".format(place["base:id"])
		row = {}
		for key, value in place.items():
			key = key.replace(":", "_")
			row[key] = value
		table.insert(row)

def find_device_address(name=None, id=None):
	table = db.table("devices")
	query = Query()
	res = None
	if name:
		res = table.search(query.dev_name == name)
	elif id:
		res = table.search(query.base_id == id)
	return res[0]["base_address"] if len(res) > 0 else None

def find_person_address(name=None, id=None):
	table = db.table("people")
	query = Query()
	res = None
	if name:
		res = table.search(query.person_name == name)
	elif id:
		res = table.search(query.base_id == id)
	return res[0]["base_address"] if len(res) > 0 else None

def find_place_address(name=None, id=None):
	table = db.table("places")
	query = Query()
	res = None
	if name:
		res = table.search(query.placeName == name)
	elif id:
		res = table.search(query.placeId == id)
	return res[0]["address"] if len(res) > 0 else None

def find_person_id(name=None):
	table = db.table("people")
	query = Query()
	res = None
	res = table.search(query.person_name == name)
	return res[0]["base_id"] if len(res) > 0 else None

def find_place_id(name=None):
	table = db.table("places")
	query = Query()
	res = None
	res = table.search(query.placeName == name)
	return res[0]["placeId"] if len(res) > 0 else None

dbfile = "{}/{}".format(os.path.expanduser("~"), ".iris.json")
db = TinyDB(dbfile)
