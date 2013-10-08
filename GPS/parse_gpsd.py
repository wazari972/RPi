#! /usr/bin/env python2

import subprocess
import json

gpspipe_p = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE) #Set up the echo command and direct the output to a pipe

current = 0
max = 10

try:
    while True:
	line = json.loads(gpspipe_p.stdout.readline())
	
	if line["class"] == "TPV":
	    print "Position: %.4f/%.4f (%.2fft)" % (float(line["lat"]), float(line["lon"]), float(line["alt"]))
	    print "Speed: %.2fmph Climb: %.2fmph" % (float(line["speed"]), float(line["climb"]))
	elif line["class"] == "SKY":
	    print "Sat. Fixes: %d" % (len(line["satellites"]))
	max += 1

	if current ==  max:
	    break
except Exception as e:
    print "shit: ", e
    pass

gpspipe_p.kill()

print "Bye!"
