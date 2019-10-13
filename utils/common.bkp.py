from __future__ import print_function  # print('me') instead of print 'me'
from __future__ import division  # 1/2 == 0.5, not 0

import_list = ['os','os.path','shutil','scipy','scipy.io','string','glob','time','sys','datetime','random','re',
    'subprocess','threading','serial','inspect','fnmatch','h5py','socket','getpass','numbers','math']#,'importlib']
import_from_list = [['FROM','pprint','pprint'],['FROM','termcolor','cprint']]
import_as_list = [['AS','numpy','np'],['AS','cPickle','pickle']]



def raw_enter(optional_str=''):
    return raw_input(optional_str+'Hit enter to continue > ')

####################################
# exception format:
def et():
    print(
        """
except KeyboardInterrupt:
    cr('\n\n*** KeyboardInterrupt ***\n')
    sys.exit()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    CS_('Exception!',emphasis=True)
    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)        

        """
        )
EXCEPT_STR = """
exc_type, exc_obj, exc_tb = sys.exc_info()
file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
CS_('Exception!',exception=True,newline=False)
CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
"""
#
####################################

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

rnd = np.random.random
rndint = np.random.randint
rndn = np.random.randn
rndchoice = np.random.choice

na = np.array


def is_even(q):
    if np.mod(q,2) == 0:
        return True
    return False
    
def fname(path):
    return path.split('/')[-1]


def pname(path):
    p = path.split('/')[:-1]
    pstr = ""
    for s in p:
        if len(s)>0:
            pstr += '/' + s
    return pstr
    
def beep():
    print('\007')

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

try:
    imread = scipy.misc.imread
    imsave = scipy.misc.imsave
    imresize = scipy.misc.imresize
except:
    print("failed: imread = scipy.misc.imread, imsave = scipy.misc.imsave")

degrees = np.degrees

arange = np.arange

if False:
    os.environ['GLOG_minloglevel'] = '2'

    gg = glob.glob
    def sgg(d):
        return sorted(gg(d),key=natural_keys)
    def sggo(d,*args):
        a = opj(d,*args)
        return sgg(a)
    def get_files_sorted_by_mtime(path_specification):
        files = sggo(path_specification)
        Mtimes = {}
        for f in files:
            Mtimes[f] = os.path.getmtime(f)
        return sorted(Mtimes.items(), key=lambda x:x[1])
    def tsggo(d,*args):
        a = opj(d,*args)
        #CS_(a)
        return get_files_sorted_by_mtime(a)

shape = np.shape
randint = np.random.randint
#random = np.random.random # - this makes a conflict, so don't use it.
randn = np.random.randn
zeros = np.zeros
ones = np.ones

reshape = np.reshape
mod = np.mod
array = np.array

abs = np.abs
if False:
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
    def opjk(*args):
        return opjh('kzpy3',opj(*args))
    def opjm(*args):
        if not using_osx():
            media_path = opj('/media',username)
            return opj(media_path,opj(*args))
        else:
            media_path = '/Volumes'
            return opj(media_path,opj(*args))

def rlen(a):
    return range(len(a))

PRINT_COMMENTS = True
def CS_(comment,section='',s='',say_comment=False,emphasis=False,exception=False,newline=True,print_comment=True):

    if print_comment and PRINT_COMMENTS:
        stri = '#  '
        stri = stri + comment
        if len(s) > len(section):
            section = s
        if len(section) > 0:
            stri += ' ('+section+')'
        if not emphasis and not exception:
            cprint(stri,attrs=[],color='white',on_color='on_grey')#cprint(stri,'red','on_green')
        elif exception:
            cprint(stri,attrs=['blink','bold'],color='red',on_color='on_yellow')
        else:
            cprint(stri,attrs=['bold','reverse'],color='white',on_color='on_grey')
            #spd2s(comment)
        if newline:
            print('\n')
    if say_comment:
        if using_osx():
            say(comment,rate=250,print_text=False)
    return True
    
