import math
import os
from Queue import PriorityQueue
from xml.etree import ElementTree
from PIL import Image

from point import Point
from quadtree import Quadtree

class Map:
	def __init__(self, definition_file, points):
		# Open definition file and background image
		definition = ElementTree.parse(open(definition_file)).getroot()
		map_file = os.path.join(os.path.split(definition_file)[0], definition.attrib['bg'])
		self.background = Image.open(map_file)
		
		self.north = math.radians(float(definition.attrib['maxlat']))
		self.south = math.radians(float(definition.attrib['minlat']))
		self.west = math.radians(float(definition.attrib['minlon']))
		self.east = math.radians(float(definition.attrib['maxlon']))

		# Store ranges color and distance
		self.ranges = [(float(r.attrib['distance']), 
					(int(r.attrib['red']), int(r.attrib['green']), int(r.attrib['blue']))) 
					for r in definition.getiterator("range")]
			
		self.width, self.height = self.background.size
		self.points = points

		# Creating top quadtree element
		self.grid = Quadtree(self.north, self.south, self.west, self.east, 6)
		for point in points:
			self.grid.add(point)

		# Precompute latitude and longitude at each row and column
		self.pixel_lons = [self.west + (self.east-self.west)*(float(i)/float(self.width)) for i in range(self.width)]
		self.pixel_lats = [self.north - (self.north-self.south)*(float(j)/float(self.height)) for j in range(self.height)]

	def generate(self):
		"Generates the output image"
	
		ranges_image = Image.new('RGB', self.background.size)
		
		# Create a lists list with the distance from each pixel to its nearest point
		colors = [[self.color(self.distance(i,j)) for i in range(self.width)] for j in range(self.height)]
		# Flatten list
		colors = [item for sublist in colors for item in sublist]

		ranges_image.putdata(colors)
		return Image.blend(ranges_image, self.background.convert('RGB'), 0.5)

	def distance(self, i, j):
		lon = self.pixel_lons[i]
		lat = self.pixel_lats[j]		

		point = Point(lat, lon)

		elements = PriorityQueue()
		elements.put_nowait((self.grid.distance(point), self.grid))
		# We iterate over the priority queue until the nearest element is a point. While it isn't we add its children to the queue.
		while True:
			(distance, elem) = elements.get_nowait()
			#print "Iterating (%d, %d) distance: %f" % (i, j, distance)
			if isinstance(elem, Point):
				return distance
			else:
				for child in elem.children:
					elements.put_nowait((child.distance(point), child))

	def color(self, distance):
		"Returns which color represents distance"
		return [c for (d,c) in self.ranges if d>distance][0]

