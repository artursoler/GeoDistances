import os
from xml.etree import ElementTree
from PIL import Image

from point import Point

class Map:
	def __init__(self, definition_file, points):
		definition = ElementTree.parse(open(definition_file)).getroot()
		map_file = os.path.join(os.path.split(definition_file)[0], definition.attrib['bg'])
		self.background = Image.open(map_file)
		
		self.north = float(definition.attrib['maxlat'])
		self.south = float(definition.attrib['minlat'])
		self.west = float(definition.attrib['minlon'])
		self.east = float(definition.attrib['maxlon'])

		self.ranges = [(float(r.attrib['distance']), 
					(int(r.attrib['red']), int(r.attrib['green']), int(r.attrib['blue']))) 
					for r in definition.getiterator("range")]
			
		self.width, self.height = self.background.size
		self.points = points

		self.pixel_lons = [self.west + (self.east-self.west)*(float(i)/float(self.width)) for i in range(self.width)]
		self.pixel_lats = [self.north - (self.north-self.south)*(float(j)/float(self.height)) for j in range(self.height)]

	def generate(self):
		ranges_image = Image.new('RGB', self.background.size)
		
		colors = [[self.color(self.distance(i,j)) for i in range(self.width)] for j in range(self.height)]
		colors = [item for sublist in colors for item in sublist]

		ranges_image.putdata(colors)
		return Image.blend(ranges_image, self.background.convert('RGB'), 0.5)

	def distance(self, i, j):
		lon = self.pixel_lons[i]
		lat = self.pixel_lats[j]		

		point = Point(lat, lon)
		return min(point.distance(p) for p in self.points)

	def color(self, distance):
		"Returns which color represents distance"
		return [c for (d,c) in self.ranges if d>distance][0]

