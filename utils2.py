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

#from kzpy3.All_Names_Module import *
import_list = ['os','os.path','shutil','scipy','scipy.io','string','glob','time','sys','datetime','random','cPickle','re',
	'subprocess','threading','serial','math','inspect','fnmatch','h5py','socket','getpass','numbers']#,'importlib']
import_from_list = [['FROM','pprint','pprint'],['FROM','scipy.optimize','curve_fit'],['FROM','termcolor','cprint']]
import_as_list = [['AS','numpy','np'],['AS','cPickle','pickle']]

for im in import_list + import_from_list + import_as_list:
	if type(im) == str:
		try:
			exec('import '+im)
			#print("imported "+im)
		except:
			pass
			print('Failed to import '+im)
	else:
		assert(type(im)) == list
		if im[0] == 'FROM':
			try:
				exec('from '+im[1]+' import '+im[2])
				#print("from "+im[1]+" imported "+im[2])
			except:
				pass
				print('Failed to from '+im[1]+' import '+im[2])
		else:
			assert(im[0] == 'AS')
			try:
				exec('import '+im[1]+' as '+im[2])
				#print("imported "+im[1]+" as "+im[2])
			except:
				pass
				print('Failed to import '+im[1]+' as '+im[2])           

#print("*** Note, kzpy3/teg2/bashrc now does: 'export PYTHONSTARTUP=~/kzpy3/vis2.py' ***")


####################################
# exception format:
if False:
	try:
		pass
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
#
####################################
stars0_ = '**********************\n*\n'
stars1_ = '\n*\n**********************'
tb = '\t'
tb_ = '\t'

na = np.array

def print_stars(n=1):
	for i in range(n):
		print("""*************************************************""")
def print_stars0(n=1):
	print_stars()
	print("*")
def print_stars1(n=1):
	print("*")
	print_stars()



host_name = socket.gethostname()
home_path = os.path.expanduser("~")
username = getpass.getuser()

imread = scipy.misc.imread
imsave = scipy.misc.imsave
degrees = np.degrees


arange = np.arange
os.environ['GLOG_minloglevel'] = '2'

gg = glob.glob
def sgg(d):
	return sorted(gg(d),key=natural_keys)
def sggo(d,*args):
	a = opj(d,*args)
	return sgg(a)

shape = np.shape
randint = np.random.randint
#random = np.random.random # - this makes a conflict, so don't use it.
randn = np.random.randn
zeros = np.zeros
ones = np.ones
imresize = scipy.misc.imresize
reshape = np.reshape
mod = np.mod
array = np.array

abs = np.abs
def opj(*args):
	if len(args) == 0:
		args = ['']
	str_args = []
	for a in args:
		str_args.append(str(a))
	return os.path.join(*str_args)
def opjh(*args):
	return opj(home_path,opj(*args))
def opjD(*args):
	return opjh('Desktop',opj(*args))
def opjm(*args):
	media_path = opj('/media',username)
	return opj(media_path,opj(*args))

def rlen(a):
	return range(len(a))

PRINT_COMMENTS = True
def CS_(comment,section='',say_comment=False):
	stri = '# - '
	if len(section) > 0:
		stri = stri + section + ': '
	stri = stri + comment
	if PRINT_COMMENTS:
		cprint(stri,attrs=['bold'],color='white',on_color='on_grey')#cprint(stri,'red','on_green')
	if say_comment:
		if using_osx():
			say(comment,rate=250,print_text=False)


def zeroToOneRange(m):
	min_n = 1.0*np.min(m)
	return (1.0*m-min_n)/(1.0*np.max(m)-min_n)
z2o = zeroToOneRange


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


def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	'''
	alist.sort(key=natural_keys) sorts in human order
	http://nedbatchelder.com/blog/200712/human_sorting.html
	(See Toothy's implementation in the comments)
	'''
	return [ atoi(c) for c in re.split('(\d+)', text) ]

def str_contains(st,str_list):
	for s in str_list:
		if not s in st:
			return False
	return True
	
def str_contains_one(st,str_list):
	for s in str_list:
		if s in st:
			return True
	return False


def unix(command_line_str, print_stdout=False, print_stderr=False,print_cmd=False):
	command_line_str = command_line_str.replace('~',home_path)
	p = subprocess.Popen(command_line_str.split(), stdout=subprocess.PIPE)
	stdout,stderr = p.communicate()
	if print_cmd:
		print(command_line_str)
	if print_stdout:
		print(stdout)
	if print_stderr:
		print(stderr)
#    return stdout,stderr
	return stdout.split('\n')



def d2s_spacer(args,spacer=' '):
	lst = []
	for e in args:
		lst.append(str(e))
	return spacer.join(lst)
def d2s(*args):
	'''
	e.g.,
	
	d2s('I','like',1,'or',[2,3,4])
	
	yields
	
	'I like 1 or [2, 3, 4]'
	
	d2c(1,2,3) => '1,2,3'
	d2f('/',1,2,3) => '1/2/3'
	'''
	return d2s_spacer(args)
