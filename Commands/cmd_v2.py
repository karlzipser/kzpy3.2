#!/usr/bin/env python
from kzpy3.utils3 import *
import default_values_v2 as default_values
exec(identify_file_str)
P = default_values.P


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

C = P['commands']

key_list = []

message = ''

def show_menu(C,key_list):
    clear_screen()
    #print(mg+"____________________\n")
    cprint(d2s(key_list_to_path(key_list)),attrs=['bold','reverse'],color='white',on_color='on_blue') 
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
                cc = rd
            elif type(C[k]) == dict:
                cc = gr
            else:
                cc = yl
        v = ''
        if k in C:
            if type(C[k]) == tuple:
                if C[k][0] == 'set value':
                    v = C[k][1]
        
        cb(bl,i,cc,k,lb,v)
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

        cw(message)
        message = ''

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
            cmd_mode = C_[key_choice][0]
            cmd_str = C_[key_choice][1]
            
            if cmd_mode == 'bash':
                yes_no = 'y'#raw_input(d2s(cmd_str,' ([y]/n) '))

                if yes_no == 'y' or yes_no == '':
                    #os.system("gnome-terminal --geometry 40x30+100+200 -x python  kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019/nodes dic P")
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
                    C_[key_choice] = (cmd_mode,value)
                    time.sleep(1/8.)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                    raw_enter()

            elif cmd_mode == 'active':
                cr('active stuff!',ra=1)







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

    




