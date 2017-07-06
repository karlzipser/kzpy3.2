from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch2'])
from vis2 import *
import Parameters as P
import torch


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
        torch.save(net.state_dict(), opjD('save_file'+time_str()+'.weights'))

        # Save for inference (creates ['net'] and moves net to GPU #0)
        weights = {'net':net.state_dict().copy()}
        for key in weights['net']:
            weights['net'][key] = weights['net'][key].cuda(device=0)
        torch.save(weights, opjD('save_file'+time_str()+'.infer'))

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
        plt.plot(np.array(D['timestamp_list'])-D['t0'],D['loss_list'],c+'.')
    D['plot'] = _plot
    return D


