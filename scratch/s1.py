#! //anaconda/bin/python

#from kzpy3.utils2 import *

def main():
	pprint('Args')
	#print type(Args['a'])
	return 'x'



def get_files_sorted_by_mtime(path_specification):
	files = sggo(path_specification)
	Mtimes = {}
	for f in files:
		Mtimes[f] = os.path.getmtime(f)
	return sorted(Mtimes.items(), key=lambda x:x[1])

pprint(get_files_sorted_by_mtime(opjh('Desktop2','*.pdf')))