CS = CS_
#CS_('imported kzpy3.utils3')
def cs(*args):
    CS(d2s_spacer(args,spacer=' '))


if False:
    CVerbose = {}
    CFile = {}
    for color in ['red','yellow','green','blue','magenta','cyan','white','Grey']: #
        an_exec_string = """
    CVerbose['COLOR'] = True
    CFile['COLOR'] = ''
    def cQ(*args):
        if not CVerbose['COLOR']:
            return
        cprint(d2s_spacer(tuple(list(args)+['\t'+CFile['COLOR']])   ,spacer=' '),'COLOR')
    """
        exec(an_exec_string.replace('Q',color[0]).replace('COLOR',color).replace('Grey','grey'))


#



def dic_is_type(Dic,type_str):
    assert type(Dic) == dict
    assert type(type_str) == str
    if 'type' in Dic.keys():
        if Dic['type'] == type_str:
            return True
    return False

if False:
    def zeroToOneRange(m):
        min_n = 1.0*np.min(m)
        return (1.0*m-min_n)/(1.0*np.max(m)-min_n)
    z2o = zeroToOneRange

    def z2_255(m):
        return (255*z2o(na(m))).astype(np.uint8)

    z55 = z2_255

    def z2_255_by_channel(m):
        for i in range(3):
            m[:,:,i] = z2_255(m[:,:,i])
        return m


def dic_of_(list_or_dic,keys):

    D = {}
    for k in keys:
        if list_or_dic == 'lists':
            D[k] = []
        elif list_or_dic == 'dics':
            D[k] = {}
        else:
            cr("***** Error, expected 'lists' or 'dics' as first argument *****")
            assert False
    return D
    
if False:
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
    cprint(d2s(*args))
def pd2n(*args):
    print(d2n(*args))

#if False:
#   for i in range(256):
#       print d2n('\x1b[',i,'m',i,' test','\x1b[36m')
rd = '\x1b[31m'
gr = '\x1b[32m'
yl = '\x1b[33m'
bl = '\x1b[34m'
mg = '\x1b[35m'
lb = '\x1b[36m'
wh = '\x1b[37m'

wh_bk = '\x1b[40m'
wh_rd = '\x1b[41m'
wh_gr = '\x1b[42m'
wh_bl = '\x1b[44m'
wh_mg = '\x1b[45m'
wh_lb = '\x1b[46m'

mg = '\x1b[35m'
lb = '\x1b[36m'
wh = '\x1b[37m'

og = '\x1b[91m'
underlined = '\x1b[4m'

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
   

