
required_arguments = ['type']

import kzpy3.utils.startup.a as startup
exec(startup.exec_str)
exec(identify_file_str)

if 'Help' in Arguments and Arguments['Help']:
    kprint(Arguments,'Arguments')
    sys.exit()

if 'suffix' not in Arguments:
    Arguments['suffix'] = ''
else:
    Arguments['suffix'] = '.'+Arguments['suffix']

P = {'runtime_parameters':{}}

for k in Arguments:
    P[k] = Arguments[k]

X = None
kprint(Arguments,'Arguments',ra=0)
if P['type'] == 'Runs_Values':
    from get_data.Runs_Values import get_data_function
    from graphics.Runs_Values import graphics_function
    import networks.squeeze
    Network = networks.squeeze.SqueezeNet
elif P['type'] == 'XOR':
    from get_data.XOR import get_data_function
    from graphics.XOR import graphics_function
    import networks.other
    Network = networks.other.OtherNet
elif P['type'] == 'ConDecon_test':
    from get_data.ConDecon_test import get_data_function
    from graphics.ConDecon_test import graphics_function
    import networks.condecon
    Network = networks.condecon.ConDecon
elif P['type'] == 'ConDecon_test2':
    from get_data.ConDecon_test2 import get_data_function
    from graphics.ConDecon_test2 import graphics_function
    from get_data.ConDecon_test2 import X
    import networks.condecon
    Network = networks.condecon.ConDecon
elif P['type'] == 'ConDecon_Fire3':
    from get_data.ConDecon_Fire3 import get_data_function
    from graphics.ConDecon_Fire3 import graphics_function
    from get_data.ConDecon_Fire3 import X
    import networks.condecon
    Network = networks.condecon.ConDecon
elif P['type'] == 'ConDecon_Fire':
    from get_data.ConDecon_Fire import get_data_function
    from graphics.ConDecon_Fire import graphics_function
    from get_data.ConDecon_Fire import X
    import networks.condecon
    Network = networks.condecon.ConDecon

project_path = pname(opjh(__file__))
P['NETWORK_OUTPUT_FOLDER'] = opjD(
    'Networks',
    d2n(#fname(project_path),
        #'_',
        P['type']+Arguments['suffix']
    ))

M['load']()
#kprint(M['Q']['runtime_parameters'])
for k in M['Q']['runtime_parameters'].keys():
    P['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]

Data = networks.net.make_batch( get_data_function, P, P['batch_size'] )
P['NUM_INPUT_CHANNELS'] = shape(Data['input'])[1]
P['NUM_OUTPUTS'] = shape(Data['target'])[1]
P['NUM_METADATA_CHANNELS'] = 0
P['INPUT_WIDTH'] = shape(Data['input'])[2]
P['INPUT_HEIGHT'] = shape(Data['input'])[3]


N = Network(P)

run_timer = Timer()
freq_timer = Timer(30)





def main():

    Abort = Toggler()

    while True:

        M['load']()

        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break

        for k in M['Q']['runtime_parameters'].keys():
            P['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]


        Data = networks.net.make_batch( get_data_function, P, P['batch_size'] )

        N.forward(Data)

        if P['backwards']:
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
            clp( 'Frequency =', int(np.round(f*P['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))

    clp('Exiting.')






if __name__ == '__main__':
    main()



#EOF
