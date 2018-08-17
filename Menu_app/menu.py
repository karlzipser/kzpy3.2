from kzpy3.utils2 import *

Int = 'Int'
Float = 'Float'


R = {}


def clear_screen():
    print(chr(27) + "[2J")



def menu(Topics,menu_path):

    for t in Topics:

        default = 0
        type_ = Float

        if type(t) == tuple:
            assert len(t) > 0
            name = t[0]
            if len(t) > 1:
                default = t[1]
            if len(t) > 2:
                type_ = t[2]
            assert len(t) < 4
            R[name] = default
            if type_ == Int:
                R[name] = int(R[name])
        else:
            assert False


    message = False
    choice_number = 0
    while choice_number != 1:
        try:
            
            clear_screen()

            ctr = 1

            print d2n(ctr,') ','exit')

            for topic in Topics:

                ctr += 1

                name = topic[0]

                if topic[2] == Int:
                    print d2n(ctr,') ',name,': ',int(R[name]))

                else:
                    print d2n(ctr,') ',name,': ',dp(R[name],2))

            if message:
                print message

            choice_number = input('#? ')

            if not is_number(choice_number):
                message = "bad option"

            elif choice_number == 1: # see "while choice_number != 1:" above
                pass

            else:
                message = False
                index_number = int(choice_number)-2
                name = Topics[index_number][0]
                current_val = R[name]
                val = num_from_str(raw_input(d2n(name,'(',current_val,') new value > ')))
                if is_number(val):
                    R[name] = val
                    if Topics[index_number][1] == Int:
                        R[name] = int(R[name])
                unix(d2n('rm ',opj(menu_path,'ready')))
                unix(d2n('rm ',opj(menu_path,'R.pkl')))
                so(R,opj(menu_path,'R.pkl'))
                unix('touch '+opj(menu_path,'ready'))

        except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)

    clear_screen()

def load_R(menu_path):
    r = sggo(menu_path,'ready')
    if len(r) > 1:
        CS_('Warning, more than one ready in '+menu_path)
    if len(r) == 1:
        R = lo(opjh(menu_path,'R.pkl'))
        unix(d2n('rm ',opj(menu_path,'ready')))
        return R
    else:
        #pd2s('Could not load from',menu_path)
        return None

#EOF