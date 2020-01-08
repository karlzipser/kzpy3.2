from kzpy3.vis3 import *

import Menu.main
exec(identify_file_str)
import other.menu_str
import other.default_args
exec(other.menu_str.exec_str)


if 'NET_TYPE' not in Arguments:
    clp("\n\n--NET_TYPE argument required.\n")
    clp("    e.g., python kzpy3/drafts/Sq7/main.py --RESUME 1 --NET_TYPE ConDecon_test2 --NET_TYPE_SUFFIX 84x47\n\n")
    sys.exit()
setup_Default_Arguments(
    other.default_args.Default_Arguments[Arguments['NET_TYPE']]
)
if 'NET_TYPE_SUFFIX' not in Arguments:
    Arguments['NET_TYPE_SUFFIX'] = ''
else:
    Arguments['NET_TYPE_SUFFIX'] = '.'+Arguments['NET_TYPE_SUFFIX']
P = {}
for k in Arguments:
    P[k] = Arguments[k]
#kprint(P);raw_enter()
"""
P['NET_TYPE'] = Arguments['net']
P['RESUME'] = Arguments['resume']
P['GPU'] = Arguments['gpu']
P['LR'] = Arguments['lr']
P['MOMENTUM'] = Arguments['momentum']
P['BATCH_SIZE'] = Arguments['batch_size']
P['NET_SAVE_TIMER_TIME'] = Arguments['save_time']
P['NUM_LOSSES_TO_AVERAGE'] = Arguments['num_losses_to_average']
"""
#P['data_tracker'] = Arguments['data_tracker']
if P['NET_TYPE'] == 'Runs_Values':
    from get_data.Runs_Values import get_data_function
    from graphics.Runs_Values import graphics_function
    import networks.squeeze
    Network = networks.squeeze.SqueezeNet
elif P['NET_TYPE'] == 'XOR':
    from get_data.XOR import get_data_function
    from graphics.XOR import graphics_function
    import networks.other
    Network = networks.other.OtherNet
elif P['NET_TYPE'] == 'ConDecon_test':
    from get_data.ConDecon_test import get_data_function
    from graphics.ConDecon_test import graphics_function
    import networks.condecon
    Network = networks.condecon.ConDecon
elif P['NET_TYPE'] == 'ConDecon_test2':
    from get_data.ConDecon_test2 import get_data_function
    from graphics.ConDecon_test2 import graphics_function
    from get_data.ConDecon_test2 import X
    import networks.condecon
    Network = networks.condecon.ConDecon
elif P['NET_TYPE'] == 'ConDecon_Fire3':
    from get_data.ConDecon_Fire3 import get_data_function
    from graphics.ConDecon_Fire3 import graphics_function
    from get_data.ConDecon_Fire3 import X
    import networks.condecon
    Network = networks.condecon.ConDecon
project_path = pname(opjh(__file__))
P['NETWORK_OUTPUT_FOLDER'] = opjD(
    'Networks',
    d2n(fname(project_path),
        '_',
        P['NET_TYPE']+Arguments['NET_TYPE_SUFFIX']
    ))
Data = networks.net.make_batch( get_data_function, P, P['BATCH_SIZE'] )
P['NUM_INPUT_CHANNELS'] = shape(Data['input'])[1]
P['NUM_OUTPUTS'] = shape(Data['target'])[1]
P['NUM_METADATA_CHANNELS'] = 0
P['INPUT_WIDTH'] = shape(Data['input'])[2]
P['INPUT_HEIGHT'] = shape(Data['input'])[3]

kprint(M['Q'])

N = Network(P)

run_timer = Timer()
freq_timer = Timer(30)


def main():

    while not M['Q']['runtime_parameters']['abort']:

        M['load']()

        Data = networks.net.make_batch( get_data_function, P, P['BATCH_SIZE'] )

        N.forward(Data)

        N.backward()

        N.save()

        try:
            graphics_function(N,M,X)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   


        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*P['BATCH_SIZE'])), 'Hz, run time =',format_seconds(run_timer.time()))

    clp('Exiting.')
    #raw_enter()






if __name__ == '__main__':
    main()



#EOF
