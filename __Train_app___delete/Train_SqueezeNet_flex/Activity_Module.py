from Parameters_Module import *
exec(identify_file_str)
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils



def Net_Activity(*args):
    """
    show network activiations
    """

    Args = args_to_dictionary(args)
    D = {}
    True
    D['activiations'] = {}
    D['imgs'] = {}

    for k in Args['activiations'].keys():

        D['activiations'][k] = Args['activiations'][k].data.cpu().numpy()

        D['imgs'][k] = {}
        for moment_indexv in [Args['batch_num']]:#in range(shape(D['activiations'][k])[0]):
            #print(k,moment_indexv)
            if k == 'final_output':
                continue
            if k == 'camera_input':
                cv = D['activiations']['camera_input']
                #camera_datav = z2o(cv[moment_indexv,:,:,:]).transpose(1,2,0)
                camera_datav = cv[moment_indexv,:,:,:].transpose(1,2,0)
                left_t0v = camera_datav[:,:,0:3]
                #right_t0v = camera_datav[:,:,3:6]
                #left_t1v = camera_datav[:,:,6:9]
                #right_t1v = camera_datav[:,:,9:12]
                camera_arrayv = np.array([left_t0v])
                vs = vis_square2(camera_arrayv,padval=0.5)
                vs[-1,-1] = -2
                vs[-1,-2] = 2
                D['imgs'][k][moment_indexv] = z2o(vs)

            else:
                num_channels = shape(D['activiations'][k])[1]        
                #print 42,num_channels,shape(D['activiations'][k])[1]
                for i in range(num_channels):
                    if D['activiations'][k][moment_indexv,i,:,:].mean() != 0.0:
                        if D['activiations'][k][moment_indexv,i,:,:].mean() != 1.0:
                            if k == 'pre_metadata_features_metadata' and i > 128:
                                pass
                            else:
                                D['activiations'][k][moment_indexv,i,:,:] = z2o(D['activiations'][k][moment_indexv,i,:,:])
                    #mi(D['activiations'][k][moment_indexv,i,:,:],d2s(i,k))
                D['imgs'][k][moment_indexv] = vis_square2(D['activiations'][k][moment_indexv],padval=0.5)
                
    def _function_view(*args):
        #sbpd2s('in view')
        Args = args_to_dictionary(args)
        if 'scales' in Args:
            Scales = Args['scales']
        else:
            Scales = {}
        if 'delay' in Args:
            delayv = Args['delay']
        else:
            delayv = 33       
        True
        for k in D['imgs'].keys():
            if k == 'final_output':
                continue
            elif k == 'camera_input':
                color_modev = cv2.COLOR_RGB2BGR
            else:
                color_modev = cv2.COLOR_GRAY2BGR
            scalev = 1
            if k in Scales:
                scalev = Scales[k]
            if scalev == 0:
                print('Not shwoing '+k)
                continue
            #print(90,k,Args['moment_index'])
            imgv = D['imgs'][k][Args['moment_index']]
            mi(imgv,d2s(k,P['start time'],P['_flp']))         
        cv2.waitKey(delayv)
    D['view'] = _function_view
    return D





#EOF
