from kzpy3.utils.times import *
from kzpy3.utils.printing2 import *

"""
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
"""





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



def project_path__to__project_import_prefix(project_path):
    project_path = project_path.replace(opjh(),'')
    a = project_path.split('/')
    c = []
    for b in a:
        if len(b) > 0:
            c.append(b)
    project_import_prefix = '.'.join(c)
    return project_import_prefix

def file_modified_test(path,mtime_prev):
    mtime = os.path.getmtime(path)
    if mtime > mtime_prev:
        return mtime
    else:
        return 0

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




def save_obj(obj, name,noisy=True,show_time=False,use_real_path=True):
    assert_disk_locations([pname(name)])
    name = name.replace('.pkl','')
    name = name + '.pkl'
    if use_real_path:
        name = os.path.realpath(name)
    with open(name + '.pkl', 'wb') as f:
        if use_real_path:
            f = os.path.realpath(f)
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    if noisy:
        timer = Timer()
        a = cf('. . . saved','`',name+'.pkl','`--rb')
        if show_time:
            b = d2s('`','in',dp(timer.time()),'seconds.\r')
        else:
            b=''
        clp(a,b)
        #sys.stdout.flush()
def load_obj(name,noisy=True,time=False,use_real_path=True):
    assert_disk_locations([pname(name)])
    if noisy:
        timer = Timer()
        clp('Loading','`',name,'`--rb','. . .\r'),

        #sys.stdout.flush()
    #if name.endswith('.pkl'):
    #    name = name[:-len('.pkl')]
    #print name
    name = name.replace('.pkl','')
    name = name + '.pkl'
    if use_real_path:
        name = os.path.realpath(name)
    assert_disk_locations(name)
    with open(name, 'rb') as f:
        o = pickle.load(f)
        if noisy:
            clp(d2s('. . . loaded in',dp(timer.time()),'seconds.\r')),
            #sys.stdout.flush()
        return o
        
lo = load_obj

def loD(name,noisy=True,use_real_path=True):
    if use_real_path:
        name = os.path.realpath(name)
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




def pythonpaths(paths):
    for p in paths:
        sys.path.append(opjh(p))










def find_files_recursively(
    src,
    pattern,
    FILES_ONLY=False,
    DIRS_ONLY=False,
    ignore_underscore=True,
    ignore_Trash=True,
    followlinks=True,
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
    print(d2n('src =' ,src,', pattern = ',"\"",pattern,"\""))
    for root, dirnames, filenames in os.walk(src,followlinks=followlinks):
        assert(not(FILES_ONLY and DIRS_ONLY))
        if FILES_ONLY:
            use_list = filenames
        elif DIRS_ONLY:
            use_list = dirnames
        else:
            use_list = filenames+dirnames
        for filename in fnmatch.filter(use_list, pattern):
            file_ = opj(root,filename)
            folder = pname(file_).replace(src,'')
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(filename)
            ctr += 1
            if timer.check():
                print(d2s(time_str('Pretty'),ctr,'matches'))
                timer.reset()
    if ignore_underscore:
        folders_ = {}
        for f in folders:
            ignore = False
            if ignore_Trash:
                if 'Trash' in f:
                    ignore = True
            g = f.split('/')
            for h in g:
                if len(h) > 0:
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
    data['src'] = src
    data['pattern'] = pattern
    pd2s(ctr,'matches,',len(data['parent_folders']),'parent folders.')
    return data




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


def try_to_close(lst):
    if type(lst) == str:
        lst = [lst]
    for l in lst:
        try:
            l.close()
            cy('closed')
        except: pass


def h5r(filename,assert_exists=True,use_real_path=True):
    if use_real_path:
        filename = os.path.realpath(filename)
    if assert_exists:
        assert_disk_locations(filename)
    return h5py.File(filename,'r')
def h5w(filename,use_real_path=True):
    if use_real_path:
        filename = os.path.realpath(filename)
    assert_disk_locations(pname(filename))
    return h5py.File(filename,'w')
def h5rw(filename,use_real_path=True):
    if use_real_path:
        filename = os.path.realpath(filename)
    assert_disk_locations(pname(filename))
    return h5py.File(filename,'r+')


def save_as_h5py(file_path,D,dtype='float16'):
    F = h5w(file_path)
    clp('writing topics to',file_path)
    for k in D.keys():
        D[k] = na(D[k])
        clp('    ',k,len(D[k]))
        if type(dtype) == dict:
            dt = dtype[k]
        else:
            dt = dtype
        F.create_dataset(k,data=D[k],dtype=dt)
    F.close()
    clp('done.')


def percent_disk_free(disk='/'):
    statvfs = os.statvfs(disk)
    size_of_filesystem_in_bytes = statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
    #print statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
    number_of_free_bytes_that_ordinary_users_have = statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users
    percent_free = dp(100*number_of_free_bytes_that_ordinary_users_have/(1.0*size_of_filesystem_in_bytes))
    return percent_free


def find_h5py_path(run_name):
    H = find_files_recursively(opjD('Data'),run_name,DIRS_ONLY=True)
    h5py_path = None
    for p in H['paths']:
        if fname(p) == 'h5py':
            h5py_path = opj(H['src'],p)
            break
    assert h5py_path is not None
    return h5py_path

def make_path_and_touch_file(path):
    os.system('mkdir -p '+pname(path))
    os.system('touch '+path)

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

def open_run2(run_name,Runs_dic=None,want_list=['L','O','F'],verbose=False):
    h5py_path = find_h5py_path(run_name)
    L,O,F = open_run(run_name,h5py_path=h5py_path,want_list=want_list,verbose=verbose)
    return L,O,F

def backup_folder(
    src=opjh('kzpy3')+'/',
    dst=opjh('_kzpy3_older','kzpy3_'+time_str())+'/'
    ):
    """
    Make a time marked backup, with default as kzpy3.
    """
    os.system('mkdir -p ' + dst)
    #os.system(d2s('cp -r',src,dst))
    os.system(d2s("rsync -ravL --exclude '*.pyc' --exclude '*.pkl'", src, dst))


def stowe_Desktop(dst=False):
    if dst==False:
        dst = opjh('Desktops_older','Desktop_'+time_str())
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
exec(identify_file_str)





def make_kzpy3_links():
    a = sggo(opjk('*'))
    for b in a:
        if os.path.isdir(b):
            c = fname(b)
            s = d2s('ln -s',b,c)
            print s
            os.system(s)







#EOF
