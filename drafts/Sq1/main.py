from kzpy3.vis3 import *
import network  
import graphics  
import Menu.main
from get_data import make_XOR_input_target as make_input_meta_target
exec(identify_file_str)
import menu_str
exec(menu_str.exec_str)
########################################
########################################
###
#M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__))); time.sleep(1)
#M['load']()
#P = M['Q']['network_parameters']
#U = M['Q']['other_parameters']
###
########################################
########################################

kprint(M['Q'])
#raw_enter()


N = network.SqueezeNet(
    P['NUM_INPUT_CHANNELS'],
    P['NUM_OUTPUTS'],
    P['NUM_METADATA_CHANNELS'],
    P['NUM_LOSSES_TO_AVERAGE'],
    )



def main():

    while not M['Q']['other_parameters']['abort']:

        M['load']()

        input_data, meta_data, target_data = \
            network.make_batch( make_input_meta_target, P['BATCH_SIZE'] )

        N.forward(input_data,meta_data,target_data)

        N.backward()

        graphics.graphics(N)

    raw_enter()






if __name__ == '__main__':
    main()



#EOF
