from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils





def Net_Activity(**Args):
    _ = {}
    _[ACTIVATIONS] = {}
    _[imgs] = {}

    for k in Args[ACTIVATIONS].keys():
        #print k
        _[ACTIVATIONS][k] = Args[ACTIVATIONS][k].data.cpu().numpy()
        _[imgs][k] = {}
        for moment_indexv in [0]:#in range(shape(_[ACTIVATIONS][k])[0]):
            #print(k,moment_indexv)
            if k == final_output:
                continue
            if k == camera_input:
                cv = _[ACTIVATIONS][camera_input]
                camera_datav = z2o(cv[moment_indexv,:,:,:])#.transpose(1,2,0)
                img_list = []
                for i in range(shape(camera_datav)[0]):
                    mi(camera_datav[i,:,:],i)
                #_[imgs][k][moment_indexv] = vis_square(array(img_list),padval=0.5)
            else:
                mi(vis_square(_[ACTIVATIONS][k][moment_indexv],padval=0.5),k);spause()

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
                #print('Not shwoing '+k)
                continue

        cv2.waitKey(delayv)
    _[view] = _function_view
    return _





#EOF
