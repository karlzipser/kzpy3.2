#!/usr/bin/env python
from kzpy3.utils3 import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--Fahrenheit','-f',required=False,type=float,)
parser.add_argument('--Celsius','-c',required=False,type=float,)
Args = parser.parse_args().__dict__

if Args['Fahrenheit'] == None and Args['Celsius'] == None:
	cr(Args)
	cr("*** Error, Args['Fahrenheit'] == None and Args['Celsius'] == None")
	sys.exit()

if Args['Fahrenheit'] != None and Args['Celsius'] != None:
	cr(Args)
	cr("*** Error, Args['Fahrenheit'] != None and Args['Celsius'] != None")
	sys.exit()

if Args['Fahrenheit'] != None:

	C = dp((Args['Fahrenheit'] - 32.) * 5/9.)
	if C > 37:
		cc = cr
	elif C > 0:
		cc = cg
	else:
		cc = cb
	cc('\n\t',Args['Fahrenheit'],'degrees F =',C,'degrees C\n')
	
else:
	F = dp((Args['Celsius'] * 9/5.) + 32)

	if F > 98.6:
		cc = cr
	elif F > 32:
		cc = cg
	else:
		cc = cb
	cc('\n\t',Args['Celsius'],'degrees C =',F,'degrees F\n')