def d2c(*args):
	return d2s_spacer(args,spacer=',')
def d2p(*args):
	return d2s_spacer(args,spacer='.')
def d2n(*args):
	return d2s_spacer(args,spacer='')
def d2f(*args):
	return d2s_spacer(args[1:],spacer=args[0])
def pd2s(*args):
	cprint(d2s(*args))#,'yellow')
def spd2s(*args):
	d_ = d2s(*args)
	l_ = len(d_)
	s_ = ""
	for q_ in range(len(d_)+4):
		s_ += "*"
	cprint(s_+'\n*','yellow')
	cprint('* '+d_,'yellow')
	cprint('*\n'+s_,'yellow')
def sbpd2s(*args):
	d_ = d2s(*args)
	l_ = len(d_)
	s_ = ""
	for q_ in range(len(d_)+4):
		s_ += "*"
	cprint(s_+'\n*','blue')
	cprint('* '+d_,'blue')
	cprint('*\n'+s_,'blue')
def srpd2s(*args):
	d_ = d2s(*args)
	l_ = len(d_)
	s_ = ""
	for q_ in range(len(d_)+4):
		s_ += "*"
	cprint(s_+'\n*','red')
	cprint('* '+d_,'red')
	cprint('*\n'+s_,'red')

def dp(f,n=2):
	"""
	get floats to the right number of decimal places, for display purposes
	"""
	assert(n>=0)
	if n == 0:
		return int(np.round(f))
	f *= 10.0**n
	f = int(np.round(f))
	return f/(10.0**n)
   

def save_obj(obj, name ):
	if name.endswith('.pkl'):
		name = name[:-len('.pkl')]
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name,noisy=True):
	if noisy:
		timer = Timer()
		print(d2s('Loading',name,'. . .\r')),
		sys.stdout.flush()
	if name.endswith('.pkl'):
		name = name[:-len('.pkl')]
	assert_disk_locations(name+'.pkl')
	with open(name + '.pkl', 'rb') as f:
		o = pickle.load(f)
		if noisy:
			print(d2s('. . . loaded in',dp(timer.time()),'seconds.\r')),
			sys.stdout.flush()
		return o
lo = load_obj
def so(arg1,arg2):
	if type(arg1) == str and type(arg2) != str:
		save_obj(arg2,arg1)
		return
	if type(arg2) == str and type(arg1) != str:
		save_obj(arg1,arg2)
		return
	assert(False)


"""
def psave(dic,data_path_key,path):
	save_obj(dic[data_path_key],opj(path,data_path_key))
def pload(dic,data_path_key,path):
	dic[data_path_key] = load_obj(opj(path,data_path_key))
"""

def txt_file_to_list_of_strings(path_and_filename):
	f = open(path_and_filename,"r") #opens file with name of "test.txt"
	str_lst = []
	for line in f:
		str_lst.append(line.strip('\n'))
	return str_lst

def list_of_strings_to_txt_file(path_and_filename,str_lst,write_mode="w"):
	f = open(path_and_filename,write_mode)
	for s in str_lst:
		f.write(s+'\n')
	f.close()


def text_to_file(f,t):
	list_of_strings_to_txt_file(f,t.split('\n'))


def file_to_text(f):
	return '\n'.join(txt_file_to_list_of_strings(f))



def rebin(a, shape):
	'''
	from http://stackoverflow.com/questions/8090229/resize-with-averaging-or-rebin-a-numpy-2d-array
	'''
	sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
	return a.reshape(sh).mean(-1).mean(1)


def dict_to_sorted_list(d):
	l = []
	ks = sorted(d.keys(),key=natural_keys)
	for k in ks:
		l.append(d[k])
	return l

def get_sorted_keys_and_data(dict):
	skeys = sorted(dict.keys())
	sdata = []
	for k in skeys:
		sdata.append(dict[k])
	return skeys,sdata


def zscore(m,thresh=np.nan):
	z = m - np.mean(m)
	z /= np.std(m)
	if not np.isnan(thresh):
		z[z < -thresh] = -thresh
		z[z > thresh] = thresh
	return z

"""

%a - abbreviated weekday name
%A - full weekday name
%b - abbreviated month name
%B - full month name
%c - preferred date and time representation
%C - century number (the year divided by 100, range 00 to 99)
%d - day of the month (01 to 31)
%D - same as %m/%d/%y
%e - day of the month (1 to 31)
%g - like %G, but without the century
%G - 4-digit year corresponding to the ISO week number (see %V).
%h - same as %b
%H - hour, using a 24-hour clock (00 to 23)
%I - hour, using a 12-hour clock (01 to 12)
%j - day of the year (001 to 366)
%m - month (01 to 12)
%M - minute
%n - newline character
%p - either am or pm according to the given time value
%r - time in a.m. and p.m. notation
%R - time in 24 hour notation
%S - second
%t - tab character
%T - current time, equal to %H:%M:%S
%u - weekday as a number (1 to 7), Monday=1. Warning: In Sun Solaris Sunday=1
%U - week number of the current year, starting with the first Sunday as the first day of the first week
%V - The ISO 8601 week number of the current year (01 to 53), where week 1 is the first week that has at least 4 days in the current year, and with Monday as the first day of the week
%W - week number of the current year, starting with the first Monday as the first day of the first week
%w - day of the week as a decimal, Sunday=0
%x - preferred date representation without the time
%X - preferred time representation without the date
%y - year without a century (range 00 to 99)
%Y - year including the century
%Z or %z - time zone or name or abbreviation
%% - a literal % character


"""

