if False:
    M = {
        'text':'Warning, meltdown in progress!',
        'period': 5,
        'till': 151239,
        'filename':'m293.py'
    }
    say(M['text'])

    Ms = {
        M['text']:M
    }


    def key_access(Dic,keys,start=True):
        if start:
            keys_copy = []
            for k in Dic['current_keys']:
                keys_copy.append(k)
            keys = keys_copy
        key = keys.pop(0)
        assert key in Dic.keys()
        if type(Dic[key]) == dict and len(keys) > 0:
            return key_access(Dic[key],keys,start=False)
        else:
            return Dic[key]



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
if False:
    Q = {1:{2:{3:4}}}
    print Q
    print kg(Q,[1,2,3])
    print Q
    print kg(Q,[1,2,3],{5:6})
    print Q


#,
print 'hi there!'
#,

#,
from kzpy3.vis3 import *
import kzpy3.Array.Array
CA()
hz = Timer(1)
tt = Timer(1/30.)
U = kzpy3.Array.Array.Array(300,2)

U['setup_plot'](
    height_in_pixels=100,
    width_in_pixels=600,
    x_origin_in_pixels=300,
    pixels_per_unit=1,
)

for i in range(0,100000,5):
    while not tt.check():
        time.sleep(0.001)
    tt.reset()
    hz.freq()
    U['append'](
        na([i/5.,100/2.*np.sin(2*i/100.)]),
        None,
        {'time':time.time()},
    )

    #U['check_ts'](1)
    #print U['array'][U['ctr']-1,0]
    d = U['array'][U['ctr']-1,0]
    #print U['array'][U['ctr']-1,:]
    U['array'][:U['ctr'],0] -= d
    #if np.mod(i,15) == 0:
        
    U['show'](
        use_CV2_plot=True,
        use_maplotlib=False,
        do_print=False,
        clear=True,
        color=(255,255,0),
        code=None,
        show=True,
        grid=False,
        scale=1.0,
    )

    U['array'][:U['ctr'],0] += d
    #spause()
    #time.sleep(0.1)
#,b
#,a
'al'
print 'asdfsadfas'
def doit():
    code_file = most_recent_py_file()
    code_lst = txt_file_to_list_of_strings(code_file)
    snippet_lst = []
    started = False
    for c in code_lst:
        #print c,c == '#,a'
        if not started and c == '#,a':
            started = True
        if started and c == '#,b':
            break
        if started:
            snippet_lst.append(c)
    setClipboardData('\n'.join(snippet_lst))

#,
print 'joe'
def most_recent_py_file(path=opjk()):
    print 'hi'
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
    return opj(max_dir,max_file)
#,b
#EOF