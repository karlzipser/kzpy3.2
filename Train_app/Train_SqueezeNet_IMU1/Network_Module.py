from Parameters_Module import *
import torch

from SqueezeNet_IMU import SqueezeNet
exec(identify_file_str)


torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P[GPU])
torch.cuda.device(P[GPU])


def Pytorch_Network():
    _ = {}
    True
    _[NET] = SqueezeNet().cuda()
    _[criterion] = torch.nn.MSELoss().cuda()
    _[optimizer] = torch.optim.Adadelta(_[NET].parameters())
    _[data_moment_loss_record] = {}
    _[rate_counter] = Rate_Counter(batch_size,P[BATCH_SIZE])
    _[epoch_counter] = {}
    for modev in [train,val]:
        _[epoch_counter][modev] = 0
    if P[RESUME]:
        cprint(d2s('Resuming with',P[WEIGHTS_FILE_PATH]),'yellow')
        save_data = torch.load(P[WEIGHTS_FILE_PATH])
        _[NET].load_state_dict(save_data['net'])
        time.sleep(4)
    else:
        pass

    def _function_save_net():
        if P[SAVE_NET_TIMER].check():
            print('saving NET state . . .')

            weights = {NET:_[NET].state_dict().copy()}
            for key in weights[NET]:
                weights[NET][key] = weights[NET][key].cuda(device=0)
            torch.save(weights, opj(P[NETWORK_OUTPUT_FOLDER],'weights',P[SAVE_FILE_NAME]+'_'+time_str()+'.infer'))

            print('. . . done saving.')
            P[SAVE_NET_TIMER].reset()
    _[SAVE_NET] = _function_save_net
   
    return _




#EOF