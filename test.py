#!/usr/bin/env python3

import sys
from iris.core import Iris
from iris.capabilities.account import Account
from iris.capabilities.place import Place
from iris.hub.advanced import HubAdvanced
from iris.hub.alarm import HubAlarm
from iris.hub.base import Hub
from iris.hub.backup import HubBackup
from iris.hub.chime import HubChime
from iris.hub.connection import HubConnection
from iris.hub.debug import HubDebug
from iris.hub.hue import HubHue
from iris.hub.metrics import HubMetrics
from iris.hub.info import HubInfo
from iris.devices.doorlock import DoorLock
from iris.devices.dimmer import Dimmer
from iris.devices.switch import Switch
import iris.utils as utils
import iris.database as db
from tinydb import TinyDB, Query

from pprint import pprint

iris = Iris(
	account="account1",
	place_name="My Home",
	#debug=True
)

d = DoorLock(iris=iris)
d.AuthorizePerson(device="Garage Door", personId="Joe User")
pprint(d.response)
#d = Dimmer(iris=iris)
#s = Switch(iris=iris)

#a = Account(iris=iris)
#a.ListDevices()
#a.ListHubs()
#a.ListPlaces()
#a.ListInvoices()
#a.ListAdjustments()
#a.SignupTransition()
#a.UpdateBillingInfoCC()
#a.SkipPremiumTrial()
#a.CreateBillingAccount()
#a.AddPlace()
### a.Delete() ### UNTESTED
#a.DelinquentAccountEvent()
#a.IssueCredit(amountInCents='1')
#a.IssueInvoiceRefund()
#pprint(a.response)
# All account methods seem to be working

#p = Place(iris=iris)
#p.ListDevices()
#p.GetHub()
#p.StartAddingDevices()
#p.StopAddingDevices()
#p.RegisterHub()
#p.AddPerson()
#p.ListPersons()
#p.ListPersonsWithAccess()
#p.ListDashboardEntries()
#p.ListHistoryEntries()
### p.Delete() ### UNTESTED
#p.CreateInvitation()
#p.SendInvitation()
#p.PendingInvitations()
#p.CancelInvitation()
#p.UpdateAddress()
#p.RegisterHubV2()
#pprint(p.response)
# All place methods seem to be working

#h = Hub(iris=iris)
#h.PairingRequest(actionType="STOP_PAIRING", timeout='600')
#h.UnpairingRequest(actionType="START_UNPAIRING", timeout='10') # NullPointerException
#h.ListHubs() # Message type [hub:ListHubs] is not supported (this is in account)
#h.ResetLogLevels()
#h.SetLogLevel(level="info")
#h.GetLogs()
#h.StreamLogs()
#h.GetConfig()
#h.SetConfig()
### h.Delete() ### UNTESTED

#h = HubBackup(iris=iris)
#h.Backup(type="V2")
#h.Restore()
#h = HubChime(iris=iris)
#h.chime()

#h = HubInfo(iris=iris)
#h.get_hubzigbee_uptime()
#pprint(h.response)

# get attributes needs destination versus device name, etc
# generate a map fpr devices/ids/addresses and store it somehow so its global
# in fact, make a module for fetching these and core will populate it
# or even better, sqlite!
