


from kzpy3.vis3 import *
import networks.net
import Menu.main
exec(identify_file_str)

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))



sys_str0 = "Learn --type ConDecon_Fire_FS,Fire3,Fire2rgbProjections.b --resume False --save_timer_time 3000 --target_offset 0 --input Fire3 --target rgb,projections --losses_to_average 256 --runs validate --display.output 0,3,3,6 --display.input 3,6 --display.target 0,3,3,6 --clip 0.1"
sys_str1 = "Learn --type ConDecon_Fire_FS,Fire3,Fire2rgb.a --resume False --save_timer_time 3000 --target_offset 0 --input Fire3 --target rgb,projections --losses_to_average 256 --runs validate --display.output 0,3 --display.input 3,6 --display.target 0,3 --clip 0.1"





def Net_Main(M=M,sys_str=False,Arguments_=False):

    D = {}

    P = {
        'resume':1,
        'GPU':999,
        'momentum':0.001,
        'LR':0.01,
        'batch_size':64,
        'backwards':True,
        'losses_to_average':25,
        'save_timer_time':5*minutes,
        'runs':'train',
        'clip':1,
        'noise':0,
        'input':False,
        'target':False,
        'display.output':[0,3],
        'display.input':[0,3],
        'display.target':[0,3],
        'batch_size':1,
        'losses_to_average':64,
        'runs':'train',
        'input_offset':0,
        'target_offset':0,
        'inputs':['Fire3'],
        'targets':['Fire3'],
        'Data_read_path':False,
        'Data_write_path':False,
        'runtime_parameters':{}
    }

    if sys_str != False:
        Arguments_ = parse_to_Arguments(sys_str)
    else:
        assert type(Arguments_) == dict

    for k in Arguments_:
        P[k] = Arguments_[k]
    kprint(P)
    for k in ['type','input','target']:
        if type(P[k]) == str:
            P[k] = [P[k]]

    assert P['type'][0] == 'ConDecon_Fire_FS'
    from get_data.ConDecon_Fire import get_data_function
    import get_data.ConDecon_Fire
    get_data.ConDecon_Fire.setup(P)
    from graphics.ConDecon_Fire import graphics_function
    import networks.condecon_FS
    Network = networks.condecon_FS.ConDecon_FS

    P['NETWORK_OUTPUT_FOLDER'] = opjD(
        'Networks',
        d2n(
            '.'.join(P['type'])
        ))

    M['load']()

    for k in M['Q']['runtime_parameters'].keys():
        P['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]

    Data = networks.net.make_batch( get_data_function, P, P['batch_size'] )
    Duplicates = {}
    for k in ['input','target']:
        Duplicates[k] = Data[k].copy()

    P['NUM_INPUT_CHANNELS'] = shape(Data['input'])[1]
    P['NUM_OUTPUTS'] = shape(Data['target'])[1]
    P['NUM_METADATA_CHANNELS'] = 0
    P['INPUT_WIDTH'] = shape(Data['input'])[2]
    P['INPUT_HEIGHT'] = shape(Data['input'])[3]

    N = Network(P)

    D['P'] = P
    D['N'] = N
    D['get_data_function'] = get_data_function
    D['graphics_function'] = graphics_function

    return D








def main():

    Nets = {
        'N0':Net_Main(sys_str=sys_str0),
        'N1':Net_Main(sys_str=sys_str1),
    }

    #N0 = Net_Main(sys_str=sys_str)
    #N0 = Net_Main(Arguments_=Arguments)
    run_timer = Timer()
    freq_timer = Timer(30)

    Abort = Toggler()

    wait_timer = Timer(5)







    while True:
        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break


        for n in Nets.keys():

            for k in M['Q']['runtime_parameters'].keys():
                Nets[n]['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]


            Data = networks.net.make_batch( Nets[n]['get_data_function'], Nets[n]['P'], Nets[n]['P']['batch_size'] )


            Nets[n]['N'].forward(Data)


            if Nets[n]['P']['backwards']:
                Nets[n]['N'].backward()

            Nets[n]['N'].save()

            if True:#try:
                Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P']) # graphics can cause an error with remote login
            else:#except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   



            f = freq_timer.freq(do_print=False)
            if is_number(f):
                clp( 'Frequency =', int(np.round(f*Nets[n]['P']['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))



    clp('Exiting.')






if __name__ == '__main__':
    main()



#EOF
