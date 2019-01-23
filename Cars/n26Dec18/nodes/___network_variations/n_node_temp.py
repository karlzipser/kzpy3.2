#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import camera
exec(identify_file_str)
import torch
from torch.autograd import Variable

import torch

def show_color_net_inputs(camera_input,pre_metadata_features_metadata=None,channel=0):
    camera_input = camera_input.data.cpu().numpy()
    for i in range(4):
        a = 3*i
        b = 3*(i+1)-1
        c = camera_input[channel,a:b+1,:,:]
        assert shape(c) == (3, 94,168)
        c = c.transpose(1,2,0) 
        assert shape(c) == (94,168,3)
        c = z55(c) # rgb
        mi(c,d2s(a,'to',b))
        spause()
    if pre_metadata_features_metadata != None:
        p = pre_metadata_features_metadata.data.cpu().numpy()
        offset = 128+1+4

        for i in range(4):
            a = 3*(i)+offset
            b = 3*(i+1)-1+offset
            c = p[channel,a:b+1,:,:]
            assert shape(c) == (3, 23,41)
            c = c.transpose(1,2,0) 
            assert shape(c) == (23,41,3)
            c = z55(c) #rgb
            img_lst.append(c)
        display(img_lst,1000,1000,4)
    


def display(img_lst,delay1,delay2,scale=4):
    right_now = img_lst[0]
    left_now  = img_lst[1]
    right_prev= img_lst[2]
    left_prev = img_lst[3]
    img_now = 0*right_now
    img_prev = 0*right_now
    width = shape(img_now)[1]
    img_now[:,:width,:] = right_now
    img_now[:,-width:,:] = left_now
    img_prev[:,:width,:] = right_prev
    img_prev[:,-width:,:] = left_prev
    mci(img_prev,scale=scale,delay=delay1,title='1')
    mci(img_now,scale=scale,delay=delay2,title='1')

def _format_camera_data_quartet(Q):
    listoftensors = []
    listoftensors.append(torch.from_numpy(Q.left_now))
    listoftensors.append(torch.from_numpy(Q.right_now))
    listoftensors.append(torch.from_numpy(Q.left_prev))
    listoftensors.append(torch.from_numpy(Q.right_prev))
    camera_data = torch.cat(listoftensors, 2)
    camera_data = camera_data.cuda().float()/255. - 0.5
    camera_data = torch.transpose(camera_data, 0, 2)
    camera_data = torch.transpose(camera_data, 1, 2)
    camera_data = camera_data.unsqueeze(0)
    camera_data = Variable(camera_data)
    return camera_data

ga = getattr
sa = setattr
if __name__ == '__main__':
    camera.QUIT = False
    rospy.init_node('network_node',anonymous=True,disable_signals=True)
    
    premeta_meta = torch.from_numpy(zeros((1,2*128,23,41))).cuda().float() # note size 256
    premeta_meta = Variable(premeta_meta)
    hz = Timer(30)
    wait = Timer()
    wait2 = Timer(30)
    while not rospy.is_shutdown() and not camera.QUIT:
        if wait.time() > 10:
            if wait2.check():
                cr('wait.time() =',int(wait.time()))
                wait2.reset()
        if True:#try:
            if len(camera.Q_list) > 0:
                if camera.Q_list[-1].ready:
                    camera.Q_list[-1].ready = False

                    camera.Q_list[-1].display(1,1,4)

                    camera_data = _format_camera_data_quartet(camera.Q_list[-1])

                    ctr = 0
                    for t in ['_now_','_prev_']:
                        for cam in ('left','right'):
                            for color in [0,1,2]:
                                img = ga(camera.Q_list[-1],cam+t+'meta')[:,:,color]
                                premeta_meta[0,128+1+4+ctr,:,:] = torch.from_numpy(img).cuda().float()/255. - 0.5
                                ctr += 1
                    show_color_net_inputs(
                        camera_data,
                        pre_metadata_features_metadata=premeta_meta,
                        channel=0)
                    #raw_enter()
                    
                    hz.freq(' (main) ')
                    wait.reset()
                    continue
            time.sleep(1./10000.)
        else:
            pass
        """
        except KeyboardInterrupt:
            camera.QUIT = True
            cr('\n\n*** KeyboardInterrupt ***\n')
            time.sleep(1)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            camera.QUIT = True
            cr('\n\n*** Exception ***\n')
            time.sleep(1)
        """
#EOF

    