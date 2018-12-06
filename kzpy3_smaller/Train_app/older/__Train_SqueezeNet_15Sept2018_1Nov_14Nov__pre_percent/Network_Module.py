from Parameters_Module import *
import torch
from kzpy3.Train_app.nets.SqueezeNet40 import SqueezeNet
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

    for folder in ['weights','loss','dm_ctrs','state_dict','optimizer']:
        unix(d2s('mkdir -p',opj(P['NETWORK_OUTPUT_FOLDER'],folder)))

    def _function_save_net():
        if P['save_net_timer'].check():
            pd2s('2 lr=',D['net'].lr)
            print('saving net state . . .')

            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                weights['net'][key] = weights['net'][key].cuda(device=0)
            torch.save(weights, opj(P['NETWORK_OUTPUT_FOLDER'],'weights',P['SAVE_FILE_NAME']+'_'+time_str()+'.infer'))
            so(P['LOSS_LIST_AVG'],opj(P['NETWORK_OUTPUT_FOLDER'],'loss',P['SAVE_FILE_NAME']+'_'+time_str()+'.loss_avg'))
            if 'dm_ctrs' in P:
                so(P['dm_ctrs'],opj(P['NETWORK_OUTPUT_FOLDER'],'dm_ctrs',P['SAVE_FILE_NAME']+'_'+time_str()+'.dm_ctrs'))
            torch.save(D['optimizer'].state_dict(), opj(P['NETWORK_OUTPUT_FOLDER'],'optimizer',P['SAVE_FILE_NAME']+'_'+time_str()+'.optimizer_state'))
            torch.save(D['net'].state_dict(), opj(P['NETWORK_OUTPUT_FOLDER'],'state_dict',P['SAVE_FILE_NAME']+'_'+time_str()+'.state_dict'))
            print('. . . done saving.')
            P['save_net_timer'].reset()

    D['SAVE_NET'] = _function_save_net

    if P['RESUME']:
        try:
            if len(sggo(P['WEIGHTS_FILE_PATH'])) > 0:
                cprint(d2s('Resuming with',P['WEIGHTS_FILE_PATH']),'red')
                save_data = torch.load(P['WEIGHTS_FILE_PATH'])
                CS_("loading "+P['WEIGHTS_FILE_PATH'])


                if False:#'Temp!!!!!!!!!!!!!!!':
                    raw_enter('This is STRANGE!!! ')
                    a=save_data['net']['final_output.1.bias'].cpu().numpy()
                    b=zeros(40)
                    b[:20]=a
                    b[-20:]=a
                    save_data['net']['final_output.1.bias'] = torch.from_numpy(b).cuda()

                    a=save_data['net']['final_output.1.weight'].cpu().numpy()
                    b=zeros((40,512,1,1))
                    b[:20,:,:,:]=a
                    b[-20:,:,:,:]=a
                    save_data['net']['final_output.1.weight'] = torch.from_numpy(b).cuda()
                    print(shape(save_data['net']['final_output.1.weight'].cpu().numpy()))
                    raw_enter()

                D['net'].load_state_dict(save_data['net'])

                if False:
                    P['save_net_timer'].trigger()
                    D['SAVE_NET']()
                    raw_enter('This is STRANGE too!!!')
            else:
                CS_("Could not load "+P['WEIGHTS_FILE_PATH'])
            m = most_recent_file_in_folder( opj(P['NETWORK_OUTPUT_FOLDER'],'loss') )
            if m:
                CS_("loading "+m)
                P['LOSS_LIST_AVG'] = lo(m)
            else:
                CS_("Could not load loss")
            m = most_recent_file_in_folder(opj(P['NETWORK_OUTPUT_FOLDER'],'optimizer'))
            if m:
                CS_("loading "+m)
                D['optimizer'].load_state_dict(torch.load(m))
                pd2s('1 lr=',D['net'].lr)
            else:
                CS_("Could not load optimizer")
            m = most_recent_file_in_folder(opj(P['NETWORK_OUTPUT_FOLDER'],'state_dict'))
            if m:
                CS_("loading "+m)
                torch.load(D['net'].state_dict(),m)
            else:
                CS_("Could not load state_dict")
            
        except Exception as e:
            CS_("********** Network_Module.py Exception ***********************")
            print(e.message, e.args)            
            D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            time.sleep(4)
    else:
        cprint('Training network from random weights','red')


   
    return D




#EOF