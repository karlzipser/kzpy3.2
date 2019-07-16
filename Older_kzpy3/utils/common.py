from __future__ import print_function  # print('me') instead of print 'me'
from __future__ import division  # 1/2 == 0.5, not 0

import_list = ['os','os.path','shutil','scipy','scipy.io','string','glob','time','sys','datetime','random','re',
    'subprocess','threading','serial','inspect','fnmatch','h5py','socket','getpass','numbers','math']#,'importlib']
import_from_list = [['FROM','pprint','pprint'],['FROM','termcolor','cprint']]
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

rnd = np.random.random
rndint = np.random.randint
rndn = np.random.randn
rndchoice = np.random.choice
na = np.array
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
shape = np.shape
randint = np.random.randint
randn = np.random.randn
zeros = np.zeros
ones = np.ones
reshape = np.reshape
mod = np.mod
array = np.array


from utils.printing import *
from utils.have_using import *

def fname(path):
    return path.split('/')[-1]

def pname(path):
    p = path.split('/')[:-1]
    pstr = ""
    for s in p:
        if len(s)>0:
            pstr += '/' + s
    return pstr


def raw_enter(optional_str=''):
    return raw_input(optional_str+'Hit enter to continue > ')


def is_even(q):
    if np.mod(q,2) == 0:
        return True
    return False
    

def str_is_int(s):
    try:
        int(s)
        return True
    except:
        return False

def rlen(a):
    return range(len(a))

def dic_is_type(Dic,type_str):
    assert type(Dic) == dict
    assert type(type_str) == str
    if 'type' in Dic.keys():
        if Dic['type'] == type_str:
            return True
    return False

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
    





def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]








   




def dict_to_sorted_list(d):
    l = []
    ks = sorted(d.keys(),key=natural_keys)
    for k in ks:
        l.append(d[k])
    return l


def advance(lst,e,min_len=1):
    len_lst = len(lst)
    if len_lst < min_len:
        pass
    elif len_lst > 1.2*min_len:
        lst = lst[-min_len:]
    else:
        lst.pop(0)
    lst.append(e)

def a_key(dic):
    keys = dic.keys()
    k = np.random.randint(len(keys))
    return keys[k]

def an_element(dic):
    return dic[a_key(dic)]

def get_key_sorted_elements_of_dic(d,specific=None):
    ks = sorted(d.keys())
    els = []
    for k in ks:
        if specific == None:
            els.append(d[k])
        else:
            els.append(d[k][specific])
    return ks,els

def even_len(d):
    l = d['l']
    return np.mod(len(l),2) == 0



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

def nvidia_smi_continuous(t=0.1):
    while True:                                     
        unix('nvidia-smi',print_stdout=True)
        time.sleep(t)














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
            print(Args)
            pd2s('*** Warning, argument',"'"+k+"'",'not proceeded by -- on command line ***')
            #raw_enter()
        if str_is_int(ar):
            Arguments[a] = int(ar)
        elif ',' in ar:
            Arguments[a] = ar.split(',')
        else:
            Arguments[a] = ar

def setup_Default_Arguments(Defaults):
    for k in Arguments:
        if k not in Defaults:
            cr("*** Warning, unexpected argument","'"+k+"'",'***')
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