if False:
    def save_obj(obj, name,noisy=True):
        assert_disk_locations([pname(name)])
        if name.endswith('.pkl'):
            name = name[:-len('.pkl')]
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        if noisy:
            timer = Timer()
            print(d2s('. . . saved',name+'.pkl in',dp(timer.time()),'seconds.\r')),
            #sys.stdout.flush()
    def load_obj(name,noisy=True):
        assert_disk_locations([pname(name)])
        if noisy:
            timer = Timer()
            print(d2s('Loading',name,'. . .\r')),
            #sys.stdout.flush()
        if name.endswith('.pkl'):
            name = name[:-len('.pkl')]
        assert_disk_locations(name+'.pkl')
        with open(name + '.pkl', 'rb') as f:
            o = pickle.load(f)
            if noisy:
                print(d2s('. . . loaded in',dp(timer.time()),'seconds.\r')),
                #sys.stdout.flush()
            return o
            
    lo = load_obj

    def loD(name,noisy=True):
        return load_obj(opjD(name),noisy)

    def so(arg1,arg2,noisy=True):
        try:
            if type(arg1) == str and type(arg2) != str:
                save_obj(arg2,arg1,noisy)
                return
            if type(arg2) == str and type(arg1) != str:
                save_obj(arg1,arg2,noisy)
                return
            if type(arg2) == str and type(arg1) == str:
                pd2s('def so(arg1,arg2): both args cannot be strings')
            assert(False)
        except:
            exec(EXCEPT_STR)

    def soD(arg1,arg2,noisy=True):
        try:
            if type(arg1) == str and type(arg2) != str:
                save_obj(arg2,opjD(arg1),noisy)
                return
            if type(arg2) == str and type(arg1) != str:
                save_obj(arg1,opjD(arg2),noisy)
                return
            if type(arg2) == str and type(arg1) == str:
                pd2s('def so(arg1,arg2): both args cannot be strings')
            assert(False)
        except:
            exec(EXCEPT_STR)




    try:
        from filelock import Timeout, FileLock
        def soL(arg1,arg2,noisy=True):
            try:
                if type(arg1) == str and type(arg2) != str:
                    name = arg1
                    obj = arg2
                elif type(arg2) == str and type(arg1) != str:
                    name = arg2
                    obj = arg1
                elif type(arg2) == str and type(arg1) == str:
                    pd2s('def so(arg1,arg2): both args cannot be strings')
                    assert(False)
                else:
                    assert(False)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

            lock_path = name + '.lock'
            lock = FileLock(lock_path, timeout=1)

            while True:
                try:
                    lock.acquire()
                    save_obj(obj,name,noisy)
                    lock.release()
                    break
                except Timeout:
                    print("Another instance of this application currently holds the lock.")


        def loL(name,noisy=True):
            lock_path = name + '.lock'
            lock = FileLock(lock_path, timeout=1)
            while True:
                try:
                    lock.acquire()
                    o = load_obj(name,noisy)
                    lock.release()
                    return o
                except Timeout:
                    print("Another instance of this application currently holds the lock.")


        def loState():
            return loL(opjk('__local__/State'))

        def soState(State):
            try:
                Original_state = lo(opjk('__local__/State'))
            except:
                Original_state = {}
            for k in State:
                Original_state[k] = State[k]
            os.system(d2s('mkdir -p',opjk('__local__')))
            os.system(d2s('touch',opjk('__local__/__init__.py')))
            soL(Original_state,opjk('__local__/State'))
    except:
        print("unable to import filelock")




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


if False:
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

if False:
    def zscore(m,thresh=np.nan,all_values=False):
        m_mean = np.mean(m)
        z = m - m_mean
        m_std = np.std(m)
        z /= m_std
        if not np.isnan(thresh):
            z[z < -thresh] = -thresh
            z[z > thresh] = thresh
        if all_values:
            return z,m_mean,m_std
        else:
            return z

if False:
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



if False:
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

    def say(t,rate=150,print_text=False):
        if print_text or not using_osx():
            spd2s(t)
        if using_osx():
            unix(d2s('say -v Susan --interactive=/green -r',rate,t))



    def code_to_code_str(path,start='symbols'):#start=-1,stop=-1):
        code = txt_file_to_list_of_strings(path)

        if start == 'symbols':
            for i in range(len(code)):
                if code[i] == '#'+'#'+'#'+'start':
                    start = i+1
                    srpd2s('found start',start)
                if code[i] == '#'+'#'+'#'+'stop':
                    stop = i+1
                    srpd2s('found stop',i)

        elif (start<0):
            start,stop = input('start,stop ')
            for i in range(len(code)):
                pd2s(i,')',code[i])
        srpd2s('code_to_clipboard(code,',start,stop,')')
        _code_to_clipboard(code,start,stop)

    c2cs = code_to_code_str

    def _code_to_clipboard(code,start,stop):
        try:
            import pyperclip
        except:
            print("Failed: import pyperclip")
            assert False
        code_str = '\n'.join(code[start:stop])
        cprint(code_str,'yellow')
        if using_osx():
            setClipboardData(code_str)
        else:
            pyperclip.copy(code_str)
        print('\nOkay, it is in the clipboard')




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

