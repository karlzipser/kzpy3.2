#! //anaconda/bin/python
# https://pymotw.com/2/argparse/
from kzpy3.utils import *
import argparse

INVALID_DEFAULT = 999999

parser = argparse.ArgumentParser(description='krn.py, run specificed cell from scratch_script.py')
parser.add_argument('cell', nargs='?',action="store", type=int,default=INVALID_DEFAULT,help='cell number')
parser.add_argument('-v', action='store_true', default=False,
    dest='verify',
    help='show cell and verify to run')
parser.add_argument('-s', action='store_true', default=False,
    dest='show_only',
    help='show cell but do not run')

parser.add_argument('-o', action='store_true', default=False,
    dest='open_script',
    help='open script file')

results = parser.parse_args()

if results.open_script:
	unix(d2s("open",opjh("kzpy3/scratch/2015/12/scratch_script.py")),False)

if results.cell != INVALID_DEFAULT:
	zrn(results.cell,results.verify,results.show_only)
else:
	print('zrn.py: no commands given, nothing done.')

