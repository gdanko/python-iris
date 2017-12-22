#!/usr/bin/env python3

import sys
from iris.core import Iris
from iris.devices.dimmer import Dimmer
from pprint import pprint

iris = Iris(
	account="gd",
	place_name="My Home",
	debug=True
)

d = Dimmer(iris)
d.SetAttribute(device="Family Room Dimmer", namespace="dim", attribute="brightness", value=1)
pprint(d.response)

iris.stop()