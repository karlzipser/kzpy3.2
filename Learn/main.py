from kzpy3.vis3 import *
import networks.net
import Menu.main
from net_main import Net_Main
exec(identify_file_str)

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))


Net_strs = {
    #Learn --main 4 --net_str Fire2rgbProjections.dcgan

    'pts2d0' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,pts2d0
            --resume True 
            --batch_size 1
            --save_timer_time 600 
            --target_offset 0 
            --input rgb,Fire3,button
            --target pts2d 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3 
            --display.input 0,3,3,6,6,9
            --display.target 0,3
            --clip 0.0001
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
            --blue_center_button True
            --pts2_h5py_type h5py_half

    """,
    'pts2d1' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,pts2d1
            --resume True 
            --batch_size 1
            --save_timer_time 600 
            --target_offset 0 
            --input rgb,Fire3,button,pts2d
            --target pts2d 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3 
            --display.input 0,3,3,6,6,9,9,12
            --display.target 0,3
            --clip 0.0001
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
            --blue_center_button True
            --pts2_h5py_type h5py_half2

    """,
    'pts2d2' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,pts2d2
            --resume True 
            --batch_size 1
            --save_timer_time 600 
            --target_offset 0 
            --input rgb,Fire3,button
            --target pts2d
            --losses_to_average 256 
            --runs train 
            --display.output 0,3 
            --display.input 0,3,3,6,6,9
            --display.target 0,3
            --clip 0.0001
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
            --blue_center_button True
            --pts2_h5py_type h5py_angles0

    """,
    'Fire2rgbProjections.dcgan' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,Fire2rgbProjections.dcgan
            --resume True 
            --batch_size 1
            --save_timer_time 300 
            --target_offset 0 
            --input Fire3 
            --target rgb,projections 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3,3,6 
            --display.input 0,3 
            --display.target 0,3,3,6
            --clip 0.0001
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
    """,


}

