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
    D['Q'] = Q
    D['R'] = {}
    add_keys(D,D['Q'])
    def function_save():
        #so(D['.pkl'],D['Q'])
        save_C(D['Q'],D['project_path'])
    def function_load():
        #D['Q'] = lo(D['.pkl'])
        load_C(D['Q'],D['project_path'])
        D['R'] = {}
        add_keys(D,D['Q'])
    D['load'] = function_load
    D['save'] = function_save
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


def load_C(C,project_path):
    if len(sggo(opj(project_path,'__local__','ready'))) == 0:
        return False
    if len(sggo(opj(project_path,'__local__','default_values.writing.pkl'))) > 0:
        return False
    if len(sggo(opj(project_path,'__local__','default_values.pkl'))) == 0:
        return False
    try:
        D = lo(opj(project_path,'__local__','default_values.pkl'))
    except:
        return False
    if len(sggo(opj(project_path,'__local__','ready'))) == 0:
        return False
    if len(sggo(opj(project_path,'__local__','default_values.writing.pkl'))) > 0:
        return False
    if len(sggo(opj(project_path,'__local__','default_values.pkl'))) == 0:
        return False
    for k in C.keys():
        C[k] = D[k]
    return True


def save_C(C,project_path):
    print 1
    try:
        sys_str = d2s('rm',opj(project_path,'__local__','ready'))
        os.system(sys_str)
    except:
        cr(sys_str,"failed")
    so(C,opj(project_path,'__local__','default_values.writing.pkl'))
    time.sleep(0.1)
    try:
        sys_str = d2s('rm',opj(project_path,'__local__','default_values.pkl'))
        print sys_str
        os.system(sys_str)
    except:
        cr(sys_str,"failed")
    sys_str = d2s('mv',opj(project_path,'__local__','default_values.writing.pkl'),opj(project_path,'__local__','default_values.pkl'))
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




