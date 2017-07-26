from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils

#img_saver = Image_to_Folder_Saver({'path':opjD('cameras0')})

_ = dictionary_access


def Batch(*args):
    Args = args_to_dictionary(args)
    D = {}
    D[network] = Args[network]
    True
    _(D,batch_size,equals,P[BATCH_SIZE])
    D[dic_type] = 'Batch'
    D[purpose] = d2s(inspect.stack()[0][3],':','object to collect data for pytorch batch')
    D[camera_data] = torch.FloatTensor().cuda()
    D[metadata] = torch.FloatTensor().cuda()
    D[target_data] = torch.FloatTensor().cuda()
    D[names] = []
    D[states] = []


    def _function_fill(*args):
        Args = args_to_dictionary(args)
        True
        D[data_ids] = []
        for b_ in range(D[batch_size]):
            Data_moment = None
            while Data_moment == None:
                ev = Args[data][next](mode,Args[mode], network,D[network])
                run_codev = ev[3]
                seg_numv = ev[0]
                offsetv = ev[1]
                Data_moment = _(Args[data],get_data)(run_code,run_codev, seg_num,seg_numv, offset,offsetv)
            D[data_ids].append((run_codev,seg_numv,offsetv))
            _function_data_into_batch(data_moment,Data_moment)
        D[data_ids].reverse() # this is to match way batch is filled up below


    def _function_data_into_batch(*args):
        Args = args_to_dictionary(args)
        Data_moment = Args[data_moment]
        True
        if True:
            D[names].insert(0,Data_moment[name]) # This to match torch.cat use below
        if True:
            list_camera_input = []
            for t in range(D[network][net].N_FRAMES):
                for camerav in (left, right):
                    list_camera_input.append(torch.from_numpy(Data_moment[camerav][t]))
            camera_datav = torch.cat(list_camera_input, 2)
            camera_datav = camera_datav.cuda().float()/255. - 0.5
            camera_datav = torch.transpose(camera_datav, 0, 2)
            camera_datav = torch.transpose(camera_datav, 1, 2)
            D[camera_data] = torch.cat((torch.unsqueeze(camera_datav, 0), D[camera_data]), 0)
        if True:
            mode_ctrv = 0
            metadatav = torch.FloatTensor().cuda()
            zero_matrixv = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
            one_matrixv = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
            for cur_labelv in [racing, caffe, follow, direct, play, furtive]:
                mode_ctrv += 1
                if cur_labelv == caffe:

                    if Data_moment[states][0]:
                        metadatav = torch.cat((one_matrixv, metadatav), 1)
                        print cur_labelv
                        raw_input('here')
                    else:
                        metadatav = torch.cat((zero_matrixv, metadatav), 1)
                else:
                    if Data_moment[labels][cur_labelv]:
                        #print cur_labelv
                        
                        metadatav = torch.cat((one_matrixv, metadatav), 1)
                    else:
                        metadatav = torch.cat((zero_matrixv, metadatav), 1)
            if LCR in Data_moment[labels]:
                #print data['states']
                for target_statev in [1,2,3]:
                    for i in range(0,len(Data_moment[states]),3): ###############!!!!!!!!!!!!!!!! temp, generalize
                        mode_ctrv += 1
                        #!!!!!!!! reverse concatinations so they are in normal order
                        if Data_moment[states][i] == target_statev:
                            metadatav = torch.cat((one_matrixv, metadatav), 1)
                        else:
                            metadatav = torch.cat((zero_matrixv, metadatav), 1)

            for i in range(128 - mode_ctrv): # Concatenate zero matrices to fit the dataset
                metadatav = torch.cat((zero_matrixv, metadatav), 1)

            D[metadata] = torch.cat((metadatav, D[metadata]), 0)

        if True:
            sv = Data_moment[steer]
            mv = Data_moment[motor]
            rv = range(2,31,3) # This depends on NUM_STEPS and STRIDE
            sv = array(sv)[rv]
            mv = array(mv)[rv]
            steerv = torch.from_numpy(sv).cuda().float() / 99.
            motorv = torch.from_numpy(mv).cuda().float() / 99.
            target_datav = torch.unsqueeze(torch.cat((steerv, motorv), 0), 0)
            D[target_data] = torch.cat((target_datav, D[target_data]), 0)
            D[states].append(Data_moment[states])



    def _function_clear():
        D[camera_data] = torch.FloatTensor().cuda()
        D[metadata] = torch.FloatTensor().cuda()
        D[target_data] = torch.FloatTensor().cuda()
        D[states] = []
        D[names] = []
        D[outputs] = None
        D[loss] = None



    def _function_forward():
        True
        Trial_loss_record = D[network][data_moment_loss_record]
        D[network][optimizer].zero_grad()
        D[outputs] = D[network][net](torch.autograd.Variable(D[camera_data]), torch.autograd.Variable(D[metadata])).cuda()
        D[loss] = D[network][criterion](D[outputs], torch.autograd.Variable(D[target_data]))
        for bv in range(D[batch_size]):
            id = D[data_ids][bv]
            tv= D[target_data][bv].cpu().numpy()
            ov = D[outputs][bv].data.cpu().numpy()
            av = tv - ov
            #Trial_loss_record[(id,tuple(tv),tuple(ov))] = np.sqrt(av * av).mean()
            Trial_loss_record[id] = np.sqrt(av * av).mean()
        D[network][rate_counter][step]()



    def _function_backward():
        True
        D[loss].backward()
        nnutils.clip_grad_norm(D[network][net].parameters(), 1.0)
        D[network][optimizer].step()



    def _function_display(*args):
        Args = args_to_dictionary(args)
        if print_now not in Args:
            Args[print_now] = False
        True
        if P[print_timer].check() or Args[print_now]:

            ov = D[outputs][0].data.cpu().numpy()

            tv = D[target_data][0].cpu().numpy()

            print('Loss:',dp(D[loss].data.cpu().numpy()[0],5))
            #print(o,t,D['data_ids'])
            av = D[camera_data][0][:].cpu().numpy()
            bv = av.transpose(1,2,0)
            hv = shape(av)[1]
            wv = shape(av)[2]
            cv = zeros((10+hv*2,10+2*wv,3))
            cv[:hv,:wv,:] = z2o(bv[:,:,3:6])
            cv[:hv,-wv:,:] = z2o(bv[:,:,:3])
            cv[-hv:,:wv,:] = z2o(bv[:,:,9:12])
            cv[-hv:,-wv:,:] = z2o(bv[:,:,6:9])
            mi(cv,'cameras');pause(0.000000001)
            print(av.min(),av.max())
            print(D[states][-1])
            #img_saver['save']({'img':c})
            figure('steer')
            clf()
            ylim(-0.05,1.05);xlim(0,len(tv))
            plot([-1,60],[0.49,0.49],'k');plot(ov,'og'); plot(tv,'or'); plt.title(D[names][0])
            pause(0.000000001)
            P[print_timer].reset()

    D[fill] = _function_fill
    D[clear] = _function_clear
    D[forward] = _function_forward
    D[backward] = _function_backward
    D[display] = _function_display
    return D




#EOF