def time_str(mode='FileSafe'):
	now = datetime.datetime.now()
	if mode=='FileSafe':
	   return now.strftime('%d%b%y_%Hh%Mm%Ss')
	if mode=='Pretty':
	   return now.strftime('%A, %d %b %Y, %r')
	if mode=='TimeShort':
	   return now.strftime('%H:%M')

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


def getClipboardData():
	p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
	retcode = p.wait()
	data = p.stdout.read()
	return data
gcd = getClipboardData
def setClipboardData(data):
	"""
	setClipboardData
	"""
	p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
	p.stdin.write(data)
	p.stdin.close()
	retcode = p.wait()
scd = setClipboardData

def say(t,rate=150,print_text=True):
	if print_text:
		spd2s(t)
	unix(d2s('say --interactive=/green -r',rate,t))






def stowe_Desktop(dst=False):
	if dst==False:
		dst = opjh('Desktop_'+time_str())
	print(dst)
	unix('mkdir -p ' + dst)
	_,l = dir_as_dic_and_list(opjD(''))
	for i in l:
		shutil.move(opjD(i),dst)

def restore_Desktop(src):
	_,l = dir_as_dic_and_list(opjD(''))
	if len(l) > 0:
		print('**** Cannot restore Desktop because Desktop is not empty.')
		return False
	_,l = dir_as_dic_and_list(src)
	for i in l:
		shutil.move(opjh(src,i),opjD(''))

def advance(lst,e,min_len=1):
	len_lst = len(lst)
	if len_lst < min_len:
		pass
	elif len_lst > 1.2*min_len:
		lst = lst[-min_len:]
	else:
		lst.pop(0)
	lst.append(e)


def kill_ps(process_name_to_kill):
	ax_ps_lst = unix('ps ax',False)
	ps_lst = []
	for p in ax_ps_lst:
		if process_name_to_kill in p:
			ps_lst.append(p)
	pid_lst = []
	for i in range(len(ps_lst)):
		pid = int(ps_lst[i].split(' ')[1])
		pid_lst.append(pid)
	#print pid_lst
	for p in pid_lst:
		unix(d2s('kill',p))


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



def most_recent_file_in_folder(path,str_elements=[],ignore_str_elements=[],return_age_in_seconds=False):
	files = gg(opj(path,'*'))
	if len(files) == 0:
		return None
	candidates = []
	for f in files:
		fn = fname(f)
		is_candidate = True
		for s in str_elements:
			if s not in fn:
				is_candidate = False
				break
		for s in ignore_str_elements:
			if s in fn:
				is_candidate = False
				break
		if is_candidate:
			candidates.append(f)
	mtimes = {}
	if len(candidates) == 0:
		return None
	for c in candidates:
		mtimes[os.path.getmtime(c)] = c
	mt = sorted(mtimes.keys())[-1]
	c = mtimes[mt]
	if return_age_in_seconds:
		return c,time.time()-mt
	else:
		return c


def a_key(dic):
	keys = dic.keys()
	k = np.random.randint(len(keys))
	return keys[k]

def an_element(dic):
	return dic[a_key(dic)]


def fn(path):
	"""
	get filename part of path
	"""
	return path.split('/')[-1]


def to_range(e,a,b):
	if e < a:
		return a
	if e > b:
		return b
	return e

def in_range(e,a,b):
	if e >= a:
		if e <= b:
			return True
	return False

def nvidia_smi_continuous(t=0.1):
	while True:                                     
		unix('nvidia-smi',print_stdout=True)
		time.sleep(t)



class Timer:
	def __init__(self, time_s=0):
		self.time_s = time_s
		self.start_time = time.time()
		self.count = 0
	def check(self):
		if time.time() - self.start_time > self.time_s:
			return True
		else:
			return False
	def time(self):
		return time.time() - self.start_time
	def reset(self):
		self.start_time = time.time()
		self.count = 0
	def trigger(self):
		self.start_time = 0
	def freq(self,name='',do_print=True):
		self.count += 1
		if self.check():
			value = self.count/self.time()
			if do_print:
				pd2s(name,'frequency =',dp(value,2),'Hz')
			self.reset()
			return value
	def message(self,message_str,color='grey',flush=False):
		if self.check():
			print(message_str+'\r'),
			sys.stdout.flush()
			self.reset()
	def percent_message(self,i,i_max,flush=False):
		self.message(d2s(i,int(100*i/(1.0*i_max)),'%'),color='white')
	def wait(self):
		while not(self.check()):
			time.sleep(self.time_s/100.0)
		self.reset()	


  