def main6():

    import torch
    import torch.nn as nn
    import torch.nn.parallel
    import torch.backends.cudnn as cudnn
    import torch.optim as optim
    import torch.utils.data
    import torchvision.datasets as dset
    import torchvision.transforms as transforms
    import torchvision.utils as vutils
    import torch.nn.utils as nnutils

    from discriminator1 import Discriminator,weights_init


    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            #'N0':Net_Main(M=M,sys_str=fire2fireFuture_dcgan_a.replace('\n',' ').replace('\t',' ')),
            'N0':Net_Main(M=M,sys_str=Net_strs[Arguments['net_str']].replace('\n',' ').replace('\t',' '),Arguments_=Arguments),

        }
    else:
        clp('   FROM COMMMAND LINE   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,Arguments_=Arguments),
        }

    n = 'N0'
    Data = networks.net.make_batch( Nets[n]['get_data_function'], Nets[n]['P'], Nets[n]['P']['batch_size'] )
    cg('Data',shape(Data['input']),shape(Data['target']))


    DISCRIMINATOR = Discriminator(nc=shape(Data['target'])[1]).cuda()   #shape(Data['target'])[1]).cuda()


    DISCRIMINATOR.apply(weights_init)

    criterion = nn.BCELoss()
    optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=0.01, betas=(0.5, 0.999))



    run_timer = Timer()
    freq_timer = Timer(30)

    Abort = Toggler()

    wait_timer = Timer(5)

    minute_timer = Timer(60)

    try:
        if Nets['N0']['P']['resume']:
            DISCRIMINATOR.load(Nets['N0']['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
    except:
        clp("*** DISCRIMINATOR.load(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan') failed ***",ra=1)


    graphics_on = False


    while True:

        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break

        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            #a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            clp('clip',Nets['N0']['P']['clip'],int(run_timer.time()),"`yb")


        
        GENERATOR = Nets[n]['N']
        Nets[n]['P']['original_Fire3_scaling'] = True

        for k in M['Q']['runtime_parameters'].keys():
            Nets[n]['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]



        Data = networks.net.make_batch( Nets[n]['get_data_function'], Nets[n]['P'], Nets[n]['P']['batch_size'] )

        

        #A
        DISCRIMINATOR.zero_grad() #1
        real = Data['target'][:,:,:,:] #2
        label = torch.full((Nets[n]['P']['batch_size'],), 1,).cuda() #3
        output = DISCRIMINATOR(torch.from_numpy(real).cuda().float()) #4

        errD_real = criterion(output, label) #5
        errD_real.backward() #6
        D_x = output.mean().item() #7

        GENERATOR.forward_no_loss(Data) #8
        fake = GENERATOR.A['output'][:,:,:,:]
        label.fill_(0) #9
        output = DISCRIMINATOR(fake.detach()) #10

        errD_fake = criterion(output, label) #11
        errD_fake.backward() #12
        D_G_z1 = output.mean().item() #13
        errD = errD_real + errD_fake #14
        optimizerD.step() #15
        
        GENERATOR.optimizer.zero_grad() #16
        label.fill_(1) #17
        output = DISCRIMINATOR(fake) #18

        s = 0.0001
        if Arguments['net_str'] == 'proRgb2rgb.noise':
            s = 0.0000001

        GENERATOR.loss = s*GENERATOR.criterion(GENERATOR.A['output'],GENERATOR.A['target']) + (1-s) * criterion(output, label) #19


        if Nets[n]['P']['backwards']:
            GENERATOR.loss.backward() #20
            nnutils.clip_grad_norm(GENERATOR.parameters(), GENERATOR.clip_param)#0.01) #1.0)
            GENERATOR.optimizer.step() #21



        GENERATOR.losses_to_average.append(GENERATOR.extract('loss'))
        if len(GENERATOR.losses_to_average) >= GENERATOR.num_losses_to_average:
            GENERATOR.losses.append( na(GENERATOR.losses_to_average).mean() )
            GENERATOR.losses_to_average = []



        if GENERATOR.save():
            DISCRIMINATOR.save(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')




        if True:#try:
            
            if Nets['N0']['P']['runtime_parameters']['show_graphics']:
                if not graphics_on:
                    clp('turning graphics on')
                graphics_on = True
                Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P']) # graphics can cause an error with remote login
            else:
                if graphics_on:
                    clp('turning graphics off')
                    graphics_on = False
                    CA()
        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   






        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*Nets[n]['P']['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))




def Main6_Output_Object(net_str='pro2pros'):

    D = {}

    import torch
    import torch.nn as nn
    import torch.nn.parallel
    import torch.backends.cudnn as cudnn
    import torch.optim as optim
    import torch.utils.data
    import torchvision.datasets as dset
    import torchvision.transforms as transforms
    import torchvision.utils as vutils
    import torch.nn.utils as nnutils

    from discriminator1 import Discriminator,weights_init



    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            #'N0':Net_Main(M=M,sys_str=fire2fireFuture_dcgan_a.replace('\n',' ').replace('\t',' ')),
            'N0':Net_Main(M=M,sys_str=Net_strs[net_str].replace('\n',' ').replace('\t',' ')),
            # 'pro2rgb.dcgan'
        }
    else:
        clp('   FROM COMMMAND LINE   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,Arguments_=Arguments),
        }

    n = 'N0'

    Data = networks.net.make_batch( Nets[n]['get_data_function'], Nets[n]['P'], Nets[n]['P']['batch_size'] )
    cg('Data',shape(Data['input']),shape(Data['target']))

    DISCRIMINATOR = Discriminator(nc=shape(Data['target'])[1]).cuda()
    DISCRIMINATOR.apply(weights_init)
    criterion = nn.BCELoss()
    optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=0.01, betas=(0.5, 0.999))



    run_timer = Timer()
    freq_timer = Timer(30)

    Abort = Toggler()

    wait_timer = Timer(5)

    minute_timer = Timer(60)



    def _function_output(in_imgs):

        if len(in_imgs) > 0:
            in_array = in_imgs[0]
            if len(in_imgs) > 1:
                for i in range(1,len(in_imgs)):
                    in_array = np.concatenate((in_array,in_imgs[i]),axis=2)
            in_array = na([in_array.transpose(2,1,0)])

        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            return False#break

        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            clp('clip',Nets['N0']['P']['clip'],int(run_timer.time()),"`yb")

        
        GENERATOR = Nets[n]['N']
        Nets[n]['P']['original_Fire3_scaling'] = True

        for k in M['Q']['runtime_parameters'].keys():

            Nets[n]['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]

        Data = networks.net.make_batch( Nets[n]['get_data_function'], Nets[n]['P'], Nets[n]['P']['batch_size'] )

        if len(in_imgs) > 0:
            Data['input'] = in_array

        GENERATOR.forward_no_loss(Data) 



        Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P']) # graphics can cause an error with remote login
 
        fake = GENERATOR.extract('output')
        imgs = []
        for i in range(0,shape(Data['target'])[1],3):
            imgs.append(z55(fake[i:i+3,:,:].transpose(2,1,0)))
        return imgs

    D['output'] = _function_output

    return D



do_example = False
if do_example:


    from kzpy3.Learn.main import Main6_Output_Object
    M = Main6_Output_Object('pro2pros')
    a=z55(rnd((94,168,3)))
    b = 0*a; b[:,:,0] = 1
    in_imgs = [a,b]
    imgs = M['output'](in_imgs)

    imgs = M['output']([])
    c = imgs[1]
    a = c.astype(float)
    a -= 0.
    n = 25
    a[a<0] = n
    aa = z55(a);mi(aa,'aaa')
    imgs = M['output']([aa,b])








        







if __name__ == '__main__':

    
        if 'main' not in Arguments or Arguments['main'] == 0:
            clp('*** main0() ***',p=2)
            main0()

        elif Arguments['main'] == 1:
            clp('*** main1() ***',p=2)
            main1()

        elif Arguments['main'] == 2:
            clp('*** main2() ***',p=2)
            main2()


        elif Arguments['main'] == 3:
            clp('*** main3() ***',p=2)
            main3()

        elif Arguments['main'] == 4:
            clp('*** main4() ***',p=2)
            
            if 'net_str' not in Arguments:
                Arguments['net_str'] = ''
            main4()


        elif Arguments['main'] == 5:
            clp('*** main5() ***',p=2)
            main5()


        elif Arguments['main'] == 6:
            kprint(Arguments)
            clp('*** main6() ***',p=2)
            if 'net_str' not in Arguments:
                Arguments['net_str'] = ''
            main6()












#EOF
