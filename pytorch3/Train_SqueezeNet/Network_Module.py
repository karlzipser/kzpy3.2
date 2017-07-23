from Parameters_Module import *
import torch
from SqueezeNet import SqueezeNet
from vis2 import *
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
    D[loss_record] = {}
    for modev in [train,val]:
        D[epoch_counter][modev] = 0
        D[loss_record][modev] = Loss_Record()
    if _(P,RESUME):
        cprint(d2s('Resuming with',_(P,WEIGHTS_FILE_PATH)),'yellow')
        save_data = torch.load(_(P,WEIGHTS_FILE_PATH))
        _(D,net).load_state_dict(save_data)
        time.sleep(4)
        #loss_record_loaded = zload_obj({'path':opjD('loss_record')})
        #loss_record = {}
        #for mode in ['train','val']:
        #    loss_record[mode] = Utils.Loss_Record()
        #    for k in loss_record_loaded[mode].keys():
        #        if not callable(loss_record[mode][k]):
        #            loss_record[mode][k] = loss_record_loaded[mode][k]
    else:
        pass
        #loss_record = {}
        #loss_record['train'] = Utils.Loss_Record()
        #loss_record['val'] = Utils.Loss_Record()
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
            for modev in [train,val]:
                zsave_obj({'obj':D[loss_record][modev],'path':opj(P[NETWORK_OUTPUT_FOLDER],'loss_history',modev+'_loss_record')})

            so(opj(P[NETWORK_OUTPUT_FOLDER],'data_moment_loss_records'),D[data_moment_loss_record])
            print('. . . done saving.')
            P[save_net_timer].reset()
    D[save_net] = _function_save_net
   
    return D



# loss_history
# data_moment_loss_record

  





def Loss_Record():
    True
    D = {}
    D['t0'] = time.time()
    D['type'] = 'Loss_Record'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','to accumlate losses, timestamp in training and validation')
    D['loss_list'] = []
    D['timestamp_list'] = []
    D['ctr_list'] = []
    D['loss_sum'] = 0
    D['loss_ctr'] = 0
    D['ctr'] = 0
    D['loss_timer'] = Timer(30)
    def _add(*args):
        Args = args_to_dictionary(args)
        lossv = Args[loss]
        alt_ctrv = Args['alt_ctr']
        D['ctr'] = max(D['ctr'],alt_ctrv+1)
        True
        D['loss_sum'] += lossv
        D['loss_ctr'] += 1
        if D['loss_timer'].check():
            D['loss_list'].append(D['loss_sum']/(1.0*D['loss_ctr']))
            D['loss_sum'] = 0
            D['loss_ctr'] = 0
            D['timestamp_list'].append(time.time())
            D['ctr_list'].append(D['ctr'])
            D['graph']('color',Args['color'])
            D['loss_timer'].reset()
        D['ctr'] += P[BATCH_SIZE]
    D[add] = _add
    def _function_graph(*args):
        Args = args_to_dictionary(args)
        c = Args['color']
        True
        figure('loss')
        plt.plot(D['ctr_list'],D['loss_list'],c+'.')
    D['graph'] = _function_graph
    return D





#
#EOF