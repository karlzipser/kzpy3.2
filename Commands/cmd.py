#!/usr/bin/env python
# v1
from kzpy3.utils3 import *
import default_values
exec(identify_file_str)
_ = default_values._


os.system('mkdir -p '+opjk('Commands','__local__'))



if 'set' in Arguments:
    if type(Arguments['set']) == int:
        arg_choice_list = [Arguments['set']]
    elif Arguments['set'] == 'clear':
        arg_choice_list = []
    else:
        arg_choice_list = Arguments['set'].split(',')
        arg_choice_list.reverse()
    so(opjk('Commands','__local__','arg_choice_list.pkl'),arg_choice_list)


try:
    arg_choice_list = lo(opjk('Commands','__local__','arg_choice_list.pkl'))
except:
    arg_choice_list = []

for k in CShowFile.keys():
    CShowFile[k] = False

#cy(Arguments,arg_choice_list,ra=1)

C = _['commands']

key_list = []

def show_menu(C,key_list):
    #clear_screen()
    print(mg+"____________________\n")
    cprint(d2s('keypath:',key_list_to_path(key_list)),attrs=['bold','reverse'],color='white',on_color='on_blue') 
    sorted_keys = sorted(C.keys())
    if len(key_list) == 0:
        s = '<top>'
    else:
        s = '<up>'
    sorted_keys.insert(0,s)
    for i in rlen(sorted_keys):
        k = sorted_keys[i]
        cc = cb
        if k in C:
            if type(C[k]) == dict:
                cc = cg
            else:
                cc = cy
        cc(i,k)
    return sorted_keys

def key_list_to_path(key_list):
    s = ''
    for k in key_list:
        s += '/'
        s += k
    return s

if __name__ == '__main__':

    while True:

        C_ = C
        for k in key_list:

            if type(C_[k]) == dict:
                C_ = C_[k]
            else:
                break

        sorted_keys = show_menu(C_,key_list)

        if len(arg_choice_list) > 0:
            raw_choice = arg_choice_list.pop()
        else:
            raw_choice = raw_input(mg+'choice: '+lb)

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
            cmd_str = C_[key_choice]
            
            yes_no = raw_input(d2s(cmd_str,' ([y]/n) '))
            if yes_no == 'y' or yes_no == '':
                #os.system("gnome-terminal --geometry 40x30+100+200 -x python  kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019/nodes dic P")
                try:
                    #print cmd_str,cmd_str[0]
                    if cmd_str[0] != '@':
                        os.system(cmd_str)
                    else:
                        os.system("gnome-terminal --geometry 50x30+100+200 -x "+cmd_str[1:])
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)                    

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

    




