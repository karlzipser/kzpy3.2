from kzpy3.utils3 import *
import torch
import kzpy3.Menu_app.menu2
import network_utils.torch_network
exec(identify_file_str)


def read_menu_and_load_network(N):
    
    if not N['timer']['parameter_file_load'].check():
        return

    Topics = kzpy3.Menu_app.menu2.load_Topics(
        N['project_path'],
        first_load=False,
        customer='Network')

    if type(Topics) == dict:
        for t in Topics.keys():
            if t == 'ABORT':
                if Topics[t] == True:
                    N['ABORT'] = True
                    time.sleep(1)
                    return
        for t in Topics['To Expose']['Network']+\
                 Topics['To Expose']['Weights']+\
                 Topics['To Expose']['Flex']:
            if '!' in t:
                pass
            else:
                N[t] = Topics[t]
    
    if N['LOAD NETWORK'] == False:
        N['net']['loaded_net'] = False
    N['weight_file_path'] = False
    if N['net']['loaded_net'] == False:
        if N['LOAD NETWORK'] == True:
            N['net']['loaded_net'] = True
            ns = N['weight_files'].keys()
            for n in ns:
                if N[n] != False:
                    if type(N[n]) == int:
                        if N[n] != 0:
                            N['weight_file_path'] = \
                                N['weight_files'][n][N[n]]
                            sbpd2s("N['weight_file_path'] = N['weight_files'][n][a[1]]")
                            break
            if N['weight_file_path'] != False:
                
                cs( "if N['weight_file_path'] != False:" )

                N['net']['Torch_network'] = \
                    network_utils.torch_network.Torch_Network(
                        N['weight_file_path'])

                cs( "Torch_network = net_utils.Torch_Network(N)" )

    N['timer']['parameter_file_load'].reset()

# weight_file_path=N['weight_files']['weights (1370)'][-1]


#EOF

