#!/usr/bin/env python3

import sys
from iris.devices.dimmer import Dimmer
from iris.devices.doorlock import DoorLock

d1 = Dimmer(
	account="gd",
	place="My Home",
	debug=True,
)

d2 = DoorLock(
	account="gd",
	place="My Home",
	debug=True,
)