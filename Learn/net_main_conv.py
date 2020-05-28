

from kzpy3.vis3 import *
import networks.net
exec(identify_file_str)


def Net_Main(M=False,sys_str=False,Arguments_=False,P_Runs_saved=None):
    #cm(0,ra=1)
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
        'projection.noise':0,
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
        'Data_read_path':False,
        'Data_write_path':False,
        'runtime_parameters':{},
        'win_x':0,
        'win_y':0,
        'width':168,
        'height':94,
        'show_graphics':True,
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

    assert P['type'][0] == 'Conv'
    from get_data.Conv import get_data_function
    import get_data.Conv
    if type(P_Runs_saved) != type(None):
        P['Runs'] = P_Runs_saved['Runs']
        P['good_list'] = P_Runs_saved['good_list']
        P['Run_coder'] = P_Runs_saved['Run_coder']
    else:
        get_data.Conv.setup(P)

    from graphics.Conv import graphics_function
    import networks.Conv
    Network = networks.Conv.Conv
    #import networks.condecon_FS
    #Network = networks.condecon_FS.ConDecon_FS

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
    cm(shape(Data['target']),ra=0)
    cm(shape(Data['target'])[1],ra=0)
    cm(P['NUM_OUTPUTS'],ra=1)

    N = Network(P)

    D['P'] = P
    D['N'] = N
    D['get_data_function'] = get_data_function
    D['graphics_function'] = graphics_function
    D['Duplicates'] = Duplicates

    return D