def fname(path):
	return path.split('/')[-1]


def pname(path):
	p = path.split('/')[:-1]
	pstr = ""
	for s in p:
		if len(s)>0:
			pstr += '/' + s
	return pstr

def sequential_means(data,nn):
	a = array(data)
	d = []
	x = []
	n = min(len(a),nn)
	for i in range(0,len(a),n):
		d.append(a[i:i+n].mean())
		x.append(i+n/2.)
	return x,d


def tab_list_print(l,n=1,color=None,on_color=None):
	for e in l:
		s = ''
		for j in range(n):
			s += '\t'
		cprint(s+e,color,on_color)



def start_at(t):
	while time.time() < t:
		time.sleep(0.1)
		print(t-time.time())

try:
	import numbers
	def is_number(n):
		return isinstance(n,numbers.Number)
except:
	print("Don't have numbers module")



def str_replace(input_str,replace_dic):
	for r in replace_dic:
		input_str = input_str.replace(r,replace_dic[r])
	return input_str



def srtky(d):
	return sorted(d.keys())


def get_key_sorted_elements_of_dic(d,specific=None):
	ks = sorted(d.keys())
	els = []
	for k in ks:
		if specific == None:
			els.append(d[k])
		else:
			els.append(d[k][specific])
	return ks,els


def mean_of_upper_range(data,min_proportion,max_proportion):
	return array(sorted(data))[int(len(data)*min_proportion):int(len(data)*max_proportion)].mean()


def mean_exclude_outliers(data,n,min_proportion,max_proportion):
	"""
	e.g.,

	L=lo('/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta/direct_rewrite_test_11May17_16h16m49s_Mr_Blue/left_image_bound_to_data.pkl' )
	k,d = get_key_sorted_elements_of_dic(L,'encoder')
	d2=mean_of_upper_range_apply_to_list(d,30,0.33,0.66)
	CA();plot(k,d);plot(k,d2)
	
	"""
	n2 = int(n/2)
	rdata = []
	len_data = len(data)
	for i in range(len_data):
		if i < n2:
			rdata.append(mean_of_upper_range(data[i:i-n2+n],min_proportion,max_proportion))
		elif i < len_data + n2:
			rdata.append(mean_of_upper_range(data[i-n2:i-n2+n],min_proportion,max_proportion))
		else:
			rdata.append(mean_of_upper_range(data[i-n2:i],min_proportion,max_proportion))
	return rdata

def meo(data,n):
	return mean_exclude_outliers(data,n,1/3.0,2/3.0)



def pythonpaths(paths):
	for p in paths:
		sys.path.append(opjh(p))


def find_files_recursively(src,pattern,FILES_ONLY=False,DIRS_ONLY=False):
	"""
	https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
	"""
	files = []
	folders = {}
	ctr = 0
	timer = Timer(5)
	if src[-1] != '/':
		src = src + '/'
	print(d2s('src =',src,'pattern =',pattern))
	for root, dirnames, filenames in os.walk(src):
		assert(not(FILES_ONLY and DIRS_ONLY))
		if FILES_ONLY:
			use_list = filenames
		elif DIRS_ONLY:
			use_list = dirnames
		else:
			use_list = filenames+dirnames
		for filename in fnmatch.filter(use_list, pattern):
			file = opj(root,filename)
			folder = pname(file).replace(src,'')
			if folder not in folders:
				folders[folder] = []
			folders[folder].append(filename)
			ctr += 1
			if timer.check():
				print(d2s(time_str('Pretty'),ctr,'matches'))
				timer.reset()
	data = {}
	data['paths'] = folders
	data['parent_folders'] = [fname(f) for f in folders.keys()]
	return data



def find_index_of_closest(val,lst):
	d = []
	for i in range(len(lst)):
		d.append(abs(lst[i]-val))
	return d.index(min(d))



