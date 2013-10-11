#! /usr/bin/env python2

from math import sqrt, pow

TIME = 0
DELAY = 1.5 # m.s-1

class SpacePoint:
    def __init__(self, lat, lng, hght):
	self.lat = lat
	self.lng = lng
	self.hght = hght

class Satellite:

    def __init__(self, position):
	self.position = position

    def getTime(self, src):
	return TIME + delay(self.position, src.position)
	
class Person:

    def __init__(self, position):
	self.position = position


    def computePosition(self):
	for i, sat in enumerate(SATS):
	    dist = distance(self, sat)
	    
	    print "Distance to sat #%d : %f" % (i, dist)
	
SATS = (Satellite(SpacePoint(5, 5, 5)),
	Satellite(SpacePoint(-5, 0, 5)),
	Satellite(SpacePoint(-10, -5, 5)))

PERSON = Person(SpacePoint(0, 0, 0))

def distance(p1, p2):
    return sqrt(pow(p2.position.lat - p1.position.lat, 2) \
	      + pow(p2.position.lng - p1.position.lng, 2) \
	      + pow(p2.position.hght - p1.position.hght, 2))

def delay(p1, p2):
    return distance(p1, p2) * DELAY


PERSON.computePosition()
