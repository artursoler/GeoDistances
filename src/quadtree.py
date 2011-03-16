from point import Point

class Quadtree:
	def __init__(self, north, south, west, east, depth):
		self.north = north
		self.south = south
		self.west = west
		self.east = east
	
		self.depth = depth
		self.center_lat = (north + south)/2.0
		self.center_lon = (east + west)/2.0

		self.children = []

	def add(self, point):
		if self.depth > 0:
			# We create subtrees when the first element is inserted in the quadtree.
			if not self.children:
				self.children = [Quadtree(self.north, self.center_lat, self.west, self.center_lon, self.depth-1),
							Quadtree(self.north, self.center_lat, self.center_lon, self.east, self.depth-1),
							Quadtree(self.center_lat, self.south, self.west, self.center_lon, self.depth-1),
							Quadtree(self.center_lat, self.south, self.center_lon, self.east, self.depth-1)]
			index = 0
			if point.lat < self.center_lat:
				index += 2
			if point.lon > self.center_lon:
				index += 1
			self.children[index].add(point)

		else:
			self.children.append(point)	

	def distance(self, point):
		if self.south > point.lat:
			if self.west < point.lon < self.east:
				return point.distance(Point(self.south, point.lon))
			else:
				return min(point.distance(Point(self.south, self.west)), point.distance(Point(self.south, self.east)))
		
		elif self.north > point.lat:
			if self.west < point.lon < self.east:
				return 0.0
			else:
				return min(point.distance(Point(point.lat, self.west)), point.distance(Point(point.lat, self.east)))

		else:
			if self.west < point.lon < self.east:
				return point.distance(Point(self.north, point.lon))
			else:
				return min(point.distance(Point(self.north, self.west)), point.distance(Point(self.north, self.east)))

