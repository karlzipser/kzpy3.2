from kzpy3.vis3 import *
import networks.net
import Menu.main
from net_main import Net_Main
exec(identify_file_str)

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))


Net_strs = {
    #Learn --main 4 --net_str Fire2rgbProjections.dcgan
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
            --clip 0.001
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
    """,

##################################################################################
    'pro2pros' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,pro2pros
            --resume True 
            --batch_size 1
            --save_timer_time 300 
            --target_offset 18,36,54,72,90
            --input button,projections 
            --target projections 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3,3,6,6,9,9,12,12,15
            --display.input 0,3,3,6
            --display.target 0,3,3,6,6,9,9,12,12,15
            --clip 1
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
    """,

    'Fire2rgbProjections.dcgan.A' : """

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
            --clip 0.001
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0

    """,

    'pro2rgb.dcgan' : """

        Learn 
            --type ConDecon_Fire_FS,Fire3,pro2rgb.dcgan
            --resume True 
            --batch_size 1
            --save_timer_time 300
            --target_offset 0 
            --input projections 
            --target rgb 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3
            --display.input 0,3 
            --display.target 0,3
            --clip 1
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0.0
            --projection.noise 50
    """,

    'Fire2rgbProjections_' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,Fire2rgbProjections.b
            --resume False 
            --save_timer_time 999999 
            --target_offset 0 
            --input Fire3 
            --target rgb,projections 
            --losses_to_average 256 
            --runs validate 
            --display.output 0,3,3,6 
            --display.input 0,3 
            --display.target 0,3,3,6
            --clip 1
            --backwards True
            --win_x 20
            --win_y 40
            --drop 0

    """,


    'fire2fireFuture' : """
        Learn 
            --type ConDecon_Fire_FS.Fire3.fire2fireFuture.c 
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
            --win_x 20
            --win_y 310
            --drop 0.2

    """,

    # Learn --main 5 --net_str fire2fireFuture.dcgan.a
    'fire2fireFuture.dcgan.a' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,fire2fireFuture.dcgan.a
            --resume True 
            --save_timer_time 300 
            --target_offset 12
            --input button,Fire3 
            --target Fire3 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3 
            --display.input 0,3,3,6
            --display.target 0,3 
            --clip 1
            --backwards True
            --win_x 20
            --win_y 310
            --drop 0
            --height 94
            --width 168
            --original_Fire3_scaling True

    """,


    'all2allFuture.6' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,all2allFuture.6 
            --resume True 
            --save_timer_time 300 
            --target_offset 6 
            --input  button,rgb,projections,Fire3
            --target button,rgb,projections,Fire3 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3,3,6,9,12
            --display.input  0,3,3,6,9,12
            --display.target 0,3,3,6,9,12 
            --clip 1
            --backwards True
            --win_x 20
            --win_y 310
            --drop 0.2

    """,
    'all2allFuture.12' : """
        Learn 
            --type ConDecon_Fire_FS,Fire3,all2allFuture.12 
            --resume True 
            --save_timer_time 300 
            --target_offset 12 
            --input  button,rgb,projections,Fire3
            --target button,rgb,projections,Fire3 
            --losses_to_average 256 
            --runs train 
            --display.output 0,3,3,6,9,12
            --display.input  0,3,3,6,9,12
            --display.target 0,3,3,6,9,12 
            --clip 0.1
            --backwards True
            --win_x 20
            --win_y 310
            --drop 0.2

    """,
}


def main0():
    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,sys_str=all2allFuture_12.replace('\n',' ').replace('\t',' ')),
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

    minute_timer = Timer(60)


  
    while True:
        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break


        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())

        
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

            #print n
            #raw_enter()
        #raw_enter()




def main2():

    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,sys_str=Fire2rgbProjections.replace('\n',' ').replace('\t',' ')),
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

    minute_timer = Timer(60)



    while True:
        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break


        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())


        for n in Nets.keys():

            Nets[n]['P']['original_Fire3_scaling'] = True

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

            #print n
        raw_enter()




def main5():

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
    DISCRIMINATOR = Discriminator(nc=32).cuda()#ngpu).cuda()#.to(device)
    DISCRIMINATOR.apply(weights_init)
    #if _DISCRIMINATOR != '':
    #    DISCRIMINATOR.load_state_dict(torch.load(_DISCRIMINATOR))
    criterion = nn.BCELoss()
    optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=0.01, betas=(0.5, 0.999))


    """
    fire2fireFuture.dcgan.a
    """
    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            #'N0':Net_Main(M=M,sys_str=fire2fireFuture_dcgan_a.replace('\n',' ').replace('\t',' ')),
            'N0':Net_Main(M=M,sys_str=Net_strs[Arguments['net_str']].replace('\n',' ').replace('\t',' ')),

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

    minute_timer = Timer(60)
    #DISCRIMINATOR.load(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
    try:
        if Nets['N0']['P']['resume']:
            DISCRIMINATOR.load(Nets['N0']['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
    except:
        clp("*** DISCRIMINATOR.load(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan') failed ***",ra=1)

    while True:

        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break

        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())


        n = 'N0'
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
        #output = output.view(-1, 1).squeeze(1)
        #print output.size(), output.view(-1, 1).squeeze(1).size()

        #raw_enter()
        errD_real = criterion(output, label) #5
        errD_real.backward() #6
        D_x = output.mean().item() #7

        GENERATOR.forward_no_loss(Data) #8
        fake = GENERATOR.A['output'][:,:,:,:]
        label.fill_(0) #9
        output = DISCRIMINATOR(fake.detach()) #10
        #output = output.view(-1, 1).squeeze(1)

        errD_fake = criterion(output, label) #11
        errD_fake.backward() #12
        D_G_z1 = output.mean().item() #13
        errD = errD_real + errD_fake #14
        optimizerD.step() #15
        
        GENERATOR.optimizer.zero_grad() #16
        label.fill_(1) #17
        output = DISCRIMINATOR(fake) #18
        #output = output.view(-1, 1).squeeze(1)

        s = 0.25
        #GENERATOR.loss =  (1-s) * criterion(output, label) #19
        GENERATOR.loss = s*GENERATOR.criterion(GENERATOR.A['output'],GENERATOR.A['target']) + (1-s) * criterion(output, label) #19


        if Nets[n]['P']['backwards']:
            GENERATOR.loss.backward() #20
            nnutils.clip_grad_norm(GENERATOR.parameters(), GENERATOR.clip_param)#0.01) #1.0)
            GENERATOR.optimizer.step() #21



        GENERATOR.losses_to_average.append(GENERATOR.extract('loss'))
        if len(GENERATOR.losses_to_average) >= GENERATOR.num_losses_to_average:
            GENERATOR.losses.append( na(GENERATOR.losses_to_average).mean() )
            GENERATOR.losses_to_average = []

        #if Nets[n]['P']['backwards']:
        #    GENERATOR.backward()

        if GENERATOR.save():
            DISCRIMINATOR.save(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')

        if True:#try:
            Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P']) # graphics can cause an error with remote login
        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   



        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*Nets[n]['P']['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))

        #print n
    #raw_enter()



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
    DISCRIMINATOR = Discriminator(nc=5*3).cuda()#ngpu).cuda()#.to(device)
    DISCRIMINATOR.apply(weights_init)
    #if _DISCRIMINATOR != '':
    #    DISCRIMINATOR.load_state_dict(torch.load(_DISCRIMINATOR))
    criterion = nn.BCELoss()
    optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=0.01, betas=(0.5, 0.999))


    """
    fire2fireFuture.dcgan.a
    """
    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            #'N0':Net_Main(M=M,sys_str=fire2fireFuture_dcgan_a.replace('\n',' ').replace('\t',' ')),
            'N0':Net_Main(M=M,sys_str=Net_strs[Arguments['net_str']].replace('\n',' ').replace('\t',' ')),

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

    minute_timer = Timer(60)
    #DISCRIMINATOR.load(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
    try:
        if Nets['N0']['P']['resume']:
            DISCRIMINATOR.load(Nets['N0']['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
    except:
        clp("*** DISCRIMINATOR.load(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan') failed ***",ra=1)

    #ctr0 = 0
    #ctr_timer = Timer()
    while True:

        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break

        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())


        n = 'N0'
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
        #output = output.view(-1, 1).squeeze(1)
        #print output.size(), output.view(-1, 1).squeeze(1).size()

        #raw_enter()
        errD_real = criterion(output, label) #5
        errD_real.backward() #6
        D_x = output.mean().item() #7

        GENERATOR.forward_no_loss(Data) #8
        fake = GENERATOR.A['output'][:,:,:,:]
        label.fill_(0) #9
        output = DISCRIMINATOR(fake.detach()) #10
        #output = output.view(-1, 1).squeeze(1)

        errD_fake = criterion(output, label) #11
        errD_fake.backward() #12
        D_G_z1 = output.mean().item() #13
        errD = errD_real + errD_fake #14
        optimizerD.step() #15
        
        GENERATOR.optimizer.zero_grad() #16
        label.fill_(1) #17
        output = DISCRIMINATOR(fake) #18
        #output = output.view(-1, 1).squeeze(1)

        s = 0.25
        #GENERATOR.loss =  (1-s) * criterion(output, label) #19
        GENERATOR.loss = s*GENERATOR.criterion(GENERATOR.A['output'],GENERATOR.A['target']) + (1-s) * criterion(output, label) #19


        if Nets[n]['P']['backwards']:
            GENERATOR.loss.backward() #20
            nnutils.clip_grad_norm(GENERATOR.parameters(), GENERATOR.clip_param)#0.01) #1.0)
            GENERATOR.optimizer.step() #21



        GENERATOR.losses_to_average.append(GENERATOR.extract('loss'))
        if len(GENERATOR.losses_to_average) >= GENERATOR.num_losses_to_average:
            GENERATOR.losses.append( na(GENERATOR.losses_to_average).mean() )
            GENERATOR.losses_to_average = []

        #if Nets[n]['P']['backwards']:
        #    GENERATOR.backward()

        if GENERATOR.save():
            DISCRIMINATOR.save(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')

        if True:#try:
            Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P']) # graphics can cause an error with remote login
        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   

        #ctr0 += 1
        #if ctr0 % 100 == 0:
        #    clp(dp(ctr0 / ctr_timer.time()))

        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*Nets[n]['P']['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))

        #print n
    #raw_enter()




def main4():

    if 'setup':
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



        """
        Learn --main 4 --net_str Fire2rgbProjections.dcgan

        Learn --main 4 --net_str pro2rgb.dcgan
        """
        if 'type' not in Arguments.keys():
            clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
            Nets = {
                'N0':Net_Main(M=M,sys_str=Net_strs[Arguments['net_str']].replace('\n',' ').replace('\t',' ')),
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

        minute_timer = Timer(60)


        from discriminator1 import Discriminator,weights_init
        DISCRIMINATOR = Discriminator(nc=3).cuda()#ngpu).cuda()#.to(device)
        DISCRIMINATOR.apply(weights_init)
        #if _DISCRIMINATOR != '':
        #    DISCRIMINATOR.load_state_dict(torch.load(_DISCRIMINATOR))
        criterion = nn.BCELoss()
        optimizerD = optim.Adam(DISCRIMINATOR.parameters(), lr=0.01, betas=(0.5, 0.999))


        #kprint(Nets['N0']['P'],ra=1)
        try:
            if Nets['N0']['P']['resume']:
                DISCRIMINATOR.load(Nets['N0']['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')
        except:
            clp("*** DISCRIMINATOR.load(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan') failed ***",ra=1)


    while True:

        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break

        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())


        n = 'N0'
        GENERATOR = Nets[n]['N']
        Nets[n]['P']['original_Fire3_scaling'] = True

        for k in M['Q']['runtime_parameters'].keys():
            Nets[n]['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]


        Data = networks.net.make_batch( Nets[n]['get_data_function'], Nets[n]['P'], Nets[n]['P']['batch_size'] )


        #A
        DISCRIMINATOR.zero_grad() #1
        real = Data['target'][:,:3,:,:] #2
        label = torch.full((Nets[n]['P']['batch_size'],), 1,).cuda() #3
        output = DISCRIMINATOR(torch.from_numpy(real).cuda().float()) #4
        #output = output.view(-1, 1).squeeze(1)
        #print output.size(), output.view(-1, 1).squeeze(1).size()

        #raw_enter()
        errD_real = criterion(output, label) #5
        errD_real.backward() #6
        D_x = output.mean().item() #7

        GENERATOR.forward_no_loss(Data) #8
        fake = GENERATOR.A['output'][:,:3,:,:]
        label.fill_(0) #9
        output = DISCRIMINATOR(fake.detach()) #10
        #output = output.view(-1, 1).squeeze(1)

        errD_fake = criterion(output, label) #11
        errD_fake.backward() #12
        D_G_z1 = output.mean().item() #13
        errD = errD_real + errD_fake #14
        optimizerD.step() #15
        
        GENERATOR.optimizer.zero_grad() #16
        label.fill_(1) #17
        output = DISCRIMINATOR(fake) #18
        #output = output.view(-1, 1).squeeze(1)

        s = 0.25
        #GENERATOR.loss =  (1-s) * criterion(output, label) #19
        GENERATOR.loss = s*GENERATOR.criterion(GENERATOR.A['output'],GENERATOR.A['target']) + (1-s) * criterion(output, label) #19

        if Nets[n]['P']['backwards']:
            GENERATOR.loss.backward() #20
            nnutils.clip_grad_norm(GENERATOR.parameters(), GENERATOR.clip_param)#0.01) #1.0)
            GENERATOR.optimizer.step() #21



        GENERATOR.losses_to_average.append(GENERATOR.extract('loss'))
        if len(GENERATOR.losses_to_average) >= GENERATOR.num_losses_to_average:
            GENERATOR.losses.append( na(GENERATOR.losses_to_average).mean() )
            GENERATOR.losses_to_average = []

        #if Nets[n]['P']['backwards']:
        #    GENERATOR.backward()

        if GENERATOR.save():
            DISCRIMINATOR.save(Nets[n]['P']['NETWORK_OUTPUT_FOLDER']+'.dcgan')

        if True:#try:
            Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P']) # graphics can cause an error with remote login
        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            clp('Exception!','`wrb',exc_type, file_name, exc_tb.tb_lineno)   



        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*Nets[n]['P']['batch_size'])), 'Hz, run time =',format_seconds(run_timer.time()))

        #print n
    #raw_enter()




def main3():

    if 'type' not in Arguments.keys():
        clp('   FROM SYS_STR   ','`ybb',ra=0,p=1)
        Nets = {
            'N0':Net_Main(M=M,sys_str=Fire2rgbProjections_.replace('\n',' ').replace('\t',' ')),
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

    minute_timer = Timer(60)



    while True:
        M['load']()
        if Abort['test'](M['Q']['runtime_parameters']['abort']):
            break


        if minute_timer.check():
            minute_timer.reset()
            Nets['N0']['P']['clip'] = float(Nets['N0']['P']['clip'])
            a = Nets['N0']['P']['clip']
            #cg(a,type(a))
            Nets['N0']['P']['clip'] *= 0.98
            print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())


        for n in Nets.keys():

            Nets[n]['P']['original_Fire3_scaling'] = True

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

            #print n
        #raw_enter()





def main1():


    Nets = {
        'N1':Net_Main(M=M,sys_str = Net_strs['Fire2rgbProjections.dcgan'].replace('\n',' ').replace('\t',' ')),
        'N0':Net_Main(M=M,sys_str = Net_strs['fire2fireFuture.dcgan.a'].replace('\n',' ').replace('\t',' ')),
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
            Nets[n]['P']['original_Fire3_scaling'] = True
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
            Out_data2['input'][0,3:35,:,:] = Nets['N0']['N'].extract('output')
            #t = cv2.resize(Out_data2['input'][0,:,:,:],(168/4,94/4))
            #t = cv2.resize(t,(168,94))
            #Out_data2['input'][0,:,:,:] = t
            Out_data2['input'][0,3:35,:,:] =  z2o(Out_data2['input'][0,3:35,:,:]) * 15.

            Out_data2['target'] = 0*Nets['N0']['Duplicates']['target']
            Data = Out_data2


        for n in Nets.keys():
            Nets[n]['P']['original_Fire3_scaling'] = True






        for k in Data:
            print 'Data',k,shape(Data[k]),Data[k].min(),Data[k].max()
        print

        #print Nets['N0']['N']
        #print Nets['N0']['N'].forward_no_loss
        Nets['N0']['N'].forward_no_loss(Data)
        #Nets[n]['N'].forward(Data)

        if True:
            Out_data = {}
            Out_data['input'] = na([Nets['N0']['N'].extract('output')])
            Out_data['target'] = 0*Nets['N1']['Duplicates']['target']


            for k in Out_data:
                print 'dup1',k,shape(Nets['N1']['Duplicates'][k])
            for k in Out_data:
                print 'Out_data',k,shape(Out_data[k])
            print
            Nets['N1']['N'].forward_no_loss(Out_data)
 




        if False:
            for k in Out_data2:
                print 'dup2',k,shape(Nets['N0']['Duplicates'][k])
            for k in Out_data2:
                print 'Out_data2',k,shape(Out_data2[k])
            print


        for n in Nets.keys():
            Nets[n]['graphics_function'](Nets[n]['N'],M,Nets[n]['P'])

        
        kprint(ctr,'ctr',ra=1)

        ctr += 1

        







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
