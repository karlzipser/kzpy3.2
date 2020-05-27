from kzpy3.vis3 import *
import networks.net
import Menu.main
from net_main import Net_Main
exec(identify_file_str)

USE_DISCRIMINATOR = False

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))

#python kzpy3/Learn/main_cov.py --main 6 --net_str pts2d2_from_scratch

Net_strs = {
    'pts2d2_from_scratch' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,pts2d2_from_scratch
            --resume True 
            --batch_size 1
            --save_timer_time 300 
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
            --reset_loss False
            --momentum 0.001
            --LR 0.01

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

    if USE_DISCRIMINATOR:
        from discriminator1 import Discriminator,weights_init

    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Net = Net_Main(M=M,sys_str=Net_strs[Arguments['net_str']].replace('\n',' ').replace('\t',' '),Arguments_=Arguments),
        cy(11111,ra=1)
    else:
        clp('   FROM COMMMAND LINE   ','`ybb',ra=0,p=1)
        Net = Net_Main(M=M,Arguments_=Arguments)
        cg(22222,ra=1)
        

    kprint(Net)
    kprint(Net['get_data_function'])
    kprint(Net['P'])
    kprint(Net['P']['batch_size'])

    Data = networks.net.make_batch( Net['get_data_function'], Net['P'], Net['P']['batch_size'] )
    cg('Data',shape(Data['input']),shape(Data['target']))


    if USE_DISCRIMINATOR:
        DISCRIMINATOR = Discriminator(nc=shape(Data['target'])[1]).cuda()


    if USE_DISCRIMINATOR:
        DISCRIMINATOR.apply(weights_init)

    criterion = nn.BCELoss()
    if USE_DISCRIMINATOR:
        optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=0.01, betas=(0.5, 0.999))



    run_timer = Timer()
    freq_timer = Timer(30)

    Abort = Toggler()

    wait_timer = Timer(5)

    minute_timer = Timer(60)

    if USE_DISCRIMINATOR:
        try:
            if Net['P']['resume']:
                DISCRIMINATOR.load(Net['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
        except:
            clp("*** DISCRIMINATOR.load(Net['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan') failed ***",ra=1)


    graphics_on = False


    while True:

        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break

        if minute_timer.check():
            minute_timer.reset()
            Net['P']['clip'] = float(Net['P']['clip'])

            Net['P']['clip'] *= 0.98
            clp('clip',Net['P']['clip'],int(run_timer.time()),"`yb")


        
        GENERATOR = Net['N']
        Net['P']['original_Fire3_scaling'] = True

        for k in M['Q']['runtime_parameters'].keys():
            Net['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]



        Data = networks.net.make_batch( Net['get_data_function'], Net['P'], Net['P']['batch_size'] )

        

        if USE_DISCRIMINATOR:
            DISCRIMINATOR.zero_grad() 
            real = Data['target'][:,:,:,:] 
            label = torch.full((Net['P']['batch_size'],), 1,).cuda() 
            output = DISCRIMINATOR(torch.from_numpy(real).cuda().float()) 

            errD_real = criterion(output, label) 
            errD_real.backward() 
            D_x = output.mean().item() 

        GENERATOR.forward_no_loss(Data) 
        fake = GENERATOR.A['output'][:,:,:,:]
        
        if USE_DISCRIMINATOR:
            label.fill_(0)
            output = DISCRIMINATOR(fake.detach()) 

        if USE_DISCRIMINATOR:
            errD_fake = criterion(output, label) 
            errD_fake.backward() 
            D_G_z1 = output.mean().item() 
            errD = errD_real + errD_fake 
            optimizerD.step() 
        
        GENERATOR.optimizer.zero_grad()

        if USE_DISCRIMINATOR:
            label.fill_(1) 
            output = DISCRIMINATOR(fake) 

        if USE_DISCRIMINATOR:
            if 's' not in Net['P']:
                s = 0.0001
            else:
                s = Net['P']['s']

            GENERATOR.loss = s*GENERATOR.criterion(GENERATOR.A['output'],GENERATOR.A['target']) + (1-s) * criterion(output, label) #19

        else:
            s = 1.0
            GENERATOR.loss = s*GENERATOR.criterion(GENERATOR.A['output'],GENERATOR.A['target'])

        if Net['P']['backwards']:
            GENERATOR.loss.backward() #20
            nnutils.clip_grad_norm(GENERATOR.parameters(), Net['P']['clip'])
            GENERATOR.optimizer.step() #21



        GENERATOR.losses_to_average.append(GENERATOR.extract('loss'))
        if len(GENERATOR.losses_to_average) >= GENERATOR.num_losses_to_average:
            GENERATOR.losses.append( na(GENERATOR.losses_to_average).mean() )
            GENERATOR.losses_to_average = []


        if USE_DISCRIMINATOR:
            if GENERATOR.save():
                DISCRIMINATOR.save(Net['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')




        if True:#try:
            
            if Net['P']['runtime_parameters']['show_graphics']:
                if not graphics_on:
                    clp('turning graphics on')
                graphics_on = True
                Net['graphics_function'](Net['N'],M,Net['P']) # graphics can cause an error with remote login
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
            clp( 'Frequency =', int(np.round(f*Net['P']['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))




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
            'N0':Net_Main(M=M,sys_str=Net_strs[net_str].replace('\n',' ').replace('\t',' ')),
        }
    else:
        clp('   FROM COMMMAND LINE   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,Arguments_=Arguments),
        }

    n = 'N0'

    Data = networks.net.make_batch( Net['get_data_function'], Net['P'], Net['P']['batch_size'] )
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
            return False#

        if minute_timer.check():
            minute_timer.reset()
            Net['P']['clip'] = float(Net['P']['clip'])
            a = Net['P']['clip']
            Net['P']['clip'] *= 0.98
            clp('clip',Net['P']['clip'],int(run_timer.time()),"`yb")

        
        GENERATOR = Net['N']
        Net['P']['original_Fire3_scaling'] = True

        for k in M['Q']['runtime_parameters'].keys():

            Net['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]

        Data = networks.net.make_batch( Net['get_data_function'], Net['P'], Net['P']['batch_size'] )

        if len(in_imgs) > 0:
            Data['input'] = in_array

        GENERATOR.forward_no_loss(Data) 



        Net['graphics_function'](Net['N'],M,Net['P']) # graphics can cause an error with remote login
 
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







Mains = {
    6: main6,
}
        







if __name__ == '__main__':

        if Arguments['main'] == 6:
            kprint(Arguments)
            clp('*** main6() ***',p=2)
            if 'net_str' not in Arguments:
                Arguments['net_str'] = ''
            Mains[6]()












#EOF