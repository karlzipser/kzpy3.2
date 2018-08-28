############################
# - compatibility with Python 3. This stuff from M. Brett's notebooks
# from __future__ import print_function  # print('me') instead of print 'me'
# The above seems to be slow to load, and is necessary to load in this file
# despite the import from kzpy if I want to use printing fully
#from __future__ import division  # 1/2 == 0.5, not 0
############################
from __future__ import print_function  # print('me') instead of print 'me'
from __future__ import division  # 1/2 == 0.5, not 0
######################
"""
pip install pyserial
sudo pip install termcolor

cv2 on osx:
	http://www.mobileway.net/2015/02/14/install-opencv-for-python-on-mac-os-x/
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	brew tap homebrew/science
	brew install opencv
	sudo ln -s /usr/local/Cellar/opencv/2.4.13.2/lib/python2.7/site-packages/cv2.so /Library/Python/2.7/site-packages/cv2.so
	sudo ln -s /usr/local/Cellar/opencv/2.4.13.2/lib/python2.7/site-packages/cv.py /Library/Python/2.7/site-packages/cv.py
	to .bash_profile: export PYTHONPATH=/Library/Python/2.7/site-packages:$PYTHONPATH
x11 on osx: https://www.xquartz.org/
	in .Xdefaults: *VT100.translations: #override  Meta <KeyPress> V:  insert-selection(PRIMARY, CUT_BUFFER0) \n
"""

from kzpy3.utils2_minimal import *

stars0_ = '**********************\n*\n'
stars1_ = '\n*\n**********************'
tb = '\t'
tb_ = '\t'

def dir_as_dic_and_list( path ):
	"""Returns a dictionary and list of files and directories within the path.

	Keyword argument:
		path

	Certain types are ignored:
		.*      -- I want to avoid hidden files and directories.
		_*      -- I use underscore to indicate things to ignore.
		Icon*   -- The Icon? files are a nuisance created by
				  Google Drive that I also want to ignore."""
	return_dic = {}
	return_list = []
	for filename in os.listdir(path):
		if not filename[0] == '.': # ignore /., /.., and hidden directories and files
			if not filename[0] == '_': # ignore files starting with '_'
				if not filename[0:4] == 'Icon': # ignore Google Drive Icon things
					return_dic[filename] = {}
					return_list.append(filename)
	return_list.sort(key=natural_keys)
	return (return_dic,return_list)


equals = 'equals__'
nothing = 'nothing__'
plus_equals = 'plus_equals__'

def dictionary_access(*args):
	"""
	# dictionary access
	# e.g.,
	W={1:{2:{3:4},100:[1,2,3]}}
	print(W)
	print(da(W,1,2))
	da(W,1,2,equals,9)
	print(W)
	print(da(W,1,2))
	"""
	Q = args[0]
	assert(type(Q)==dict)
	range_end = len(args)
	right_hand_side = nothing
	if len(args) > 3:
		if args[-2] in [equals,plus_equals]:
			right_hand_side = args[-1]
			range_end = len(args)-2
	for i in range(1,range_end):
		k = args[i]
		assert(type(k) in [str,int,bool,float,tuple])
		if k not in Q:
			Q[k] = {}
		if i == range_end-1:
			if right_hand_side != nothing:
				if args[-2] == equals:
					Q[k] = right_hand_side
				elif args[-2] == plus_equals:
					Q[k] += right_hand_side
				return
		#print(type(k),type(Q[k]))
		Q = Q[k]
	return Q
da = dictionary_access




#c = code_to_code_str({'path':path, 'start':106   })

def code_to_code_str(d):
	import pyperclip
	path = d['path']
	code = txt_file_to_list_of_strings(path)
	for i in range(len(code)):
		pd2s(i,')',code[i])
	start,stop = input('start,stop ')
	code_to_clipboard({'path':path,'start':start,'stop':stop})



def code_to_clipboard(d):
	import pyperclip
	code = d['path']
	start = d['start']
	stop = d['stop']

	code_str = '\n'.join(code[start:stop])
	cprint(code_str,'yellow')
	pyperclip.copy(code_str) 
	print('\nOkay, it is in the clipboard')



def blank_dic():
	print("""
def blank_dic(d):
	D = {}
	D[''] = d['']
	True
	D['type'] = '?'
	D['Purpose'] = d2s(inspect.stack()[0][3],':','?')
	return D""")



def translate_args(d):
	translation_dic = d['translation_dic']
	argument_dictionary = d['argument_dictionary']
	print(translation_dic)
	print(argument_dictionary)
	True
	if len(argument_dictionary) == 0:
		return {}
	for k in translation_dic.keys():
		v = translation_dic[k]
		translation_dic['-'+v] = v
	new_dictionary = {}
	for k in argument_dictionary.keys():
		if k in translation_dic.keys():
			new_dictionary[translation_dic[k]] = argument_dictionary[k]
		else:
			print(k+' is an unknown argument!')
			assert(False)
	for k in new_dictionary.keys():
		if k[0] == '-':
			new_dictionary[k[1:]] = new_dictionary[k]
			del new_dictionary[k]
	return new_dictionary




def args_to_dic(d):
	pargs = d['pargs']
	if type(pargs) == str:
		pargs = pargs.split(' ')
	assert(even_len({'l':pargs}))
	rargs = {}
	for i in range(0,len(pargs),2):
		assert(pargs[i][0] == '-')
		k = pargs[i][1:]
		val = pargs[i+1]
		exec(d2n("rargs['",k,"'] = ","'",val,"'"))
		if type(rargs[k]) == str and rargs[k][0] == '{' and rargs[k][-1] == '}':
			exec('rargs[k] = '+rargs[k])
		elif type(rargs[k]) == str and rargs[k][0] == '[' and rargs[k][-1] == ']':
			exec('rargs[k] = '+rargs[k])
	return rargs


def str_replace(input_str,replace_dic):
	for r in replace_dic:
		input_str = input_str.replace(r,replace_dic[r])
	return input_str



def srtky(d):
	return sorted(d.keys())



	def memory():
		"""
		Get node total memory and memory usage
		http://stackoverflow.com/questions/17718449/determine-free-ram-in-python
		"""
		with open('/proc/meminfo', 'r') as mem:
			ret = {}
			tmp = 0
			for i in mem:
				sline = i.split()
				if str(sline[0]) == 'MemTotal:':
					ret['total'] = int(sline[1])
				elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
					tmp += int(sline[1])
			ret['free'] = tmp
			ret['used'] = int(ret['total']) - int(ret['free'])
		return ret



if False:
	def serial_ports():
		""" Lists serial port names

			:raises EnvironmentError:
				On unsupported or unknown platforms
			:returns:
				A list of the serial ports available on the system

			http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
		"""
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result

"""
def zrn(c,verify=False,show_only=False):
	f = opjh('kzpy3/scratch/2015/12/scratch_script.py')
	t = txt_file_to_list_of_strings(f)
	ctr = 0
	u = '\n'.join(t)
	v = u.split('############\n')
	print('###########\n')
	print(v[c])
	if not show_only:
		if verify:
			d = raw_input('########### Do this? ')
			if d == 'y':
				exec(v[c],globals())
		else:
			exec(v[c],globals())
"""


def get_sorted_keys_and_data(dict):
	skeys = sorted(dict.keys())
	sdata = []
	for k in skeys:
		sdata.append(dict[k])
	return skeys,sdata


"""
def psave(dic,data_path_key,path):
	save_obj(dic[data_path_key],opj(path,data_path_key))
def pload(dic,data_path_key,path):
	dic[data_path_key] = load_obj(opj(path,data_path_key))
"""

#EOF