if False:
	##################################
	#

	ZD_Dictionary = None
	ZD_Dictionary_name = '<no name>'
	ZD_dic_show_ends = 24


	def zaccess(d,alst,truncate=True,dic_show_ends=4):
		print(zdic_to_str(d,alst,truncate,dic_show_ends))
		for a in alst:
			#print a,d
			if type(d) != dict:
				break
			d = d[sorted(d.keys())[a]]
		return d

	def zds(d,dic_show_ends,*alst):
		alst = list(alst)
		assert(dic_show_ends>1)
		if len(alst) == 0:
			print("zds(d,dic_show_ends,*alst), but len(alst) == 0")
		print(zdic_to_str(d,alst,False,dic_show_ends))



	def _zdl(d,dic_show_ends,*alst):
		alst = list(alst)
		assert(dic_show_ends>1)
		if len(alst) == 0:
			print("zds(d,dic_show_ends,*alst), but len(alst) == 0")
		list_of_strings_to_txt_file(opjh('kzpy3','zdl.txt'),zdic_to_str(d,alst,False,dic_show_ends).split('\n'))




	def zdl(d,dic_show_ends,*alst):
		"""
		https://stackoverflow.com/questions/2749796/how-to-get-the-original-variable-name-of-variable-passed-to-a-function
		"""
		"""
		import inspect
		frame = inspect.currentframe()
		frame = inspect.getouterframes(frame)[1]
		string = inspect.getframeinfo(frame[0]).code_context[0].strip()
		args = string[string.find('(') + 1:-1].split(',')
		names = []
		for i in args:
			if i.find('=') != -1:
				names.append(i.split('=')[1].strip())
			else:
				names.append(i)
		"""
		alst = list(alst)
		assert(dic_show_ends>1)
		if len(alst) == 0:
			print("zds(d,dic_show_ends,*alst), but len(alst) == 0")
		dic_str = zdic_to_str(d,alst,False,dic_show_ends)
		ks = []
		for a in alst:
			if type(d) != dict:
				break
			k = sorted(d.keys())[a]
			d = d[k]
			ks.append(k)
		out_str = ">> "+ZD_Dictionary_name #names[0]
		for k in ks:
			if is_number(k) or type(k) == tuple:
				out_str += '['+str(k)+']'
			else:
				out_str += "['"+k+"']"
		cprint(out_str,'yellow')
		list_of_strings_to_txt_file(opjh('kzpy3','zdl.txt'),[out_str,ZD_Dictionary_name]+dic_str.split('\n'))


	def zdset(d,dic_show_ends=24):
		import inspect
		frame = inspect.currentframe()
		frame = inspect.getouterframes(frame)[1]
		string = inspect.getframeinfo(frame[0]).code_context[0].strip()
		args = string[string.find('(') + 1:-1].split(',')
		names = []
		for i in args:
			if i.find('=') != -1:
				names.append(i.split('=')[1].strip())
			else:
				names.append(i)
		global ZD_Dictionary,ZD_Dictionary_name,ZD_dic_show_ends
		ZD_Dictionary = d
		ZD_Dictionary_name = names[0]
		ZD_dic_show_ends = dic_show_ends




	def zd(*alst):
		alst = list(alst)
		if len(alst) == 0:
			alst = [-1]
		zdl(ZD_Dictionary,ZD_dic_show_ends,*alst)


	def zda(d,dic_show_ends,*alst):
		"""
		https://stackoverflow.com/questions/2749796/how-to-get-the-original-variable-name-of-variable-passed-to-a-function
		"""
		import inspect
		frame = inspect.currentframe()
		frame = inspect.getouterframes(frame)[1]
		string = inspect.getframeinfo(frame[0]).code_context[0].strip()
		args = string[string.find('(') + 1:-1].split(',')
		names = []
		for i in args:
			if i.find('=') != -1:
				names.append(i.split('=')[1].strip())
			else:
				names.append(i)

		zds(d,dic_show_ends,*alst)
		ks = []
		for a in alst:
			if type(d) != dict:
				break
			k = sorted(d.keys())[a]
			d = d[k]
			ks.append(k)
		out_str = ">> "+names[0]
		for k in ks:
			if is_number(k):
				out_str += '['+str(k)+']'
			else:
				out_str += "['"+k+"']"
		cprint(out_str,'yellow')
		return d


	def zlst_truncate(lst,show_ends=2):
		if show_ends == 0:
			return []
		if len(lst) > 2*show_ends:
			out_lst = lst[:show_ends] + ['...'] + lst[-show_ends:]
		else:
			out_lst = lst
		return out_lst

	def zlst_to_str(lst,truncate=True,decimal_places=2,show_ends=2,depth=0,range_lst=[-2]):
		original_len = -1
		if truncate:
			original_len = len(lst)
			lst = zlst_truncate(lst,show_ends=show_ends)
		lst_str = d2n('\t'*(depth),"[")
		for i in range(len(lst)):
			e = lst[i]
			if type(e) == str:
				lst_str += e
			elif type(e) == int:
				lst_str += str(e)
			elif is_number(e):
				lst_str += str(dp(e,decimal_places))
			elif type(e) == list:
				lst_str += zlst_to_str(e,truncate=truncate,decimal_places=decimal_places,show_ends=show_ends)
			elif type(e) == dict:
				lst_str += zdic_to_str(e,range_lst,depth=depth+1)# zlst_to_str(e,truncate=truncate,decimal_places=decimal_places,show_ends=show_ends)
			else:
				lst_str += '???'
			if i < len(lst)-1:
				lst_str += ' '
		lst_str += ']'
		if original_len > 0:
			lst_str += d2n(' (len=',original_len,')')
		return lst_str

	def zdic_to_str(d,range_lst,depth=0,dic_show_ends=4,dic_truncate=True,show_depth=False,show_type=False):

		dic_str_lst = []

		sorted_keys = sorted(d.keys())
		
		this_range = range_lst[0]
		
		if type(this_range) == int:
			if this_range < 0:
				neg_two = False
				if this_range == -2:
					neg_two = True
				if dic_truncate:
					this_range = [0,min(dic_show_ends,len(sorted_keys))]
				else:
					this_range = [0,len(sorted_keys)]
				if neg_two:
					range_lst = range_lst + [-2]
			else:
				this_range = [this_range,this_range+1]

		if this_range[0] > 0:
			dic_str_lst.append(d2n('\t'*depth,'<0> ...'))

		for i in range(this_range[0],this_range[1]):
			if i >= len(sorted_keys):
				return
			key = sorted_keys[i]
			value = d[key]

			if show_depth:
				dic_str_lst.append(d2n('\t'*depth,'<',i,'> ',key,':'))
			else:
				dic_str_lst.append(d2n('\t'*depth,key,':'))
			if isinstance(value,dict):
				if len(range_lst) > 1:
					dic_str_lst.append( zdic_to_str(value,range_lst[1:],depth=depth+1,dic_show_ends=dic_show_ends,dic_truncate=dic_truncate) )
				else:
					dic_str_lst.append(d2n('\t'*(depth+1),'...'))
			else:
				if type(value) == list:
					dic_str_lst.append(zlst_to_str(value,depth=depth+1,range_lst=range_lst[1:]))
				elif type(value) == np.ndarray:
					dic_str_lst.append(zlst_to_str(list(value),depth=depth+1,range_lst=range_lst[1:]))
				elif type(value) == str:
					dic_str_lst.append(d2s('\t'*(depth+1),str(value)))
				else:
					if show_type:
						dic_str_lst.append(d2s('\t'*(depth+1),str(value),type(value)))
					else:
						dic_str_lst.append(d2s('\t'*(depth+1),str(value)))
		if this_range[1] < len(sorted_keys):
			dic_str_lst.append(d2n('\t'*depth,'..',len(d)-1,')'))
		dic_str = ""
		for d in dic_str_lst:
			dic_str += d + "\n"

		return dic_str
	#
	#############################




