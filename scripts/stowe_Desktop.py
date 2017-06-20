#! //anaconda/bin/python

from kzpy3.utils import *
import argparse


INVALID_DEFAULT = '__nada__'
parser = argparse.ArgumentParser(description='stowe_Desktop')
parser.add_argument('dst', nargs='?',action="store", type=str,default=INVALID_DEFAULT,help='dst')

results = parser.parse_args()

if results.dst == INVALID_DEFAULT:
	stowe_Desktop()
else:
	stowe_Desktop(results.dst)
