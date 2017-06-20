#! //anaconda/bin/python

from kzpy3.utils import *
import argparse


INVALID_DEFAULT = '__nada__'
parser = argparse.ArgumentParser(description='stowe_Desktop')
parser.add_argument('src', nargs='?',action="store", type=str,default=INVALID_DEFAULT,help='src folder')

results = parser.parse_args()

if results.src == INVALID_DEFAULT:
	print('Need to give src folder.')
else:
	restore_Desktop(results.src)