def assert_disk_locations(locations):
	if type(locations) == str:
		locations = [locations]
	for l in locations:
		#print(d2s("Checking for",l))
		if len(gg(l)) < 1:
			srpd2s(d2s("Error:\n",l,"not available!"))
			if len(l.split('/')) > 0:
				spd2s('Could not find',pname(l),'!!!!!!!!!!')
				raise ValueError(d2s('Could not find',pname(l),'!!!!!!!!!!'))
			#assert(False)
		#print(d2s(l,'is there.\n'))




def h5r(filename,assert_exists=False):
	if assert_exists:
		assert_disk_locations(filename)
	return h5py.File(filename,'r')
def h5w(filename):
	assert_disk_locations(pname(filename))
	return h5py.File(filename,'w')



"""
def XX(in_str):
	eqn = in_str.split('=')
	var_name = eqn[0].replace(' ','')
	elements = eqn[1]
	elements = in_str.split('/')
	exec_lst = []
	exec_lst.append(elements[0])
	for i in range(1,len(elements)):
		quote = "'"
		if '`' in elements[i]:
			quote = ""
		exec_lst.append(('['+quote+elements[i]+quote+']').replace('`',''))
	exec_str = var_name + " = " + ("".join(exec_lst)).replace(' ','')
	return exec_str


def remove_functions_from_dic(d):
	for k in d.keys():
		if callable(d[k]):
			d[k] = 'FUNCTION_PLACEHOLDER'
"""


def even_len(d):
	l = d['l']
	return np.mod(len(l),2) == 0

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









def img_to_img_uint8(d):
	img = d['img']

	return (255.0*z2o(img)).astype(np.uint8)


"""
def zsave_obj(d):
	obj = d['obj']
	path = d['path']
	if 'save_function_placeholder' not in d:
		save_function_placeholder = True

	if path != None:
		print(path)
	if callable(obj):
		if save_function_placeholder:
			text_to_file({ 'txt':'<function>', 'path':path+'.fun' })
		else:
			pass
	elif type(obj) == str:
		text_to_file({'txt':obj,'path':path+'.txt'})
	elif fname(path) == 'img_uint8':
		imsave(path+'.png',obj)
	elif type(obj) == dict:
		assert(path != None)
		unix('mkdir -p '+path)
		for k in obj.keys():
			zsave_obj({ 'obj':obj[k], 'path':opj(path,k) })
	else:
		save_obj(obj,path)
"""

