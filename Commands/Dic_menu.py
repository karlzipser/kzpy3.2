#!/usr/bin/env python
from kzpy3.vis3 import *
import colored
exec(identify_file_str)
for k in CShowFile.keys():
    CShowFile[k] = False


def Default_Values(Q,project_path,parent_keys=[],read_only=False):
    D = {}
    os.system('mkdir -p '+opj(project_path,'__local__'))
    D['project_path'] = project_path
    D['.pkl'] = opj(project_path,'__local__','default_values.pkl')
    
    D['parent_keys'] = parent_keys
    D['current_keys'] = ['Q']
    D['Q'] = Q
    D['read_only'] = read_only
    if not read_only:
        os.system('rm '+D['.pkl'])
    add_keys(D,D['Q'])
    def function_save():
        if D['read_only']:
            return
        save_C(D['Q'],D['project_path'])
    def function_load():
        load_C(D['Q'],D['project_path'])
        add_keys(D,D['Q'])
    def function_up():
        if len(D['current_keys']) > 0:
            D['current_keys'].pop()
            return {
                'message':  'went up',
                'action':   'success',
            }
        else:
            return {
                'message':  d2s('***','cannot go up.'),
                'action':   'failure',
            }
    def function_down(key):
        K = key_access(D,D['current_keys'])
        if key in K and type(K[key]) == dict:
            D['current_keys'].append(key)
            return {
                'message':  d2s('down to',key),
                'action':   'success',
            }
        else:
            return {
                'message':  d2s('***',key,'not there, cannot go down to it.'),
                'action':   'failure',
            } 

    def function_show(message=''):
        clear_screen()
        print D['project_path'].replace(opjh(),'')
        return show_menu(key_access(D,D['current_keys']),message)

    def function_menu():
        message = ''
        if not D['read_only']:
            D['save']()
        while True:
            D['load']()
            items = D['show'](message)
            while True:
                R = make_choice(items)
                if R['message'] != 'ran python':
                    break
            if R['action'] == 'quit':
                cw("\ndone.\n")
                return #sys.exit()
            elif R['action'] == 'failure':
                message = R['message']
                continue
            elif R['action'] == 'continue':
                message = R['message'] #'continue'
                continue
            elif R['action'] == 'choose':
                
                if R['message'] == '<up>':
                    S = D['up']()
                    message = S['message']
                    cb('S =',S)
                elif R['message'] == '<top>':
                    message = 'already at <top>'
                else:
                    S = D['down'](R['message'])
                    message = S['message']
                    if S['action'] == 'success':
                        continue
                    else:
                        K = key_access(D,D['current_keys'])
                        message = set_value(D,R['message'])
                        continue



    D['up'] = function_up
    D['down'] = function_down
    D['load'] = function_load
    D['save'] = function_save
    D['show'] = function_show
    D['menu'] = function_menu
    return D


def set_value(D,key):
    K = key_access(D,D['current_keys'])
    if K['--mode--'] == 'const':
        message = d2s(key,'is constant, not changed.')
        return message
    if K['--mode--'] == 'bash':
        os.system(K[key])
        raw_enter()
        message = K[key]
        return message
    if type(K[key]) == bool:
        yes_no = raw_input(d2n("Toggle '",key,"'? ([y]/n) "))
        if yes_no == 'y' or yes_no == '':
            value = not K[key]
        else:
            message = d2n("'",key,"' unchanged")
            return message
    else:
        value = input(d2n("Enter value for '",key,"' (",K[key],"): "))
    if type(value) != type(K[key]):
        message = d2n("*** type(",value,") != type(",K[key],")")
    else:
        K[key] = value
        message = d2n("set '",key,"' to ",value,'')
        D['save']()
    return message


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


def add_keys(D,E,keys=[]):
    E['--keys--'] = keys
    if '--mode--' not in E:
        if D['read_only']:
            E['--mode--'] = 'const'
        else:
            E['--mode--'] = 'var'
    elif D['read_only'] and E['--mode--'] == 'var':
        E['--mode--'] = 'const'

    for k in E.keys():
        if type(E[k]) == dict:
            add_keys(D,E[k],keys+[k])


def load_C(C,project_path,name='default_values'):
    if len(sggo(opj(project_path,'__local__','ready'))) == 0:
        return False
    if len(sggo(opj(project_path,'__local__',name+'.writing.pkl'))) > 0:
        return False
    if len(sggo(opj(project_path,'__local__',name+'.pkl'))) == 0:
        return False
    try:
        D = lo(opj(project_path,'__local__',name+'.pkl'))
    except:
        return False
    if len(sggo(opj(project_path,'__local__','ready'))) == 0:
        return False
    if len(sggo(opj(project_path,'__local__',name+'.writing.pkl'))) > 0:
        return False
    if len(sggo(opj(project_path,'__local__',name+'.pkl'))) == 0:
        return False
    for k in C.keys():
        C[k] = D[k]
    return True


