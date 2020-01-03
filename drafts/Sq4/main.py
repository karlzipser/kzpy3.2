from kzpy3.vis3 import *
import network  
#import graphics  
import Menu.main
exec(identify_file_str)
import menu_str
exec(menu_str.exec_str)

if P['NET_TYPE'] == 'Runs_Values':
    from get_data.Runs_Values import get_data_function as get_data_function
    from graphics.Runs_Values import graphics_function as graphics_function
elif P['NET_TYPE'] == 'XOR':
    from get_data.XOR import get_data_function as get_data_function
    from graphics.XOR import graphics_function as graphics_function

input_data, meta_data, target_data = \
            network.make_batch( get_data_function, P, P['BATCH_SIZE'] )
P['NUM_INPUT_CHANNELS'] = shape(input_data)[1]
P['NUM_OUTPUTS'] = shape(target_data)[1]
P['NUM_METADATA_CHANNELS'] = 0
P['INPUT_WIDTH'] = shape(input_data)[2]
P['INPUT_HEIGHT'] = shape(input_data)[3]
P['METADATA_WIDTH'] = 41
P['METADATA_HEIGHT'] = 23
kprint(M['Q'])

N = network.SqueezeNet(
    P['NUM_INPUT_CHANNELS'],
    P['NUM_OUTPUTS'],
    P['NUM_METADATA_CHANNELS'],
    P['NUM_LOSSES_TO_AVERAGE'],
    P['NETWORK_OUTPUT_FOLDER'],
    P['NET_SAVE_TIMER_TIME'],
    P['GPU'],
    )
if P['GPU'] > -1:
    N = N.cuda()
else:
    clp('Running in CPU mode')
if P['RESUME']:
    N.load()
else:
    clp('Starting with random weights','`wbb')
 



def main():
    run_timer = Timer()
    freq_timer = Timer(30)

    while not M['Q']['other_parameters']['abort']:

        M['load']()

        input_data, meta_data, target_data = \
            network.make_batch( get_data_function, P, P['BATCH_SIZE'] )

        N.forward(input_data,meta_data,target_data)

        N.backward()

        N.save()

        try:
            graphics_function(N,M)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    


        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*P['BATCH_SIZE'])), 'Hz, run time =',format_seconds(run_timer.time()))

    raw_enter()






if __name__ == '__main__':
    main()



#EOF
