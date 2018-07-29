from Parameters_Module import *
import torch
from kzpy3.Train_app.nets.SqueezeNet import SqueezeNet
exec(identify_file_str)




torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P['GPU'])
torch.cuda.device(P['GPU'])


def Pytorch_Network():
    D = {}
    True

    D['net'] = SqueezeNet().cuda()
    D['criterion'] = torch.nn.MSELoss().cuda()
    D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
    D['data_moment_loss_record'] = {}
    D['rate_counter'] = Rate_Counter('batch_size',P['BATCH_SIZE'])
    if P['RESUME']:
        cprint(d2s('Resuming with',P['WEIGHTS_FILE_PATH']),'red')
        save_data = torch.load(P['WEIGHTS_FILE_PATH'])
        D['net'].load_state_dict(save_data['net'])
        time.sleep(4)
    else:
        cprint('Training network from random weights','red')

    def _function_save_net():
        if P['save_net_timer'].check():
            print('saving net state . . .')
            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                weights['net'][key] = weights['net'][key].cuda(device=0)
            torch.save(weights, opj(P['NETWORK_OUTPUT_FOLDER'],'weights',P['SAVE_FILE_NAME']+'_'+time_str()+'.infer'))

            #for mode in ['train','val']:
            #    zsave_obj({'obj':D['loss_record'][mode],'path':opj(P['NETWORK_OUTPUT_FOLDER'],'loss_history',mode+'_loss_record')})

            #so(opj(P['NETWORK_OUTPUT_FOLDER'],'data_moment_loss_records'),D['data_moment_loss_record'])
            print('. . . done saving.')
            P['save_net_timer'].reset()

    D['SAVE_NET'] = _function_save_net
   
    return D




#EOF