from kzpy3.vis3 import *
import networks.net
import Menu.main
from net_main import Net_Main
exec(identify_file_str)

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))


sys_str0 = "Learn --type ConDecon_Fire_FS,Fire3,Fire2rgbProjections.b --resume False --save_timer_time 3000 --target_offset 0 --input Fire3 --target rgb,projections --losses_to_average 256 --runs validate --display.output 0,3,3,6 --display.input 3,6 --display.target 0,3,3,6 --clip 0.1"
sys_str1 = "Learn --type ConDecon_Fire_FS,Fire3,Fire2rgb.a --resume False --save_timer_time 3000 --target_offset 0 --input Fire3 --target rgb,projections --losses_to_average 256 --runs validate --display.output 0,3 --display.input 3,6 --display.target 0,3 --clip 0.1"


def main0():

    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,sys_str=sys_str0),
            'N1':Net_Main(M=M,sys_str=sys_str1),
        }
    else:
        clp('   FROM COMMMAND LINE   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,Arguments_=Arguments),
        }

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


Fire2rgbProjections = """

    Learn 
        --type ConDecon_Fire_FS,Fire3,Fire2rgbProjections.b
        --resume True 
        --save_timer_time 999999 
        --target_offset 0 
        --input Fire3 
        --target rgb,projections 
        --losses_to_average 256 
        --runs validate 
        --display.output 0,3,3,6 
        --display.input 0,3 
        --display.target 0,3,3,6
        --clip 0.1
        --backwards False

"""
fire2fireFuture = """

    Learn 
        --type ConDecon_Fire_FS,Fire3,fire2fireFuture.b 
        --resume True 
        --save_timer_time 999999 
        --target_offset 15 
        --input button,Fire3 
        --target Fire3 
        --losses_to_average 256 
        --runs validate 
        --display.output 0,3 
        --display.input 0,3,3,6 
        --display.target 0,3 
        --clip 0.1
        --backwards False

"""


def main1():


    Nets = {
        'N1':Net_Main(M=M,sys_str = Fire2rgbProjections.replace('\n',' ').replace('\t',' ')),
        'N0':Net_Main(M=M,sys_str = fire2fireFuture.replace('\n',' ').replace('\t',' ')),
    }


    run_timer = Timer()
    freq_timer = Timer(30)

    Abort = Toggler()

    wait_timer = Timer(5)



    ctr = 0

    while True:
        M['load']()
        M['Q']['runtime_parameters']['graphics_timer_time'] = -1
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break




        for n in Nets.keys():
            for k in M['Q']['runtime_parameters'].keys():
                Nets[n]['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]


        if ctr == 0 or ctr >= 10:
            Data = networks.net.make_batch( Nets['N0']['get_data_function'], Nets['N0']['P'], Nets['N0']['P']['batch_size'] )
            ctr = 0
            Nets['N0']['Duplicates'] = {}
            for k in ['input','target']:
                Nets['N0']['Duplicates'][k] = Data[k].copy()
        else:
            Out_data2 = {}
            Out_data2['input'] = Data['input']
            cy(shape(Out_data2['input']))
            cg(shape(Nets['N0']['N'].extract('output')))
            Out_data2['input'][0,3:35,:,:] = z2o(Nets['N0']['N'].extract('output'))*15.
            Out_data2['target'] = 0*Nets['N0']['Duplicates']['target']
            Data = Out_data2

        ctr += 1















        for k in Data:
            print 'Data',k,shape(Data[k]),Data[k].min(),Data[k].max()
        print

        Nets['N0']['N'].forward(Data)


        if True:
            Out_data = {}
            Out_data['input'] = na([Nets['N0']['N'].extract('output')])
            Out_data['target'] = 0*Nets['N1']['Duplicates']['target']


            for k in Out_data:
                print 'dup1',k,shape(Nets['N1']['Duplicates'][k])
            for k in Out_data:
                print 'Out_data',k,shape(Out_data[k])
            print
            Nets['N1']['N'].forward(Out_data)
 




        if False:
            for k in Out_data2:
                print 'dup2',k,shape(Nets['N0']['Duplicates'][k])
            for k in Out_data2:
                print 'Out_data2',k,shape(Out_data2[k])
            print


        for n in Nets.keys():
            Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P'])
        cm(6,ra=1)









if __name__ == '__main__':

    
        if 'main' not in Arguments or Arguments['main'] == 0:
            clp('*** main0() ***',p=2)
            main0()

        if Arguments['main'] == 1:
            clp('*** main1() ***',p=2)
            main1()



#EOF
