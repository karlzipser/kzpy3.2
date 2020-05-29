
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
        wait_timer.trigger()

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

    prev_loss = None

    weight_timer = Timer(30)
    n = 'N0'
    GENERATOR = Nets[n]['N']
    
    graphics_on = False

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
            #print 'clip',Nets['N0']['P']['clip'],int(run_timer.time())
            clp('clip',Nets['N0']['P']['clip'],int(run_timer.time()),"`yb")

        
        
        Nets[n]['P']['original_Fire3_scaling'] = True

        for k in M['Q']['runtime_parameters'].keys():
            Nets[n]['P']['runtime_parameters'][k] = M['Q']['runtime_parameters'][k]


        
        if weight_timer.check():
            try:
                weight_timer.reset()
                current_loss = GENERATOR.losses[-1]#na(GENERATOR.losses[-3:]).mean()
                if prev_loss == None:
                    prev_loss = current_loss
                d = (current_loss - prev_loss) / current_loss
                print(d,current_loss,prev_loss)
                if d > 0.1:
                    clp("if (current_loss - pre_loss) / current_loss > 0.75:",'wrb')
                    GENERATOR.use_stored_weight()
                    Nets['N0']['P']['clip'] /= 2.0
                else:
                    GENERATOR.store_weights()
                prev_loss = current_loss
            except KeyboardInterrupt:
                cr('*** KeyboardInterrupt ***')
                sys.exit()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)        

            

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
        fake = torch.clamp(fake, min=0, max=255)
        #print(fake.min(), fake.max())
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

        s = 0.1 # 0.001
        s = 0.001 # 1/22 13:13
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

        #print n
    #raw_enter()




        
