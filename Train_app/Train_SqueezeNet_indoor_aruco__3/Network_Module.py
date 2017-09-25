from Parameters_Module import *
import torch
#import Loss_Record_Module
from Train_app.nets.SqueezeNet import SqueezeNet
exec(identify_file_str)


_ = dictionary_access


torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(_(P,GPU))
torch.cuda.device(_(P,GPU))


def Pytorch_Network():
    D = {}
    True
    _(D,dic_type,equals,'Pytorch_Network')
    _(D,purpose,equals,d2s(inspect.stack()[0][3],':','Object network.'))
    _(D,net,equals,SqueezeNet().cuda())
    _(D,criterion,equals,torch.nn.MSELoss().cuda())
    _(D,optimizer,equals,torch.optim.Adadelta(D[net].parameters()))
    _(D,data_moment_loss_record,equals,{})
    D[rate_counter] = Rate_Counter(batch_size,P[BATCH_SIZE])
    D[epoch_counter] = {}
    #D[loss_record] = {}
    for modev in [train,val]:
        D[epoch_counter][modev] = 0
        #D[loss_record][modev] = Loss_Record_Module.Loss_Record()
    if _(P,RESUME):
        cprint(d2s('Resuming with',_(P,WEIGHTS_FILE_PATH)),'yellow')
        save_data = torch.load(_(P,WEIGHTS_FILE_PATH))
        _(D,net).load_state_dict(save_data[net])
        time.sleep(4)

    else:
        pass

    def _function_save_net():
        #loss_record = d['loss_record']
        if P[save_net_timer].check():
            print('saving net state . . .')
            #torch.save(net.state_dict(), opjD(P.save_file_name+time_str()+'.weights'))
            # Save for inference (creates ['net'] and moves net to GPU #0)
            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                weights['net'][key] = weights['net'][key].cuda(device=0)
            torch.save(weights, opj(P[NETWORK_OUTPUT_FOLDER],'weights',P[SAVE_FILE_NAME]+'_'+time_str()+'.infer'))
            #for modev in [train,val]:
            #    zsave_obj({'obj':D[loss_record][modev],'path':opj(P[NETWORK_OUTPUT_FOLDER],'loss_history',modev+'_loss_record')})

            #so(opj(P[NETWORK_OUTPUT_FOLDER],'data_moment_loss_records'),D[data_moment_loss_record])
            print('. . . done saving.')
            P[save_net_timer].reset()
    D[save_net] = _function_save_net
   
    return D




#EOF