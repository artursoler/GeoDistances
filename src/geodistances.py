#!/usr/bin/python

import math
from xml.etree import ElementTree
import zipfile
import sys

from point import Point
from map import Map

WPT_TAG = "{http://www.topografix.com/GPX/1/0}wpt"

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Usage: python geodistances.py GPX_MAP MAP_DEFINITION OUTPUT_IMAGE"
		print "GPX_MAP must be zipped."
		print "MAP_DEFINITION must be a XML document"
		print "OUTPUT_IMAGE can be in BMP, JPG or PNG (requires libraries when installing PIL)"
	else:
		# Reads gpx in zip file
		file = zipfile.ZipFile(open(sys.argv[1]))
		file = file.open(file.namelist()[0])
	
		# Loads all waypoints
		wpt_elements = ElementTree.parse(file).getroot().getiterator(WPT_TAG)
		points = [Point(math.radians(float(wpt.attrib['lat'])), math.radians(float(wpt.attrib['lon']))) for wpt in wpt_elements]
		# Creates map with waypoints and generates image
		map = Map(sys.argv[2], points)
		output = map.generate()
		output.save(sys.argv[3])

