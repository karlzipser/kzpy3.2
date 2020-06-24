from kzpy3.utils.files import *
#from kzpy3.utils.printing import *
#,a
try:
    import pyperclip
except:
    print("Failed: import pyperclip")
#,b
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
    #print snippet_lst

    code_str = '\n'.join(snippet_lst)
    if using_osx():
        setClipboardData(code_str)
    else:
        pyperclip.copy(code_str)
    clp('set clipboard from','`',
        cf(pname(code_file)+'/','`--d',fname(code_file),'`--b',s1=''),
        cf('(',len(snippet_lst),' lines)','`y-d',s0='')
    )
    if len(snippet_lst) == 0:
        clp('*** No code snippet. Did you use #,a and #,b ? ***','`r-b')
    #else:
    #    clp('\t',len(snippet_lst),'lines')

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


#exec(identify_file_str)

#EOF