"""
def zload_obj(d):
	path = d['path']

	if 'ctr' not in d:
		ctr = 0
	else:
		ctr = d['ctr']
	
	print(path,ctr)
	obj = {}
	txt = sggo(path,'*.txt')
	fun = sggo(path,'*.fun')
	pkl = sggo(path,'*.pkl')
	img_uint8 = sggo(path,'*.png')
	all_files = sggo(path,'*')
	dic = []
	for a in all_files:
		if os.path.isdir(a):
			dic.append(a)
	#print(dic)
	#print txt
	#print fun
	#print pkl
	#print img_uint8
	#print dic
	#raw_input('hit enter')
	for k in txt:
		q = '\n'.join(txt_file_to_list_of_strings(k))
		n = fname(k).split('.')[0]
		obj[n] = q
	for k in fun:
		n = fname(k).split('.')[0]
		#print('do nothing with '+k)
		#obj[n] = '<function>'
	for k in pkl:
		n = fname(k).split('.')[0]
		obj[n] = load_obj(k)
	for k in img_uint8:
		n = fname(k).split('.')[0]
		obj[n] = imread(k)
	for k in dic:
		n = fname(k)
		#print(dic,n,k,ctr)
		obj[n] = zload_obj({'path':k,'ctr':ctr+1})

	#raw_input('hit enter')
	return obj
"""


def restore_functions(d):
	src = d['src']
	dst = d['dst']

	for k in src.keys():
		if callable(src[k]):
			dst[k] = src[k]
		elif type(src[k]) == dict:
			restore_functions({'src':src[k],'dst':dst[k]})
		else:
			pass


def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l



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



def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*100))
	return l







def img_to_img_uint8(d):
	img = d['img']
	True
	return (255.0*z2o(img)).astype(np.uint8)


"""
def zsave_obj(d):
	obj = d['obj']
	path = d['path']
	True
	if path != None:
		print(path)
	if callable(obj):
		text_to_file({ 'txt':'<function>', 'path':path+'.fun' })
	elif type(obj) == str:
		text_to_file({'txt':obj,'path':path+'.txt'})
	elif fname(path) == 'img_uint8':
		imsave(path+'.png',obj)
	elif type(obj) == dict:
		assert(path != None)
		unix('mkdir -p '+path)
		for k in obj.keys():
			zsave_obj({ 'obj':obj[k], 'path':opj(path,k) })
	else:
		save_obj(obj,path)
"""


"""
def zload_obj(d):
	path = d['path']
	True
	if 'ctr' not in d:
		ctr = 0
	else:
		ctr = d['ctr']
	
	print(path,ctr)
	obj = {}
	txt = sggo(path,'*.txt')
	fun = sggo(path,'*.fun')
	pkl = sggo(path,'*.pkl')
	img_uint8 = sggo(path,'*.png')
	all_files = sggo(path,'*')
	dic = []
	for a in all_files:
		if os.path.isdir(a):
			dic.append(a)
	print(dic)
	#print txt
	#print fun
	#print pkl
	#print img_uint8
	#print dic
	#raw_input('hit enter')
	for k in txt:
		q = '\n'.join(txt_file_to_list_of_strings(k))
		n = fname(k).split('.')[0]
		obj[n] = q
	for k in fun:
		n = fname(k).split('.')[0]
		print('do nothing with '+k)
		#obj[n] = '<function>'
	for k in pkl:
		n = fname(k).split('.')[0]
		obj[n] = load_obj(k)
	for k in img_uint8:
		n = fname(k).split('.')[0]
		obj[n] = imread(k)
	for k in dic:
		n = fname(k)
		print(dic,n,k,ctr)
		obj[n] = zload_obj({'path':k,'ctr':ctr+1})

	#raw_input('hit enter')
	return obj
"""

"""
def zrestore_functions(d):
	src = d['src']
	dst = d['dst']
	True
	for k in src.keys():
		if callable(src[k]):
			dst[k] = src[k]
		elif type(src[k]) == dict:
			restore_functions({'src':src[k],'dst':dst[k]})
		else:
			pass
"""
			

"""
def stop_ros():
	#M['Stop_Arduinos'] = True
	#rospy.signal_shutdown("M[Stop_Arduinos] = True")
	print('!!!!! stop_ros() !!!!!')
	#time.sleep(1)
	unix(opjh('kzpy3/kill_ros.sh'))
	#assert(False)
"""








def is_even(q):
	if np.mod(q,2) == 0:
		return True
	return False




def args_to_dictionary(*args):
	if not is_even(len(args[0])):
		print("args_to_dictionary(*args)")
		print("args are:")
		print(args)
		#raise ValueError('ERROR because: not is_even(len(args[0]))')
		spd2s('def args_to_dictionary(*args): Warning, not is_even(len(args[0]))')
		return
	ctr = 0
	keys = []
	values = []
	for e in args[0]:
		if is_even(ctr):
			keys.append(e)
		else:
			values.append(e)
		ctr += 1
	d = {}
	if len(keys) != len(values):
		print("args_to_dictionary(*args)")
		print("given keys are:")
		print(keys)
		print("given values are:")
		print(values)
		raise ValueError('ERROR because: len(keys) != len(values)')
	for k,v in zip(keys,values):
		d[k] = v
	return d



