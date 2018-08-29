from kzpy3.utils3 import *
import torch
import torch.nn.utils as nnutils
from kzpy3.Train_app.nets.Z1dconvnet0 import Z1dconvnet0
exec(identify_file_str)

torch.set_default_tensor_type('torch.FloatTensor')

if HAVE_GPU:
    torch.cuda.set_device(0)
    torch.cuda.device(0)


def Pytorch_Network(weights_file_path,network_output_folder,safe_file_name,resuming=True,loss_list_n=30):
    D = {}
    D['loss list'],D['loss list average'] = [],[]
    D['loss timer'] = Timer(10)
    D['save net timer'] = Timer(60*20)
    if HAVE_GPU:
        D['net'] = Z1dconvnet0().cuda()
        D['criterion'] = torch.nn.MSELoss().cuda()
    else:
        D['net'] = Z1dconvnet0()#.cuda()
        D['criterion'] = torch.nn.MSELoss()#.cuda()
    try:
        assert resuming == True
        cprint(d2s('Resuming with',weights_file_path,'red'))
        save_data = torch.load(weights_file_path)
        D['net'].load_state_dict(save_data['net'])
        D['loss list average'] = lo(most_recent_file_in_folder(opj(network_output_folder,'loss')))
        #try:
        D['optimizer'].load_state_dict(torch.load(most_recent_file_in_folder(opj(network_output_folder,'optimizer'))))
        #except:
        #    print 'unable load_state of optimizer'
        #    D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
        time.sleep(4)
    except:
        cprint('Training network from random weights','red')
        D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)


    def _function_save_net():
        if D['save net timer'].check():
            print('saving net state . . .')
            for folder in ['weights','loss','dm_ctrs','state_dict','optimizer']:
                unix(d2s('mkdir -p',opj(network_output_folder,folder)))
            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                if HAVE_GPU:
                    weights['net'][key] = weights['net'][key].cuda(device=0)
                else:
                    weights['net'][key] = weights['net'][key]#.cuda(device=0)
            torch.save(weights, opj(network_output_folder,'weights',safe_file_name+'_'+time_str()+'.infer'))
            so(D['loss list average'],opj(network_output_folder,'loss',safe_file_name+'_'+time_str()+'.loss_avg'))
            #so(P['dm_ctrs'],opj(network_output_folder,'dm_ctrs',safe_file_name+'_'+time_str()+'.dm_ctrs'))
            torch.save(D['optimizer'].state_dict(), opj(network_output_folder,'optimizer',safe_file_name+'_'+time_str()+'.optimizer_state'))
            torch.save(D['net'].state_dict(), opj(network_output_folder,'state_dict',safe_file_name+'_'+time_str()+'.state_dict'))
            print('. . . done saving.')
            D['save net timer'].reset()

    D['save net'] = _function_save_net


    def _function_forward(the_input,the_target):
        pass
        D['optimizer'].zero_grad()
        D['outputs'] = D['net'](torch.autograd.Variable(the_input))
        D['loss'] = D['criterion'](D['outputs'],torch.autograd.Variable(the_target))
        #if D['loss timer'].check():
        #    print D['loss']
        #    D['loss timer'].reset()

    D['forward'] = _function_forward


    def _function_backward():
        try:
            D['loss'].backward()
            nnutils.clip_grad_norm(D['net'].parameters(), 1.0)
            D['optimizer'].step()    
            D['loss list'].append(D['loss'].data.cpu().numpy()[:].mean())
            if len(D['loss list']) > loss_list_n:
                D['loss list average'].append(na(D['loss list']).mean())
                D['loss list'] = []
        except Exception as e:
            print("********** Exception ****** def _function_backward(): failed!!!! *****************")
            print(e.message, e.args)
            #exec(EXCEPT_STR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

    D['backward'] = _function_backward

    return D




#EOF