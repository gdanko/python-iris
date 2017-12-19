python-iris
===================

python-iris provides a Python interface to the second generation Iris by Lowe's API.

## Requirements
* Python 3.4 or greater
* websocket-client 0.44.0 or greater

## Authentication
The 2nd generation Iris API communicates via websocket. To authenticate you first need to login to the login page with your account credentials. A `Set-Cookie` header is returned with an authentication token. When creating the websocket, this token is passed as a request cookie, at which point you are authenticated. To avoid unnecessary hits to the login server I cache the token (cookie expiration date - 1 hour). When you create an instance of the Iris object all of these things are checked and a new token is requested only when needed.

## How it Works on the Back End
The API is completely undocumented but I was able to get some basic hints from the gentleman who runs https://iriswebportal.com. I have spent a lot of time in the WebKit Inspector, examining the websocket's requests and response and understanding how to make various requests. A lot of trial and error went into this as well.

## The Configuration File
Sorry Windows people, I write and test on a Unix system. The configuration file is a hidden "dot" file at `~/.iris.yml`. When you first create it, it looks like this:
```
accounts:
  account1:
    password: xxxxx
    username: xxxxx
```
After you have logged in it will look like this:
```
accounts:
  account1:
    password: xxxxx
    timestamp: 1513719482
    token: xxxxx
    username: xxxxx
```
The timestamp determines when a new token will be generated.

## The Core Iris Object
The center of python-iris is the Core Iris object. When a new instance is created a few things happen.
* Authentication happens
* The websocket object is created
* A connection is made to the websocket

After successful login occurs a few more things happen
* The SQLite database is initialized
* The following tables are populated: places, devices, people, rules, and scenes.

The purpose of putting everything into SQLite is for translating names to IDs or addresses. When a request is made for a device, you need to specify the device's "base address" which is a cryptic string which includes the device's UUID. WIth the database you can specify the name of the device and the database module will fetch the required information.

## Device Objects
This is where it got really tricky. The Iris API has a concept of capabilities. A device's capabilities is stored in its attribute list as a list (array for you non-Python people). From what I have been able to determine, all devices share the following common capabilites:
* dev - device base
* devadv - device advanced
* devconn - device connection
* devpow - device power

But to better illustrate this concept, a simple lightswitch will add the following:
* swit - switch

And a dimmer switch will go a step further. It will have `swit` and will add `dim` which is used for dimmers.

Device objects can have methods and/or attributes. I am still finding a bit of overlap between methods and attributes but I will leave it be for now.

## Device Attributes
Each capability will have its own set of attributes and/or methods. Some attributes are read-only and some are read-write. For that reason I dynamically generate `get_*` or `set_*` methods for each attribute, depending on its writability. The methods are named `get_<namespace>_<attribute>` or `set_<namespace>_<attribute>`. Each capability has its own "namespace" and that is where the nomanclature comes from. For example, if you have a instance of the dimmer module, you will have available a method called `set_dim_brightness` which will set the brightness of your dimmer from 0-100. To confuse things futher, it will also have a method called `RampBrightness` which takes two parameters, `brightness` and `seconds`. You effectively have two ways of doing the same thing, except that the latter will ramp it up slowly.

## Using a Device Module
To use a device module you first need to create the Core Iris object. You then create the device module object and pass it the Iris object in its constructor like so:
```
from iris.core import Iris
from iris.devices.doorlock import DoorLock
from pprint import pprint as pp

d = DoorLock(iris=iris)
d.AuthorizePerson(device="Door1", person="John Doe"
pp(d.response)
```
This small script will authorize John Doe's PIN on Door1. Now you can also see where the database comes into play. One thing to note, there is logic speficied to determine if `device` is a device ID (UUID) or a name. It intelligently determines the correct base ID for the device, person, place, rule, or scene.

## The Response and Success Objects
All "things" are derived from `iris.capability.Capability`. This class contains response and success objects. Explaing this warrants a deeper explanation about how things work.

When a method is called in a device object, it gets passed to `iris.request.device_method_request`. Every method has a list of both required and valid parameters. `iris.request.device_method_request` passes the request and all of its parameters to `iris.utils.method_validator`. If the validator determines that something is wrong, it calls `iris.utils.make_response` to generate the client's response object. The client's success flag is set accordingly. Now if the validator passes, its output is sent to `iris.payloads` to generate the payload required for the specified method. Once the payload has been properly generated, it is passed to `iris.request.send` where it is sent to the websocket. The send function parses the output and calls `iris.utils.make_response` to generate the response and success objects.

## More on Dynamically Generated Methods
As stated before, because there are so many possible attributes it would be difficult to create a method for each. As a result I am generating the methods dynamically. I know this is bad Python and in the near future I will most likely create `get_attribute` and `set_attribute` methods in the base device class. Regardless of how I approach it, it needs to be mentioned that the "source of truth" comes from a JSON file that lives within the package. It has information about every capability and method and attribute within. This is `iris.utils.method_validator` is able to determine if invalid parameters are passed to a method.

## What's Next?
I have a lot of work to do in understanding the relationship between things like subsystems and whatnot. I also want to clean up the parameter validation and support more devices.

## Thanks
Many thanks to thegillion from over at the Iris Community. He was instrumental in making all of this happen and continues to assist and contribute to the project. If you find this utility useful in any way, please find him over at the community site, get his PayPal address, and buy him a six pack.

## How You Can Help
There are many devices that I do not have so building for them can be tricky since I've no way to test. The devices I currently own are:
* First generation motion sensors
* First generation contact sensors (LOTS OF THESE)
* Schlage level locks
* Kwikset deadbolts
* First Alert smoke/CO detectors
* First generation NYCE tilt sensor
* RCOA CT101 thermostats
* First and second generation Iris contact sensors
* GE dimmer switch
* GE 3 way light switches with the add-ons
* First generation KeyFob
* NYCE door hinge sensors

If you have devices not on this list, please try the following script and send the output to gdanko@gmail.com.
```
#!/usr/bin/env python3

from iris.core import Iris
from pprint import pprint

iris = Iris(
	account="YOURACCOUNT",
	place_name="YOURPLACENAME",
	debug=True
)
pprint(iris.devices)
```
This will allow me to understand the capabilities of other devices and build their modules correctly.
