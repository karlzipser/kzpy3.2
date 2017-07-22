from Parameters_Module import *
import torch
from SqueezeNet import SqueezeNet
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
    _(D,trial_loss_record,equals,{})
    for modev in [train,val]:
	    _(D,epoch_counter,val,equals,0)
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

    return D

"""


def Rate_Counter():
    D = {}
    D['type'] = 'Rate_Counter'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Network rate object')
    D['rate_ctr'] = 0
    D['rate_timer_interval'] = 10.0
    D['rate_timer'] = Timer(D['rate_timer_interval'])
    def _step(d):
        batch_size = d['batch_size']

        D['rate_ctr'] += 1
        if D['rate_timer'].check():
            print(d2s('rate =',dp(batch_size*D['rate_ctr']/D['rate_timer_interval'],2),'Hz'))
            D['rate_timer'].reset()
            D['rate_ctr'] = 0
    D['step'] = _step
    return D   


def save_net(d):
    net = d['net']
    loss_record = d['loss_record']
    if P.save_net_timer.check():
        torch.save(net.state_dict(), opjD(P.save_file_name+time_str()+'.weights'))

        # Save for inference (creates ['net'] and moves net to GPU #0)
        weights = {'net':net.state_dict().copy()}
        for key in weights['net']:
            weights['net'][key] = weights['net'][key].cuda(device=0)
        torch.save(weights, opjD(P.save_file_name+time_str()+'.infer'))

        P.save_net_timer.reset()



def Loss_Record():
    True
    D = {}
    D['t0'] = time.time()
    D['type'] = 'Loss_Record'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','to accumlate losses, timestamp in training and validation')
    D['loss_list'] = []
    D['timestamp_list'] = []
    #ctr_list = []
    D['loss_sum'] = 0
    D['loss_ctr'] = 0
    D['loss_timer'] = Timer(30)
    def _add(d):
        loss = d['loss']
        True
        D['loss_sum'] += loss
        D['loss_ctr'] += 1
        if D['loss_timer'].check():
            D['loss_list'].append(D['loss_sum']/(1.0*D['loss_ctr']))
            D['loss_sum'] = 0
            D['loss_ctr'] = 0
            D['timestamp_list'].append(time.time())
            D['loss_timer'].reset()
    D['add'] = _add
    def _plot(d):
        c = d['c']
        True
        plt.plot((np.array(D['timestamp_list'])-D['t0'])/3600.0,D['loss_list'],c+'.')
    D['plot'] = _plot
    return D



"""

#
#EOF