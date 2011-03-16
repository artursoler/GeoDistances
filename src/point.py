import math

EARTH_RAD = 6371.0
EARTH_RAD_2 = EARTH_RAD * 2

class Point:
	def __init__(self, lat, lon):
		# Precomputes some values
		self.lat = lat
		self.lon = lon
		self.lat_cos = math.cos(self.lat)

	def distance(self, other):
		"Calculates distances between two points using the haversine formula"
		delta_lat = self.lat - other.lat
		delta_lon = self.lon - other.lon
		a = math.sin(delta_lat/2.0)**2 + self.lat_cos*other.lat_cos*math.sin(delta_lon/2.0)**2
		c = math.atan2(math.sqrt(a), math.sqrt(1-a))
		return EARTH_RAD_2 * c

	def __str__(self):
		return "[%f, %f]" % (self.lat, self.lon)

	def __repr__(self):
		return str(self)

