class MissingConstructorParameter(Exception):
	def __init__(self, classname=None, parameter=None):
		self.classname = classname
		self.parameter = parameter
		return

	def __str__(self):
		self.error = "The required \"{}\" parameter is missing from the {} constructor.".format(self.parameter, self.classname)
		return self.error

class PlaceIDNotFound(Exception):
	def __init__(self, place_name=None):
		self.place_name = place_name
		return

	def __str__(self):
		self.error = "The ID for the place name {} was not found.".format(self.place_name)
		return self.error

class ConfigFileRead(Exception):
	def __init__(self, path=None, message=None):
		self.path = path
		self.message = message
		return

	def __str__(self):
		self.error = "An error occurred when reading the Iris configuration file \"{}\": {}".format(self.path, self.message)
		return self.error

class InvalidConfigFile(Exception):
	def __init__(self, path=None, message=None):
		self.path = path
		self.message = message
		return

	def __str__(self):
		self.error = "The specified config file \"{}\" is invalid: {}".format(self.path, self.message)
		return self.error

class InvalidProfile(Exception):
	def __init__(self, profile=None, message=None):
		self.profile = profile
		self.message = message
		return

	def __str__(self):
		self.error = "The specified is profile \"{}\" is invalid: {}.".format(self.profile, self.message)
		return self.error

class MissingProfile(Exception):
	def __init__(self, profile=None):
		self.profile = profile
		return

	def __str__(self):
		self.error = "The specified profile \"{}\" does not exist.".format(self.profile)
		return self.error

class InvalidJsonError(Exception):
	def __init__(self, status_code=None, body=None):
		self.status_code = status_code
		self.body = body if body else "No HTML body returned"
		return

	def __str__(self):
		return "Invalid JSON was received from the Iris login server. Status code {}; HTML body: {}.".format(self.status_code, self.body)

class AuthenticationError(Exception):
	def __init__(self, wanted=None, got=None):
		self.wanted = wanted
		self.got = got
		return

	def __str__(self):
		return "Did not receive a success status from the Iris login server."

class NoCookieError(Exception):
	def __init__(self):
		return

	def __str__(self):
		self.error = "The request to the Iris login server was successful, but no Set-Cookie header was found in the reponse headers."
		return self.error

class NoTokenInCookieError(Exception):
	def __init__(self):
		return

	def __str__(self):
		self.error = "There was no Iris authentication token in the Set-Cookie response header."
		return self.error

class CookieParseError(Exception):
	def __init__(self):
		return

	def __str__(self):
		self.error = "Could not parse the cookie returned by the Iris login server."
		return self.error

class DeviceMapError(Exception):
	def __init__(self, message=None):
		self.message = message
		return

	def __str__(self):
		self.error = "Failed to generate the required device map. The error is: {}.".format(self.message)
		return self.error

class PersonMapError(Exception):
	def __init__(self, message=None):
		self.message = message
		return

	def __str__(self):
		self.error = "Failed to generate the required person map. The error is: {}.".format(self.message)
		return self.error

class NotAnIrisCoreObject(Exception):
	def __init__(self, classname=None, got=None):
		self.classname = classname
		self.got = got
		return

	def __str__(self):
		self.error = "The class {} requires a valid iris.core.Iris object in the constructor. You provided {}.".format(self.classname, self.got)
		return self.error

class SetAttributeError(Exception):
	def __init__(self, classname=None, attribute=None, message=None):
		self.classname = classname
		self.attribute = attribute
		self.message = message
		return

	def __str__(self):
		self.error = "The class {} requires a valid iris.core.Iris object in the constructor.".format(self.classname)
		return self.error