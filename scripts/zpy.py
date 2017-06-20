#! //anaconda/bin/python

from kzpy3.utils import *
from numpy import *
import argparse


INVALID_DEFAULT = '__nada__'
parser = argparse.ArgumentParser(description='zpy.py, run specificed string in python')
parser.add_argument('cell', nargs='?',action="store", type=str,default=INVALID_DEFAULT,help='cell number')
parser.add_argument('--clear', action='store_true', default=False,
    dest='clear_variables',
    help='clear /tmp/zpy_vars')

parser.add_argument('-o', action='store_true', default=False,
    dest='open_zpy_vars',
    help='open /tmp/zpy_vars')

results = parser.parse_args()

if results.open_zpy_vars:
	unix('open /tmp/zpy_vars',False)

if results.clear_variables:
	for g in gg('/tmp/zpy_vars/*'):
		unix('rm '+g,False)

if results.cell != INVALID_DEFAULT:

	_first = [_v for _v in globals().keys() if not _v.startswith('_')]

	unix('mkdir -p /tmp/zpy_vars',False)
	if True:
		for _f in gg(opj('/tmp/zpy_vars','*.pkl')):
			_vn = _f.split('/')[-1].split('.pkl')[0]
			try:
				exec( _vn + " = load_obj('"+_f.replace('.pkl','')+"')")
			except:
				print(d2s('unable to load',_f))


	exec(sys.argv[1])

	_o = sys.argv[1].split('\n')[-1].split(';')[-1]

	try:
		exec('_q = '+_o)
		print(_q)
	except:
		pass
		
	_second = [_v for _v in globals().keys() if not _v.startswith('_')]

	vars = list(set(_second) - set(_first))

	if True:
		for _v in vars:
			save_obj(globals()[_v],opj('/tmp/zpy_vars',_v))
else:
	print('zpy.py: no commands given, nothing done.')