if False:
    def fn(path):
        """
        get filename part of path
        """
        return path.split('/')[-1]


if False:
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


if False:
    class Timer:
        def __init__(self, time_s=0):
            self.time_s = time_s
            self.start_time = time.time()
            self.count = 0
        def check(self):
            #self.count += 1
            if time.time() - self.start_time > self.time_s:
                return True
            else:
                return False
        def c(self):
            return self.check()
        def time(self):
            return time.time() - self.start_time
        def reset(self):
            self.start_time = time.time()
            self.count = 0
        def trigger(self):
            self.start_time = 0
            print("*** warning, trigger used ***")
            #raw_enter()
        def freq(self,name='',do_print=True):
            self.count += 1
            if self.check():
                value = self.count/self.time()
                if do_print:
                    pd2s(name,'frequency =',dp(value,2),'Hz')
                self.reset()
                return value
            return False
        def message(self,message_str,color='grey',flush=False):
            if self.check():
                print(message_str+'\r'),
                #sys.stdout.flush()
                self.reset()
        def percent_message(self,i,i_max,flush=False):
            self.message(d2s(i,int(100*i/(1.0*i_max)),'%'),color='white')
        def wait(self):
            while not(self.check()):
                time.sleep(self.time_s/100.0)
            self.reset()    
    Tr = Timer

  


if False:
    def sequential_means(data,nn):
        a = array(data)
        d = []
        x = []
        n = min(len(a),nn)
        for i in range(0,len(a),n):
            d.append(a[i:i+n].mean())
            x.append(i+n/2.)
        return x,d

if False:
    def tab_list_print(l,n=1,color=None,on_color=None):
        for e in l:
            s = ''
            for j in range(n):
                s += '\t'
            cprint(s+e,color,on_color)


if False:
    def start_at(t):
        while time.time() < t:
            time.sleep(0.1)
            print(t-time.time())

if False:
    try:
        import numbers
        def is_number(n):
            if type(n) == bool:
                return False
            if type(n) == type(None):
                return False
            return isinstance(n,numbers.Number)
    except:
        print("Don't have numbers module")



def get_key_sorted_elements_of_dic(d,specific=None):
    ks = sorted(d.keys())
    els = []
    for k in ks:
        if specific == None:
            els.append(d[k])
        else:
            els.append(d[k][specific])
    return ks,els

if False:
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


if False:
    def pythonpaths(paths):
        for p in paths:
            sys.path.append(opjh(p))


    def find_files_recursively(
        src,
        pattern,
        FILES_ONLY=False,
        DIRS_ONLY=False,
        ignore_underscore=False,
    ):
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
                """

                """
                file = opj(root,filename)
                folder = pname(file).replace(src,'')
                if folder not in folders:
                    folders[folder] = []
                folders[folder].append(filename)
                ctr += 1
                if timer.check():
                    print(d2s(time_str('Pretty'),ctr,'matches'))
                    timer.reset()

        #print(folders)
        #print(type(folders))
        if ignore_underscore:
            folders_ = {}
            for f in folders:
                ignore = False
                g = f.split('/')
                for h in g:
                    if h[0] == '_':
                        #cb('ignoring',f)
                        ignore = True
                        break
                if not ignore:
                    folders_[f] = folders[f]
            folders = folders_

        data = {}
        data['paths'] = folders
        data['parent_folders'] = [fname(f) for f in folders.keys()]
        return data


if False:
    def find_index_of_closest(val,lst):
        d = []
        for i in range(len(lst)):
            d.append(abs(lst[i]-val))
        return d.index(min(d))