if __name__ == '__main__':

    ABORT = False


    from kzpy3.Commands.temp2 import Q
    D2 = Default_Values(Q,opjk('Commands'),['a','b'])

    from kzpy3.Commands.temp3 import Q
    D3 = Default_Values(Q,opjk('Commands'))

    while True:

        load_C(C)

        C_ = C

        for k in key_list:
            if type(C_[k]) == dict:
                C_ = C_[k]
            else:
                break

        sorted_keys = show_menu(C_,key_list)

        cw(message); message = ''

        if ABORT == True:
            break

        if len(arg_choice_list) > 0:
            raw_choice = arg_choice_list.pop()
        else:
            raw_choice = raw_input(mg+'choice: '+lb)

        if raw_choice == '':
            message = "other commands: 'load','save','q' (quit), 'p' (python)"
            continue

        if raw_choice == 'q':
            message = "\ndone.\n"
            ABORT = True
            continue


        if raw_choice == 'p':
            try:
                code = raw_input(d2n("Enter python code: "))
                d = code.split(';')
                if 'print' not in d[-1]:
                    d[-1]=d2s('print(',d[-1],')')
                code = ';'.join(d)
                exec(code)
                raw_enter()
                continue
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                message = d2s('Exception!',exc_type,file_name,exc_tb.tb_lineno)
                continue


        if raw_choice == 'load':
            try:
                files_mtimes = get_files_sorted_by_mtime(opjk('Commands','__local__','C.*.pkl'))
                lst = []
                for f in files_mtimes:
                    lst.append(f[0])
                if len(lst) < 1:
                    message = "No C.*.pkl's to load"
                    continue
                lst.reverse()
                for i in rlen(lst):
                    print(d2n(i,') ',fname(lst[i]).split('.')[-2]))
                num = input('num: ')
                f = opjk('Commands','__local__','C.'+fname(lst[num]).split('.')[-2]+'.pkl')
                C = lo(f)
                message = d2s('loaded',f)
                save_C(C)
            except:
                message = "load failed"
            continue

        if raw_choice == 'save':
            name = raw_input('name: ')
            try:
                os.system(d2s("rm",opjk('Commands','__local__','C.'+name+'.pkl')))
            except:
                message="asdfdasfadsf"
                pass
            save_C(C)
            f = opjk('Commands','__local__','C.'+name+'.pkl')
            os.system(d2s("cp",opjk('Commands','__local__','C.pkl'),f))
            message = d2s('saved',f)
            continue

        if str_is_int(raw_choice):
            choice = int(raw_choice)
        else:
            message = d2s("*** choice","'"+raw_choice+"'",'is not an integer')
            continue
        if choice < 0 or choice+1 > len(sorted_keys):
            message = '*** choice is out of range'
            continue

        key_choice = sorted_keys[choice]

        if choice == 0:
            if sorted_keys[0] == '<up>':
                key_list.pop()
            else:
                message = "*** can't go up, already at top"
                continue
        elif type(C_[key_choice]) == dict:
            key_list.append(key_choice)

        else:
            cmd_mode = C_[key_choice][0]
            cmd_str = C_[key_choice][1]
            
            if cmd_mode == 'bash':
                yes_no = 'y'#raw_input(d2s(cmd_str,' ([y]/n) '))

                if yes_no == 'y' or yes_no == '':

                    try:
                        if cmd_str[0] != '@':
                            os.system(cmd_str)
                        else:
                            os.system("gnome-terminal --geometry 50x30+100+200 -x "+cmd_str[1:])
                            raw_enter()
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        CS_('Exception!',emphasis=True)
                        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                        raw_enter()

            elif cmd_mode == 'set value':
                try:
                    if type(C_[key_choice][1]) == bool:
                        value = C_[key_choice][1]
                        yes_no = raw_input(d2n("Toggle '",key_choice,"'? ([y]/n) "))
                        if yes_no == 'y' or yes_no == '':
                            value = not value
                            message = d2n("(set '",key_choice,"' to ",value,')')
                        if value:
                            message = d2n("('",key_choice,"' unchanged)")
                    else:
                        value = input(d2n("Enter value for '",key_choice,"': "))
                        if type(value) != type(C_[key_choice][1]):
                            message = d2n("!!! type(",value,") != type(",C_[key_choice][1],") !!!")
                            continue
                        message = d2n("(set '",key_choice,"' to ",value,')')
                    print key_choice,value,C_[key_choice]
                    C_[key_choice] = (cmd_mode,value,'edited')
                    save_C(C)
                    time.sleep(1/8.)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                    raw_enter()

            elif cmd_mode == 'active':
                
                    A = Dic_Loader(C_[key_choice][1])
                    while True:
                        try:
                            if A['load']():
                                clear_screen()
                                for k in sorted(A['Dic'].keys()):
                                    cw(gr,str(k)+')',yl,A['Dic'][k])
                                cw(lb,time_str('Pretty'))
                        except KeyboardInterrupt:
                            cr('*** KeyboardInterrupt ***')
                            break
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            CS_('Exception!',emphasis=True)
                            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

            elif cmd_mode == 'python':
                code = raw_input(d2n("Enter python code: "))
                d = code.split(';')
                if 'print' not in d[-1]:
                    d[-1]=d2s('print(',d[-1],')')
                code = ';'.join(d)
                exec(code)
                raw_enter()

            elif cmd_mode == 'path':
                c = file_to_text(C_[key_choice][1])
                C_[key_choice][1]
                exec(c)
                normal_dic_to_dic_in_Command_form(Q)
                assign_path(Q,C_[key_choice][1])
                Q['_path_'] = ('const',C_[key_choice][1])
                C_[key_choice] = Q
                save_C(C)
                key_list.append(key_choice)








"""
rd = '\x1b[31m'
gr = '\x1b[32m'
yl = '\x1b[33m'
bl = '\x1b[34m'
mg = '\x1b[35m'
lb = '\x1b[36m'
wh = '\x1b[29m'
https://pypi.org/project/colored/
"""

#EOF

    




