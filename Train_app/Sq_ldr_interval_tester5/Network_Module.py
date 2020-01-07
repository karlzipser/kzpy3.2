from kzpy3.utils3 import *
import torch
#from kzpy3.Train_app.nets.SqueezeNet40_global_A import SqueezeNet
from kzpy3.Train_app.nets.SqueezeNet_ldr_interval import SqueezeNet


exec(identify_file_str)

def Pytorch_Network(_):
    """
    print(_['NETWORK_OUTPUT_FOLDER'])
    print(_['INITIAL_WEIGHTS_FOLDER'])
    print(_['WEIGHTS_FILE_PATH'])
    """
    D = {}
    torch.set_default_tensor_type('torch.FloatTensor') 
    torch.cuda.set_device(_['GPU'])
    torch.cuda.device(_['GPU'])
    cg("GPUs =",torch.cuda.device_count(),"current GPU =",torch.cuda.current_device())

    D['net'] = SqueezeNet().cuda()





    D['criterion'] = torch.nn.MSELoss().cuda()
    if False: #original
        D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
    D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters()))
    try:
        for folder in ['weights','loss','dm_ctrs','state_dict','optimizer']:
            unix(d2s('mkdir -p',opj(_['NETWORK_OUTPUT_FOLDER'],folder)))
    except:
        cr('*** Failed to create default network output folders ***')

    def _function_save_net():
        if _['save_net_timer'].check():
            pd2s('2 lr=',D['net'].lr)
            print('saving net state . . .')

            weights = {'net':D['net'].state_dict().copy()}
            for key in weights['net']:
                weights['net'][key] = weights['net'][key].cuda(device=0)
            torch.save(weights, opj(_['NETWORK_OUTPUT_FOLDER'],'weights',_['SAVE_FILE_NAME']+'_'+time_str()+'.infer'))
            so(_['LOSS_LIST_AVG'],opj(_['NETWORK_OUTPUT_FOLDER'],'loss',_['SAVE_FILE_NAME']+'_'+time_str()+'.loss_avg'))
            if 'dm_ctrs' in _:
                so(_['dm_ctrs'],opj(_['NETWORK_OUTPUT_FOLDER'],'dm_ctrs',_['SAVE_FILE_NAME']+'_'+time_str()+'.dm_ctrs'))
            torch.save(D['optimizer'].state_dict(), opj(_['NETWORK_OUTPUT_FOLDER'],'optimizer',_['SAVE_FILE_NAME']+'_'+time_str()+'.optimizer_state'))
            torch.save(D['net'].state_dict(), opj(_['NETWORK_OUTPUT_FOLDER'],'state_dict',_['SAVE_FILE_NAME']+'_'+time_str()+'.state_dict'))
            print('. . . done saving.')
            _['save_net_timer'].reset()

    D['SAVE_NET'] = _function_save_net

    if _['RESUME']:


        if _['freeze premetadata weights']:

            def load_net(path):
                save_data = torch.load(path)
                net = save_data['net']
                return net

            A = load_net(most_recent_file_in_folder(opjD('Networks/net_24Dec2018_12imgs_projections/weights'),['.infer'],[]))
            B = load_net(_['WEIGHTS_FILE_PATH'])

            for l in ['pre_metadata_features.0.weight',
                     'pre_metadata_features.0.bias',
                     'pre_metadata_features.3.squeeze.weight',
                     'pre_metadata_features.3.squeeze.bias',
                     'pre_metadata_features.3.expand1x1.weight',
                     'pre_metadata_features.3.expand1x1.bias',
                     'pre_metadata_features.3.expand3x3.weight',
                     'pre_metadata_features.3.expand3x3.bias',]:
                cy("Copying",l,'from',_['update premetadata weights from other model'])
                B[l] = A[l]
            weights = {'net':B}
            torch.save(weights,opj(_['NETWORK_OUTPUT_FOLDER'],'weights','merged.infer'))

        try:
            if len(sggo(_['WEIGHTS_FILE_PATH'])) > 0:
                

                if _['freeze premetadata weights']:
                    cprint(d2s('Resuming with',opj(_['NETWORK_OUTPUT_FOLDER'],'weights','merged.infer')),'red')
                    save_data = torch.load(opj(_['NETWORK_OUTPUT_FOLDER'],'weights','merged.infer'))
                else:
                    cprint(d2s('Resuming with',_['WEIGHTS_FILE_PATH']),'red')
                    save_data = torch.load(_['WEIGHTS_FILE_PATH'])

                D['net'].load_state_dict(save_data['net'])

                if False:
                    _['save_net_timer'].trigger()
                    D['SAVE_NET']()
                    raw_enter('This is STRANGE too!!!')

            if _['freeze premetadata weights']:
                ctr = 0
                for param in D['net'].parameters():
                    rg = True
                    if ctr < 8:
                        rg = False
                    param.requires_grad = rg
                    if rg:
                        f = cg
                    else:
                        f = cr
                    f(ctr,param.size())
                    ctr += 1

            else:
                CS_("Could not load "+_['WEIGHTS_FILE_PATH'])
            m = most_recent_file_in_folder( opj(_['NETWORK_OUTPUT_FOLDER'],'loss') )
            if m:
                CS_("loading "+m)
                _['LOSS_LIST_AVG'] = lo(m)
            else:
                CS_("Could not load loss")
            m = most_recent_file_in_folder(opj(_['NETWORK_OUTPUT_FOLDER'],'optimizer'))
            if m:
                CS_("loading "+m)
                D['optimizer'].load_state_dict(torch.load(m))
                pd2s('1 lr=',D['net'].lr)
            else:
                CS_("Could not load optimizer")
            m = most_recent_file_in_folder(opj(_['NETWORK_OUTPUT_FOLDER'],'state_dict'))
            """
            # This always fails
            if m:
                CS_("loading "+m)
                torch.load(D['net'].state_dict(),m)
            else:
                CS_("Could not load state_dict")
            """
            
        except Exception as e:
            CS_("********** Network_Module.py Exception ***********************")
            print(e.message, e.args)
            cr("*** D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters())) ***") 
            if False: #original
                D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
            D['optimizer'] = torch.optim.Adadelta(filter(lambda p: p.requires_grad,D['net'].parameters())) 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            time.sleep(4)
    else:
        cprint('Training network from random weights','red')


   
    return D




#EOF