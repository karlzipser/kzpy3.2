from kzpy3.utils2 import *

def clear_screen():
    print(chr(27) + "[2J")

def menu(Topics,menu_path):

    message = False
    choice_number = 0
    Number_name_binding = {}
    while choice_number != 1:
        try:
            
            clear_screen()

            ctr = 1

            print d2n(ctr,') ','exit')

            for name in Topics.keys():

                ctr += 1

                Number_name_binding[ctr] = name
                
                print d2n(ctr,') ',name,': ',Topics[Number_name_binding[ctr]])
                #print d2n(ctr,') ',name,': ',dp(Topics[Number_name_binding[ctr]],2))

            if message:
                print message

            choice_number = input('#? ')

            if type(choice_number) != int:
                message = "bad option"

            elif choice_number == 1:
                pass

            else:
                message = False
                name = Number_name_binding[choice_number]
                current_val = Topics[name]
                #val = num_from_str(raw_input(d2n(name,'(',current_val,') new value > ')))
                Topics[name] = input(d2n(name,'(',current_val,') new value > '))
                #if is_number(val):
                #    Topics[name] = val
                    #if type(Topics[Number_name_binding[ctr]]) == int:
                    #    Topics[name] = int(Topics[name])
                unix(d2n('rm ',opj(menu_path,'ready')))
                unix(d2n('rm ',opj(menu_path,'Topics.pkl')))
                so(Topics,opj(menu_path,'Topics.pkl'))
                unix('touch '+opj(menu_path,'ready'))

        except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)

    clear_screen()

def load_Topics(menu_path,first_load=False):
    if first_load:
        r = ['ready']
    else:
        r = sggo(menu_path,'ready')
    if len(r) > 1:
        CS_('Warning, more than one ready in '+menu_path)
    if len(r) == 1:
        Topics = lo(opjh(menu_path,'Topics.pkl'))
        unix(d2n('rm ',opj(menu_path,'ready')))
        return Topics
    else:
        #pd2s('Could not load from',menu_path)
        return None

def load_menu_data(menu_path,Parameters,first_load=False):
    timer = Timer(0.5)
    while Parameters['ABORT'] == False:
        if timer.check():
            Topics = load_Topics(menu_path,first_load)
            if type(Topics) == dict:
                for t in Topics.keys():
                    Parameters[t] = Topics[t]
            timer.reset()
        else:
            time.sleep(0.1)

#EOF