def save_C(C,project_path,name='default_values'):
    try:
        sys_str = d2s('rm',opj(project_path,'__local__','ready'))
        os.system(sys_str)
    except:
        cr(sys_str,"failed")
    so(C,opj(project_path,'__local__',name+'.writing.pkl'))
    time.sleep(0.1)
    try:
        sys_str = d2s('rm',opj(project_path,'__local__',name+'.pkl'))
        print sys_str
        os.system(sys_str)
    except:
        cr(sys_str,"failed")
    sys_str = d2s('mv',opj(project_path,'__local__',name+'.writing.pkl'),opj(project_path,'__local__',name+'.pkl'))
    print sys_str
    os.system(sys_str)
    sys_str = d2s('touch',opj(project_path,'__local__','ready'))
    print sys_str
    os.system(sys_str)    

def is_meta_key(k):
    if len(k) < 2:
        return False
    if k[:2] != '--' and k[-2:] != '--':
        return False
    else:
        return True

def clear_screen():
    cr("\nclear screen\n")

def show_menu(C,message):
    if '--keys--' in C:
        key_list = C['--keys--']
    else:
        key_list = ['no keys']
    cprint(
        '/'+'/'.join(key_list),
        attrs=['bold','reverse'],
        color='white',
        on_color='on_blue'
    ) 
    sorted_keys_ = sorted(C.keys())
    sorted_keys = []
    for k in sorted_keys_:
        if not is_meta_key(k):
            sorted_keys.append(k)
    if len(key_list) == 0:
        s = '<top>'
    else:
        s = '<up>'
    sorted_keys.insert(0,s)
    cc = bl
    for i in rlen(sorted_keys):
        if i == 0 and s == '<top>':
            cb(s)
            continue #return ''
        k = sorted_keys[i]
        val_color = lb
        v = ''
        edited = ''
        if k in C:
            if type(C[k]) == dict:
                ctr = 0
                for l in C[k]:
                    if not is_meta_key(l):
                        ctr += 1
                #v = d2n(ctr)
                v = ''
                cc = wh+underlined
                val_color = wh
            elif is_meta_key(k):
                v = C[k]
                cc = colored.fg('grey_23') 
            elif C['--mode--'] == 'bash':
                cc = og
                v = ''
            elif C['--mode--'] == 'const':
                v = C[k]
                cc = wh
                val_color = wh
            else:
                v = C[k]
                cc = yl

        cb(bl,i,cc+k+colored.attr('res_underlined'),val_color,v,edited)
    cg('$',message)
    return sorted_keys


def Dic_Loader(path,wait_time=0.2):
    D = {}
    if '.pkl' not in path:
        path = path+'.pkl'
    D['path'] = path
    D['mtime_prev'] = -1
    D['wait time'] = wait_time
    D['wait timer'] = Timer(D['wait time'])
    D['Dic'] = None

    def function_load():
        if D['wait timer'].check():
            D['wait timer'].reset()
            if file_modified_test():
                D['Dic'] = lo(D['path'])
                return True
        time.sleep(D['wait time']/2.)
        return False

    def file_modified_test():
        D['mtime'] = os.path.getmtime(D['path'])
        if D['mtime'] > D['mtime_prev']:
            D['mtime_prev'] = D['mtime']
            return True
        return False

    D['load'] = function_load

    return D



def make_choice(sorted_keys):

    raw_choice = raw_input(wh+'choice: '+lb)

    if raw_choice == '':
        return {
            'message':"other commands: 'q' (quit), 'p' (python)",
            'action':'continue',
        }
        
    if raw_choice == 'q':
        return {
            'message':  "\ndone.\n",
            'action':   'quit',
        }

    if raw_choice == 'p':
        menu_python()
        return {
            'message':  "ran python",
            'action':   'continue',
        }

    if str_is_int(raw_choice):
        choice = int(raw_choice)
    else:
        return {
            'message':  d2s("*** choice","'"+raw_choice+"'",'is not an integer'),
            'action':   'failure',
        }

    if choice < 0 or choice+1 > len(sorted_keys):
        return {
            'message':  '*** choice is out of range',
            'action':   'failure',
        }
    key_choice = sorted_keys[choice]

    return {
        'message':  key_choice,
        'action':   'choose',
    }


def menu_python():
    try:
        code = raw_input(d2n("Enter python code: "))
        d = code.split(';')
        if 'print' not in d[-1]:
            d[-1]=d2s('print(',d[-1],')')
        code = ';'.join(d)
        exec(code)
        return ''
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        message = d2s('Exception!',exc_type,file_name,exc_tb.tb_lineno)
        return message


if __name__ == '__main__':

    Default_Args = {
        'menu':True,
        'read_only':False,
        'dic_project_path':opjk('Commands/A'),
    }

    for d in Default_Args:
        if d not in Arguments:
            Arguments[d] = Default_Args[d]

    Dics = {}

    dic_project_path = Arguments['dic_project_path']

    exec_str = d2s(
        'from',
        project_path__to__project_import_prefix(dic_project_path)+'.default_values',
        'import Q',
    )
    exec(exec_str)

    Dics[dic_project_path] = \
        Default_Values(Q,dic_project_path,read_only=Arguments['read_only'])

    if Arguments['read_only']:
        Dics[dic_project_path]['load']()

    if Arguments['menu']:
        Dics[dic_project_path]['menu']()





#EOF


    