if False:
    def assert_disk_locations(locations):
        if type(locations) == str:
            locations = [locations]
        for l in locations:
            #print(d2s("Checking for",l))
            if len(gg(l)) < 1:
                if False: # old version
                    srpd2s(d2s("Error:\n",l,"not available!"))
                    if len(l.split('/')) > 0:
                        spd2s('Could not find',l,'!!!!!!!!!!')
                        raise ValueError(d2s('Could not find',pname(l),'!!!!!!!!!!'))
                #srpd2s(d2s("Error:\n",l,"not available!"))
                #if len(l.split('/')) > 0:
                #   spd2s('Could not find',l,'!!!!!!!!!!')
                raise ValueError(d2s('Could not find',l))
            #assert(False)
            #print(d2s(l,'is there.\n'))




    def h5r(filename,assert_exists=True):
        if assert_exists:
            assert_disk_locations(filename)
        return h5py.File(filename,'r')
    def h5w(filename):
        assert_disk_locations(pname(filename))
        return h5py.File(filename,'w')
    def h5rw(filename):
        assert_disk_locations(pname(filename))
        return h5py.File(filename,'r+')



def even_len(d):
    l = d['l']
    return np.mod(len(l),2) == 0

if False:
    def is_even(q):
        if np.mod(q,2) == 0:
            return True
        return False



















"""
def img_to_img_uint8(d):
    img = d['img']
    return (255.0*z2o(img)).astype(np.uint8)
"""




















if False:

    def str_is_int(s):
        try:
            int(s)
            return True
        except:
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

if False:
    def clear_screen():
        print(chr(27) + "[2J")

#####################################################
#

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
        if a[0] == '-':
            assert a[0] == '-'
            assert a[1] == '-'
            a = a[2:]
        else:
            pd2s('*** Warning, argument',"'"+k+"'",'not proceeded by -- on command line ***')
            raw_enter()
        if str_is_int(ar):
            Arguments[a] = int(ar)
        elif ',' in ar:
            Arguments[a] = ar.split(',')
        else:
            Arguments[a] = ar

def setup_Default_Arguments(Defaults):
    for k in Arguments:
        if k not in Defaults:
            cr("*** Warning, unexpected argument","'"+k+"'",'***',ra=1)
    for k in Defaults:
        if k not in Arguments:
            Arguments[k] = Defaults[k]
    if 'help' in Arguments:
        if Arguments['help']:
            print("\nDefault Arguments")
            for k in sorted(Defaults):
                print(d2n('\t',k,':\t',Arguments[k]),' (',type(Arguments[k]),')')
            print("")
            sys.exit()              

def print_Arguments():
    if len(Arguments) > 0:
        cg("\nArguments",sf=0)
        for k in Arguments:
            cy(d2n('\t',k,':',Arguments[k],' (',type(Arguments[k]),')'),sf=0)
    else:
        cb('No Arguments')

def set_Argument_defaults(Arguments,Defaults):
    for k in Defaults:
        if k not in Arguments:
            Arguments[k] = Defaults[k]

def require_Arguments(arglst):
    fail = False
    for a in arglst:
        if a not in Arguments:
            cr("***",__file__,"lacking command line argument ","'"+a+"'")
            fail = True
    if fail:
        cr("Required arguments are:",arglst)
        sys.exit(-1)

#
if False:
    #####################################################
    identify_file_str_future = """
    from __future__ import division
    from __future__ import print_function
    if '__file__' not in locals():
        __file__ = 'INTERPRETER'
    cprint('using '+__file__,'yellow')
        """
    #exec(identify_file_str_future)
    #
    #####################################################




if False:
    def find_nearest(array,value):
        """
        https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        """
        idx = (np.abs(array-value)).argmin()
        return array[idx]





    def bound_value(the_value,the_min,the_max):
        if the_value > the_max:
            return the_max
        elif the_value < the_min:
            return the_min
        else:
            return the_value






if False:
    def intr(n):
        return np.int(np.round(n))


