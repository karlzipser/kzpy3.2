#!/usr/bin/env python
from kzpy3.vis3 import *
import colored
exec(identify_file_str)
for k in CShowFile.keys():
    CShowFile[k] = False


def Default_Values(Q,project_path,parent_keys=[]):
    D = {}
    os.system('mkdir -p '+opj(project_path,'__local__'))
    D['project_path'] = project_path
    D['.pkl'] = opj(project_path,'__local__','default_values.pkl')
    os.system('rm '+D['.pkl'])
    D['parent_keys'] = parent_keys
    D['current_keys'] = []
    D['Q'] = Q
    D['R'] = {}
    add_keys(D,D['Q'])
    def function_save():
        save_C(D['Q'],D['project_path'])
    def function_load():
        load_C(D['Q'],D['project_path'])
        D['R'] = {}
        add_keys(D,D['Q'])
    D['load'] = function_load
    D['save'] = function_save
    D['show'] = show_menu(D['R']['/'.join(D['current_keys'])])
    return D


def add_keys(D,E,keys=[]):
    key_path = '/'.join(keys)
    if len(key_path) > 0:
        D['R'][key_path] = E
    else:
        D['R'] = {}
    E['--keys--'] = keys
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
    print 1
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





def show_menu(C):
    clear_screen()
    if '--keys--' in C:
        key_list = C['--keys--']
    else:
        key_list = ['no keys']
    cprint(
        '/'.join(key_list),
        attrs=['bold','reverse'],
        color='white',
        on_color='on_blue'
    ) 
    sorted_keys_ = sorted(C.keys())
    sorted_keys = []
    for k in sorted_keys_:
        if len(k) < 2 or (len(k) > 2 and k[:2] != '--' and k[-2:] != '--'):
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
            continue
        k = sorted_keys[i]
        val_color = lb
        if k in C:
            if type(C[k]) == tuple and C[k][0] == 'active':
                cc = og
            elif type(C[k]) == tuple and C[k][0] == 'python':
                cc = lb
            elif type(C[k]) == tuple and C[k][0] == 'path':
                cc = gr+underlined
            elif type(C[k]) == tuple and C[k][0] == 'const':
                cc = colored.fg('grey_23')
                val_color = cc
            elif type(C[k]) == dict:
                cc = wh+underlined
            else:
                cc = yl
        v = ''
        edited = ''
        if k in C:
            if type(C[k]) == tuple:
                if C[k][0] == 'set value' or C[k][0] == 'const':
                    v = C[k][1]
                    if len(C[k]) > 2:
                        if C[k][2] == 'edited':
                            edited = '*'

        cb(bl,i,cc+k+colored.attr('res_underlined'),val_color,v,edited)




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



#EOF


    




