from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils





def Net_Activity(*args):
    Args = args_to_dictionary(args)
    _ = {}
    True
    _[activiations] = {}
    _[imgs] = {}

    for k in Args[activiations].keys():
        _[activiations][k] = Args[activiations][k].data.cpu().numpy()
        _[imgs][k] = {}
        for moment_indexv in [0]:#in range(shape(_[activiations][k])[0]):
            #print(k,moment_indexv)
            if k == final_output:
                continue
            if k == camera_input:
                cv = _[activiations][camera_input]
                camera_datav = z2o(cv[moment_indexv,:,:,:]).transpose(1,2,0)
                left_t0v = camera_datav[:,:,0:3] # make this pring out all left and right images in columns
                right_t0v = camera_datav[:,:,3:6]
                left_t1v = camera_datav[:,:,6:9]
                right_t1v = camera_datav[:,:,9+3*6:12+3*6]
                camera_arrayv = np.array([right_t0v,left_t0v,right_t1v,left_t1v])
                _[imgs][k][moment_indexv] = vis_square(camera_arrayv,padval=0.5)
            else:
                _[imgs][k][moment_indexv] = vis_square(_[activiations][k][moment_indexv],padval=0.5)

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
        for k in _[imgs].keys():
            if k == final_output:
                continue
            elif k == camera_input:
                color_modev = cv2.COLOR_RGB2BGR
            else:
                color_modev = cv2.COLOR_GRAY2BGR
            scalev = 1
            if k in Scales:
                scalev = Scales[k]
            if scalev == 0:
                print('Not shwoing '+k)
                continue
            print(k,Args[moment_index])
            imgv = _[imgs][k][Args[moment_index]]
            imgv = z2o(imgv)*255
            imgv=imgv.astype(np.uint8)
            imgv = cv2.cvtColor(imgv,color_modev)
            imgv = cv2.resize(imgv, (0,0), fx=scalev, fy=scalev, interpolation=0)
            cv2.imshow(k,imgv)
        cv2.waitKey(delayv)
    _[view] = _function_view
    return _





#EOF
