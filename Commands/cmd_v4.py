#!/usr/bin/env python
from kzpy3.vis3 import *
import default_values_v4 as default_values
exec(identify_file_str)
P = default_values.P
for k in CShowFile.keys():
    CShowFile[k] = False



#############################################
# Arguments, setup
os.system('mkdir -p '+opjk('Commands','__local__'))
if 'set' in Arguments:
    if type(Arguments['set']) == int:
        arg_choice_list = [Arguments['set']]
    elif Arguments['set'] == 'clear':
        arg_choice_list = []
    else:
        arg_choice_list = Arguments['set'].split(',')
        for a in arg_choice_list:
            try:
                assert str_is_int(a)
            except:
                cr('*** Invalid arg_choice_list string:',"'"+Arguments['set']+"'")
                sys.exit()
        arg_choice_list.reverse()
    so(opjk('Commands','__local__','arg_choice_list.pkl'),arg_choice_list)
try:
    arg_choice_list = lo(opjk('Commands','__local__','arg_choice_list.pkl'))
except:
    arg_choice_list = []
#
#############################################


C = P['commands']
key_list = []
message = ''




def load_C(C):
    if len(sggo(opjk('Commands','__local__','ready'))) == 0:
        return False
    if len(sggo(opjk('Commands','__local__','C.writing.pkl'))) > 0:
        return False
    if len(sggo(opjk('Commands','__local__','C.pkl'))) == 0:
        return False
    try:
        D = lo(opjk('Commands','__local__','C.pkl'))
    except:
        return False
    if len(sggo(opjk('Commands','__local__','ready'))) == 0:
        return False
    if len(sggo(opjk('Commands','__local__','C.writing.pkl'))) > 0:
        return False
    if len(sggo(opjk('Commands','__local__','C.pkl'))) == 0:
        return False
    for k in C.keys():
        C[k] = D[k]
    return True



def save_C(C):
    try:
        sys_str = d2s('rm',opjk('Commands','__local__','ready'))
        os.system(sys_str)
    except:
        cr(sys_str,"failed")
    so(C,opjk('Commands','__local__','C.writing.pkl'))
    time.sleep(0.1)
    try:
        sys_str = d2s('rm',opjk('Commands','__local__','C.pkl'))
        print sys_str
        os.system(sys_str)
    except:
        cr(sys_str,"failed")
    sys_str = d2s('mv',opjk('Commands','__local__','C.writing.pkl'),opjk('Commands','__local__','C.pkl'))
    print sys_str
    os.system(sys_str)
    sys_str = d2s('touch',opjk('Commands','__local__','ready'))
    print sys_str
    os.system(sys_str)    



def show_menu(C,key_list):
    clear_screen()
    cprint(
        '/'.join(key_list),
        attrs=['bold','reverse'],
        color='white',
        on_color='on_blue'
    ) 
    sorted_keys = sorted(C.keys())
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
        if k in C:
            if type(C[k]) == tuple and C[k][0] == 'active':
                cc = og
            elif type(C[k]) == tuple and C[k][0] == 'python':
                cc = lb
            elif type(C[k]) == dict:
                cc = wh
            else:
                cc = yl
        v = ''
        edited = ''
        if k in C:
            if type(C[k]) == tuple:
                if C[k][0] == 'set value':
                    v = C[k][1]
                    if len(C[k]) > 2:
                        if C[k][2] == 'edited':
                            edited = '*'

        cb(bl,i,cc,k,lb,v,edited)
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

        




if __name__ == '__main__':

    ABORT = False

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
            cr("*** choice","'"+raw_choice+"'",'is not an integer',ra=1)
            continue
        if choice < 0 or choice+1 > len(sorted_keys):
            cr('*** choice is out of range',ra=1)
            continue

        key_choice = sorted_keys[choice]

        if choice == 0:
            if sorted_keys[0] == '<up>':
                key_list.pop()
            else:
                cr("*** can't go up, already at top",ra=1)
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

        






"""
rd = '\x1b[31m'
gr = '\x1b[32m'
yl = '\x1b[33m'
bl = '\x1b[34m'
mg = '\x1b[35m'
lb = '\x1b[36m'
wh = '\x1b[29m'
"""

#EOF

    