if False:
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

    if using_osx():
        pass#CS_('using OS X')
    elif using_linux():
        pass#CS_('using linux')
    else:
        CS_('using UNKNOWN system')


    try:
        import rospy
        HAVE_ROS = True
        #CS_('HAVE_ROS = True')
    except:
        HAVE_ROS = False
        #CS_('HAVE_ROS = False')

    try:
        #cs('username =',username)
        if username == 'nvidia':
            HAVE_GPU = True
            #CS_('HAVE_GPU = True')
        else:
            #unix('nvidia-smi',print_stdout=True)
            HAVE_GPU = True
            #CS_('HAVE_GPU = True')
    except:
        HAVE_GPU = False
        #CS_('HAVE_GPU = False')





if False:
    def internet_on():
        """
        https://stackoverflow.com/questions/3764291/checking-network-connection
        """
        import urllib2
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=1)
            return True
        except urllib2.URLError as err: 
            return False

    def internet_on_thread(P_):
        spd2s("__internet_on_thread")
        timer = Timer(2)
        if 'ABORT' not in P_:
            P_['ABORT'] = False
        if 'internet_on' not in P_:
            P_['internet_on'] = False
        try:
            while P_['ABORT'] == False:
                if timer.check():
                    P_['internet_on'] = internet_on()
                    timer.reset()
                else:
                    time.sleep(1)
        except Exception as e:
            srpd2s("__internet_on_thread",e)
            time.sleep(1)

if False: # as example
    threading.Thread(target=internet_on_thread,args=[P,]).start()








if False:
    def percent_disk_free(disk='/'):
        statvfs = os.statvfs(disk)
        size_of_filesystem_in_bytes = statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
        #print statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
        number_of_free_bytes_that_ordinary_users_have = statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users
        percent_free = dp(100*number_of_free_bytes_that_ordinary_users_have/(1.0*size_of_filesystem_in_bytes))
        return percent_free

if True:
    def memory():
        """
        Get node total memory and memory usage
        http://stackoverflow.com/questions/17718449/determine-free-ram-in-python
        """
        if using_osx():
            import psutil
            m = psutil.virtual_memory()
            return m.percent
        else:
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
    def format_row(list_of_sym_percent_pairs):
        __,ncols = get_terminal_size()
        row_str = ''
        for i in range(ncols):
            for sp in list_of_sym_percent_pairs:
                sym = sp[0]
                per = sp[1]
                if per < 0:
                    per = 0.
                elif per > 99:
                    per = 99.
                col = int(per/100.*ncols)
                if i == col:
                    row_str += sym
                    break
            else:
                row_str += ' '
        return row_str
    def Progress_animator(total_count,update_Hz=1.0,message=''):
        from kzpy3.misc.progress import ProgressBar2
        D = {}
        D['total_count'] = total_count
        D['progress'] = ProgressBar2(total_count,message=' '+message+': ') 
        D['progress timer'] = Timer(1.0/(1.0*update_Hz))
        def _update_function(current_count):
            if True:
                if D['progress timer'].check():
                    #print 'CCC'
                    assert current_count < D['total_count']+1
                    D['progress'].animate(current_count)
                    D['progress timer'].reset()
                else:
                    pass#time.sleep(0.1)
            else:#except Exception as e:
                pass
        D['update'] = _update_function
        return D


if False:
    def project_path__to__project_import_prefix(project_path):
        project_path = project_path.replace(opjh(),'')
        a = project_path.split('/')
        c = []
        for b in a:
            if len(b) > 0:
                c.append(b)
        project_import_prefix = '.'.join(c)
        return project_import_prefix




if False:
    def try_to_close(lst):
        for l in lst:
            try:
                l.close()
                cy('closed')
            except: pass









if False:
    # These are not utils, but may be used widely

    Behavioral_mode_code = {
        'left':110,
        'right':111,
        'direct':112,
    }
    Behavioral_code_to_mode = {}
    for k in Behavioral_mode_code.keys():
        Behavioral_code_to_mode[Behavioral_mode_code[k]] = k


