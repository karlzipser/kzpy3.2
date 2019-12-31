from kzpy3.vis3 import *
import network  
import graphics  
import Menu.main
exec(identify_file_str)
import menu_str
exec(menu_str.exec_str)



if P['NET_TYPE'] == 'Runs_Values':
    from get_data import make_Runs_Values_input_target as make_input_meta_target
elif P['NET_TYPE'] == 'XOR':
    from get_data import make_XOR_input_target as         make_input_meta_target

input_data, meta_data, target_data = \
            network.make_batch( make_input_meta_target, P, P['BATCH_SIZE'] )
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
            network.make_batch( make_input_meta_target, P, P['BATCH_SIZE'] )
        #clp(shape(input_data),shape(target_data))

        N.forward(input_data,meta_data,target_data)

        N.backward()

        N.save()

        graphics.graphics(N,M)

        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*P['BATCH_SIZE'])), 'Hz, run time =',dp(run_timer.time()/3600.),'hours')

    raw_enter()






if __name__ == '__main__':
    main()



#EOF
