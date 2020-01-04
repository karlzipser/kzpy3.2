from kzpy3.vis3 import *
import network  
import Menu.main
exec(identify_file_str)
import menu_str
exec(menu_str.exec_str)

if P['NET_TYPE'] == 'Runs_Values':
    from get_data.Runs_Values import get_data_function
    from graphics.Runs_Values import graphics_function
    Network = network.SqueezeNet
elif P['NET_TYPE'] == 'XOR':
    from get_data.XOR import get_data_function
    from graphics.XOR import graphics_function
    Network = network.SqueezeNet
Data = network.make_batch( get_data_function, P, P['BATCH_SIZE'] )
P['NUM_INPUT_CHANNELS'] = shape(Data['input'])[1]
P['NUM_OUTPUTS'] = shape(Data['target'])[1]
P['NUM_METADATA_CHANNELS'] = 0
P['INPUT_WIDTH'] = shape(Data['input'])[2]
P['INPUT_HEIGHT'] = shape(Data['input'])[3]
P['METADATA_WIDTH'] = 41
P['METADATA_HEIGHT'] = 23
kprint(M['Q'])

N = Network(P)

run_timer = Timer()
freq_timer = Timer(30)

def main():


    while not M['Q']['other_parameters']['abort']:

        M['load']()

        Data = network.make_batch( get_data_function, P, P['BATCH_SIZE'] )

        N.forward(Data)

        N.backward()

        N.save()

        try:
            graphics_function(N,M)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   


        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*P['BATCH_SIZE'])), 'Hz, run time =',format_seconds(run_timer.time()))

    raw_enter()






if __name__ == '__main__':
    main()



#EOF