def open_run(run_name,h5py_path=None,Runs_dic=None,want_list=['L','O','F'],verbose=False):
    #cb("run_name =",run_name,"h5py_path =",h5py_path)
    if h5py_path != None:
        path = h5py_path
        #cb("A) path =",path)
    elif Runs_dic != None:
        path = pname(Runs_dic[run_name])
        #cb("B) path =",path)
    else:
        #cb('C)')
        cr("*** Can't open run",run_name,"because h5py_path=None and Runs_dic=None ***")
        return False,False,False
    files = sggo(path,run_name,"*.h5py")
    if len(files) < 3:
        cr("*** Can't open run",run_name,"because len(files) < 3 ***")
        return False,False,False
    Files = {'L':None,'O':None,'F':None,}
    File_names = {'L':'left_timestamp_metadata','O':'original_timestamp_data','F':'flip_images',}
    for n in File_names:
        if n not in want_list:
            continue
        for f in files:
            if File_names[n] in fname(f):
                if verbose:
                    cg('found',f)
                Files[n] = h5r(f)
    for n in Files:
        if Files[n] == None and n in want_list:
            cr("*** Error, lacking",n)
            return False,False,False
    return Files['L'],Files['O'],Files['F']


    

def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows),int(columns)


second = 1.0
seconds = second
minute = 60*seconds
minutes = minute
hour = 60*minutes
hours = hour
day = 24*hours
days = day








if False:
    def sort_dir_by_ctime(dir_path):
        """
        https://www.w3resource.com/python-exercises/python-basic-exercise-71.php
        """
        from stat import S_ISREG, ST_MTIME, ST_MODE
        import os, sys, time
        data = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
        data = ((os.stat(path), path) for path in data)
        # regular files, insert creation date
        data = ((stat[ST_MTIME], path)
                   for stat, path in data if S_ISREG(stat[ST_MODE]))
        paths = []
        for cdate, path in sorted(data):
            paths.append(path)
        return paths



def getch():
    import sys, termios, tty, os, time
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if False:
    def sort_by_column(a,col,reverse=False):
        a = na(a)
        if reverse:
            a *= -1
        a = a[a[:,col].argsort()]
        if reverse:
            a *= -1
        return a
    

if False:
    def key_get_set(D,key_list,value=None):
        key = key_list.pop(0)
        assert key in D.keys()
        if len(key_list) == 0:
            if value != None:
                D[key] = value
                return value
            else:
                return D[key]
        else:
            return key_get_set(D[key],key_list,value)
    kg = key_get_set


# https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
from functools import reduce  # forward compatibility for Python 3
import operator
def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)
def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
def key_get_set(D,key_list,value=None):
    """
    Get or set value in dictionary with list of keys.

    e.g.s,
        Q = {1:{2:{3:4}}}
        print(Q)
        print(kg(Q,[1,2,3]))
        print(Q)
        print(kg(Q,[1,2,3],{4:5}))
        print(Q)
        keys = [1,2,3]
        print(kg(Q,keys+[4]))
        print(kg(Q,(keys,4)))
        kg(Q,(keys,4),10)
        print(Q)
    """
    if type(key_list) == tuple:
        key_list = key_list[0] + [key_list[1]]
    if value == None:
        return getFromDict(D,key_list)
    else:
        setInDict(D,key_list,value)
        return value
kg = key_get_set

