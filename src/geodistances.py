#!/usr/bin/python

from xml.etree import ElementTree
import zipfile
import sys

from point import Point
from map import Map

WPT_TAG = "{http://www.topografix.com/GPX/1/0}wpt"

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Usage: python geodistances.py GPX_MAP.ZIP MAP_DEFINITION.XML OUTPUT_IMAGE.BMP"
	else:
		# Reads gpx in zip file
		file = zipfile.ZipFile(open(sys.argv[1]))
		file = file.open(file.namelist()[0])
	
		# Loads all waypoints
		wpt_elements = ElementTree.parse(file).getroot().getiterator(WPT_TAG)
		points = [Point(float(wpt.attrib['lat']), float(wpt.attrib['lon'])) for wpt in wpt_elements]
				
		# Creates map with waypoints and generates image
		map = Map(sys.argv[2], points)
		output = map.generate()
		output.save(sys.argv[3])