"""
def nice_print_dic(d):
	dic = d['dic']
	if 'name' in d:
		name = d['name']
	else:
		name = False
	True
	if name != 'False':
		pd2s(name,':')
	sk = sorted(dic.keys())
	for k in sk:
		pd2s(tb,k,'=',dic[k])
	print('')
"""
"""
def nice_print_dic(*args):
	if len(args) == 1 and type(args[0]) == dict:
		d = args[0]
	else:
		d = args_to_dictionary(args) # note, different from args_to_dic(d) !
	dic = d['dic']
	if 'name' in d:
		name = d['name']
	else:
		name = False
	if True:
		if name != 'False':
			pd2s(name,':')
		sk = sorted(dic.keys())
		for k in sk:
			pd2s(tb,k,':',dic[k])
		print('')
"""



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





if False:

	dic_exec_str = """
	Args = args_to_dictionary(args)
	for k in keys_:
		if type(k) == str:
			assert(k in Args)
			exec(k+'='+"'"+k+"'")
		elif type(k) == list:
			exec(k[0]+'='+"'"+k[0]+"'")
			if k[0] not in Args:
				Args[k[0]] = k[1]
	del keys_
				"""




	def zdprint(*args):
		keys_ = ['dic',['depth',-2]]
		exec(dic_exec_str)
		if True:
			if len(Args[dic]) == 0:
				print('empty dictionary')
				return
			zdset(Args[dic])
			zd(Args[depth])
			txt_lst = txt_file_to_list_of_strings(opjh('kzpy3','zdl.txt'))
			print('\n'.join(txt_lst))



def str_is_int(s):
	try:
		int(s)
		return True
	except:
		return False

#####################################################
#
if True:#username != 'nvidia':
	temp = args_to_dictionary(sys.argv[1:])
	if temp != None:
		Args = {}
		for k in temp.keys():
			if '/' in temp[k]:
				print('Treating '+temp[k]+' as filename')
				exec("Args[\'"+k+"\'] = '"+temp[k]+"'")
			elif type(temp[k]) == str:
				exec("Args[\'"+k+"\'] = '"+temp[k]+"'")
			else:
				exec('Args[\''+k+'\'] = '+temp[k])
		del temp
		Arguments = {}
		for a in Args.keys():
			ar = Args[a]
			if str_is_int(ar):
				Arguments[a] = int(ar)
			else:
				Arguments[a] = ar

identify_file_str = """
if '__file__' not in locals():
	__file__ = ' __file__ '
cprint('******** '+__file__+' ********','yellow')
	"""
#
#####################################################



"""
def Rate_Counter(*args):
	Args = args_to_dictionary(args)
	D = {}
	if 'batch_size' in Args:
		D['batch_size'] = Args['batch_size']
	else:
		D['batch_size'] = 1.0
	True
	D[type] = 'Rate_Counter'
	D['purpose'] = d2s(inspect.stack()[0][3],':','Network rate object')
	D['rate_ctr'] = 0
	D['rate_timer_interval'] = 10.0
	D['rate_timer'] = Timer(D['rate_timer_interval'])
	def _function_step():
		D['rate_ctr'] += 1
		if D['rate_timer'].check():
			print(d2s('rate =',dp(D['batch_size']*D['rate_ctr']/D['rate_timer_interval'],2),'Hz'))
			D['rate_timer'].reset()
			D['rate_ctr'] = 0
	D['step'] = _function_step
	return D
"""



def find_nearest(array,value):
	"""
	https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
	"""
	idx = (np.abs(array-value)).argmin()
	return array[idx]


def raw_enter(optional_str=''):
	return raw_input(optional_str+'Hit enter to continue > ')

"""
def build_dic(key_lists):
	D = {}
	if len(key_lists) == 0:
		return D
	for k in key_lists[0]:
		D[k] = build_dic(key_lists[1:])
	return D
def build_dic_list_leaves(key_lists):
	D = {}
	if len(key_lists) == 0:
		return []
	for k in key_lists[0]:
		D[k] = build_dic_list_leaves(key_lists[1:])
	return D	
"""


def bound_value(the_value,the_min,the_max):
	if the_value > the_max:
		return the_max
	elif the_value < the_min:
		return the_min
	else:
		return the_value


def using_platform():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'osx'
    else:
        spd2s('unknown system (not linux or osx)')
        assert False
def using_linux():
    if using_platform() == 'linux':
        return True
    return False
def using_osx():
    if using_platform() == 'osx':
        return True
    return False


def get_safe_name(name):
    lst = []
    for i in range(len(name)):
        if name[i].isalnum():
            lst.append(name[i])
        else:
            lst.append('_')
    return "".join(lst)
    

def num_from_str(s):
	try:
		return int(s)
	except:
		try:
			return float(s)
		except:
			return 'String does not represent a number.'


def intr(n):
	return np.int(np.round(n))


try:
	import rospy
	HAVE_ROS = True
	CS_('HAVE_ROS = True')
except:
	HAVE_ROS = False
	CS_('HAVE_ROS = False')

	
#EOF