#,a
if False:
    def get_code_snippet():
        code_file = most_recent_py_file()
        code_lst = txt_file_to_list_of_strings(code_file)
        snippet_lst = []
        started = False
        for c in code_lst:
            if not started and c == '#,a':
                started = True
            if started and c == '#,b':
                break
            if started:
                snippet_lst.append(c)
        setClipboardData('\n'.join(snippet_lst))
        cb('setClipboardData() from',code_file)

    gsp = get_code_snippet

    def most_recent_py_file(path=opjk(),return_mtime=False):
        max_mtime = 0
        for dirname,subdirs,files in os.walk(path):
            for fname in files:
                if len(fname) >= 3:
                    if fname[-3:] == '.py':
                        full_path = os.path.join(dirname,fname)
                        mtime = os.stat(full_path).st_mtime
                        if mtime > max_mtime:
                            max_mtime = mtime
                            max_dir = dirname
                            max_file = fname
        if return_mtime:
            return opj(max_dir,max_file),max_mtime
        else:
            return opj(max_dir,max_file)
#,b
if False:
    def file_modified_test(path,mtime_prev):
        mtime = os.path.getmtime(path)
        if mtime > mtime_prev:
            return mtime
        else:
            return 0




if False:

    def date_and_time_setting_strings():
        now = datetime.datetime.now()
        date_str = now.strftime('20%y%m%d')
        time_str = now.strftime('%H:%M:%S')
        date_str = "sudo date +%Y%m%d -s "+date_str
        time_str = "sudo date +%T -s "+time_str
        return date_str,time_str

    def ssh_date_time(host_ip,user='nvidia',timeout=10):
        date_str,time_str = date_and_time_setting_strings()
        sys_str = d2n('ssh -o ConnectTimeout=',timeout,' ',user+'@'+host_ip," '",date_str,'; ',time_str,"'")
        print(sys_str)
        os.system(sys_str)

    def rsync(ip,user='nvidia',timeout=10):
        os.system("rsync -ravL --exclude '*.pyc' --exclude '*.pkl' kzpy3/* nvidia@"+ip+":kzpy3/")
        cprint(d2s(ip,'finished.'),'white','on_blue')
        beep()

    def update_TXs(ips=[]):
        for ip in ips:
            threading.Thread(target=rsync,args=[ip]).start()

    def update_TXs_range(start,stop=None,base_ip='169.254.131'):
        if stop == None:
            stop = start+1
        ips = []
        for i in range(start,stop):
            ips.append(d2n(base_ip,'.',i))
        update_TXs(ips)





identify_file_str = """
if '__file__' not in locals():
    __file__ = 'INTERPRETER'
cprint('using '+__file__,'yellow')
CVerbose = {}
CShowFile = {}
cfile = fname(__file__)#.replace(opjk(),'').replace(opjh(),'')
cstr = "CVerbose['COLOR'] = True\\n"+\
    "CShowFile['COLOR'] = True\\n"+\
    "def cQ(*args,**kwargs):\\n"+\
    "\tif not CVerbose['COLOR']:\\n"+\
    "\t\treturn\\n"+\
    "\tif CShowFile['COLOR']:\\n"+\
    "\t\tccfile = '('+cfile+')'\\n"+\
    "\telse:\\n"+\
    "\t\tccfile = ''\\n"+\
    "\tif 'sf' in kwargs and not kwargs['sf']:\\n"+\
    "\t\tscf = ''\\n"+\
    "\telse:\\n"+\
    "\t\tscf = \tccfile\\n"+\
    "\tcprint(d2s_spacer(tuple(list(args)+['\t'+scf]),spacer=' '),'COLOR')\\n"+\
    "\tif 'ra' in kwargs:\\n"+\
    "\t\tif kwargs['ra'] == 1:\\n"+\
    "\t\t\tcprint('\b  (hit Enter to continue)','COLOR')\\n"+\
    "\t\t\traw_input()\\n"+\
    "\tif 't' in kwargs:\\n"+\
    "\t\tif kwargs['t'] > 0:\\n"+\
    "\t\t\ttime.sleep(kwargs['t'])\\n"
for color in ['red','yellow','green','blue','magenta','cyan','white','Grey']:
    an_exec_string = cstr.replace('Q',color[0]).replace('COLOR',color).replace('Grey','grey')
    exec(an_exec_string)
    """

exec(identify_file_str)

#EOF
