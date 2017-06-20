#! //anaconda/bin/python

from kzpy3.utils import *
from numpy import *
import argparse


INVALID_DEFAULT = '__nada__'
parser = argparse.ArgumentParser(description='dict.py, look up word in dictionary')
parser.add_argument('word', nargs='?',action="store", type=str,default=INVALID_DEFAULT,help='word to look up')

results = parser.parse_args()

unix('open dict://'+results.word,False)