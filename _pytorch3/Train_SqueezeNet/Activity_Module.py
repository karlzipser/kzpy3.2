from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils

#img_saver = Image_to_Folder_Saver({'path':opjD('cameras0')})

_ = dictionary_access


def Net_Activity(*args):
    Args = args_to_dictionary(args)
    D = {}
    True
    D[activiations] = {}
    D[imgs] = {}

    for k in Args[activiations].keys():
        #if k == final_output:
        #    continue
        D[activiations][k] = Args[activiations][k].data.cpu().numpy()
        D[imgs][k] = {}
        for moment_indexv in [0]:#in range(shape(D[activiations][k])[0]):
            #print(k,moment_indexv)
            if k == final_output:
                continue
            if k == camera_input:
                cv = D[activiations][camera_input]
                camera_datav = z2o(cv[moment_indexv,:,:,:]).transpose(1,2,0)
                left_t0v = camera_datav[:,:,0:3]
                right_t0v = camera_datav[:,:,3:6]
                left_t1v = camera_datav[:,:,6:9]
                right_t1v = camera_datav[:,:,9:12]
                camera_arrayv = np.array([right_t0v,left_t0v,right_t1v,left_t1v])
                D[imgs][k][moment_indexv] = vis_square(camera_arrayv,padval=0.5)
            else:
                D[imgs][k][moment_indexv] = vis_square(D[activiations][k][moment_indexv],padval=0.5)

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
        for k in D[imgs].keys():
            if k == final_output:
                continue
                """
                continue
                steerv = D[activiations][final_output][0][:10]
                motorv = D[activiations][final_output][0][10:]
                figure('steer motor');clf();xylim(0,19,0,1)
                plot(range(10),steerv,'ro-')
                plot(range(10,20,1),motorv,'bo-')
                plot([0,19],[0.49,0.49],'k')
                pause(0.000001)
                continue
                """
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
            imgv = D[imgs][k][Args[moment_index]]
            imgv = z2o(imgv)*255
            imgv=imgv.astype(np.uint8)
            imgv = cv2.cvtColor(imgv,color_modev)
            imgv = cv2.resize(imgv, (0,0), fx=scalev, fy=scalev, interpolation=0)
            cv2.imshow(k,imgv)
        cv2.waitKey(delayv)
    D[view] = _function_view
    return D





#EOF
