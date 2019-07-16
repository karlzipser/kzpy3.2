from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils
exec(identify_file_str)

def Net_Activity(*args):
    """
    show network activiations
    """
    cy("GPUs =",torch.cuda.device_count(),"current GPU =",torch.cuda.current_device())
    Args = args_to_dictionary(args)
    _ = Args['P']
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
                camera_datav = z2o(cv[moment_indexv,:,:,:]).transpose(1,2,0)
                left_t0v = camera_datav[:,:,0:3]
                right_t0v = camera_datav[:,:,3:6]
                left_t1v = camera_datav[:,:,6:9].copy()
                right_t1v = camera_datav[:,:,9:12].copy()
                if _['use_LIDAR']:
                    left_t1v[:,:,0] *= 0
                    right_t1v[:,:,0] *= 0
                #right_t1v = camera_datav[:,:,9:12]
                camera_arrayv = np.array([right_t0v,left_t0v,right_t1v,left_t1v])
                D['imgs'][k][moment_indexv] = vis_square(camera_arrayv,padval=0.5)
            else:
                num_channels = shape(D['activiations'][k])[1]        
                if _['verbose']: print num_channels,shape(D['activiations'][k])[1]
                for i in range(num_channels):
                    if D['activiations'][k][moment_indexv,i,:,:].mean() != 0.0:
                        if D['activiations'][k][moment_indexv,i,:,:].mean() != 1.0:
                            if False:#k == 'pre_metadata_features_metadata' and i > 128:
                                pass
                            else:
                                D['activiations'][k][moment_indexv,i,:,:] = z2o(D['activiations'][k][moment_indexv,i,:,:])
                    #mi(D['activiations'][k][moment_indexv,i,:,:],d2s(i,k))
                D['imgs'][k][moment_indexv] = vis_square2(D['activiations'][k][moment_indexv],padval=0.5)
                
    def _function_view(*args):
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
                """
                continue
                steerv = D['activiations'][final_output][0][:10]
                motorv = D['activiations'][final_output][0][10:]
                figure('steer motor');clf();xylim(0,19,0,1)
                plot(range(10),steerv,'ro-')
                plot(range(10,20,1),motorv,'bo-')
                plot([0,19],[0.49,0.49],'k')
                pause(0.000001)
                continue
                """
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
            if _['verbose']:print(k,Args['moment_index'])
            imgv = D['imgs'][k][Args['moment_index']]
            mi(imgv,d2s(fname(_['project_path']),k,_['start time']))
            #imsave(opjD(k+'.png'),imgv)
            """
            imgv = z2o(imgv)*255
            imgv = imgv.astype(np.uint8)
            imgv = cv2.cvtColor(imgv,color_modev)
            imgv = cv2.resize(imgv, (0,0), fx=scalev, fy=scalev, interpolation=0)
            cv2.imshow(k,imgv)
            """
            
        cv2.waitKey(delayv)
    D['view'] = _function_view
    return D





#EOF
