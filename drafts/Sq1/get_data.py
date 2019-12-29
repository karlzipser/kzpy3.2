from kzpy3.vis3 import *
import Menu.main
exec(identify_file_str)
import menu_str
exec(menu_str.exec_str)

########################################
########################################
###
#M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__))); time.sleep(1)
#M['load']()
#P = M['Q']['network_parameters']
###
########################################
########################################


def make_XOR_input_target():
    a = random.choice([0,1])
    b = random.choice([0,1])

    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0

    input_data =    zeros((P['NUM_INPUT_CHANNELS'], P['INPUT_WIDTH'],P['INPUT_HEIGHT']))
    input_data[0,:] += 1 * a
    input_data[1,:] += 1 * b

    meta_data = None
    target_data =   zeros(P['NUM_OUTPUTS'])
    target_data += 1 * c

    return input_data,meta_data,target_data



#EOF
