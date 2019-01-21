#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import torch
import torch.autograd
import cv_bridge
from sensor_msgs.msg import Image
import cv2
exec(identify_file_str)

full_width,full_height = 168,94
meta_width,meta_height = 41,23


CS_state = {}
CS_state['bridge'] = cv_bridge.CvBridge()
def Camera_Shot(data):
    D = {}
    img = CS_state['bridge'].imgmsg_to_cv2(data,'rgb8')
    if shape(img)[0] > 94:
        img = cv2.resize(img,(full_width,full_height))
    D['img'] = img
    D['ts'] = data.header.stamp.secs + data.header.stamp.nsecs / 10.0**9
    D['seq'] = data.header.seq
    return D

timer=Timer()

def Quartet(name='no_name'):
    D = {}
    D['name'] = name
    for side in ['left','right']:
        D[side] = {}
        for when in ['now','prev']:
            D[side][when] = {}
            for size_ in ['full','small']:
                D[side][when][size_] = None

    D['ready'] = True

    def _function_display(delay0,delay1,delay2,size_='full',scale=4):
        shape_ = np.shape(D['left']['now'][size_])
        print shape_
        width,height = shape_[1],shape_[0]
        img_now = np.zeros((height,2*width+int(width/16),3),np.uint8) + 127
        img_prev = img_now.copy()
        img_blank = img_now.copy()
        img_now[:,:width,:] =   D['right']['now'][size_]
        img_now[:,-width:,:] =  D['left']['now'][size_]
        img_prev[:,:width,:] =  D['right']['prev'][size_]
        img_prev[:,-width:,:] = D['left']['prev'][size_]
        img_blank[:,:width,:] =  0*D['right']['prev'][size_]
        img_blank[:,-width:,:] = 0*D['left']['prev'][size_]
        print timer.time();timer.reset()
        if delay0 > 0:
            mci(img_blank,scale=scale,delay=delay0,title='Quartet '+D['name'])
        print timer.time();timer.reset()
        mci(img_prev,scale=scale,delay=delay1,title='Quartet '+D['name'])
        print timer.time();timer.reset()
        if delay2 > 0:
            mci(img_now,scale=scale,delay=delay2,title='Quartet '+D['name'])
        print timer.time();timer.reset()

    def _function_to_torch(size_='full'):
        listoftensors = []
        for when in ['now','prev']:
            for side in (['left','right']):
                listoftensors.append(torch.from_numpy(D[side][when][size_]))
        camera_data = torch.cat(listoftensors, 2)
        camera_data = camera_data.cuda().float()/255. - 0.5
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        camera_data = camera_data.unsqueeze(0)
        camera_data = torch.autograd.Variable(camera_data)
        return camera_data

    def _function_from_torch(net_cuda,channel=0,offset=0):
        net_data = net_cuda.data.cpu().numpy()
        q = (('left','now'),('right','now'),('left','prev'),('right','prev'))
        for i in range(4):
            a = 3*i
            b = 3*(i+1)-1
            c = net_data[channel,offset+a:offset+b+1,:,:]
            assert shape(c) == (3,full_height,full_width) or shape(c) == (3,meta_height,meta_width)
            c = c.transpose(1,2,0) 
            assert shape(c) == (full_height,full_width,3) or shape(c) == (meta_height,meta_width,3)
            c = z55(c) # now in rgb
            if shape(c)[0] > 30:
                size_ = 'full'
            else:
                size_ = 'small'
            side = q[i][0]
            when = q[i][1]
            D[side][when][size_] = c

    D['display'] = _function_display
    D['to_torch'] = _function_to_torch
    D['from_torch'] = _function_from_torch

    return D



def ZED():
    D={}
    D['full_shape'] = (full_height,full_width)
    D['small_shape'] = (meta_height,meta_width)
    D['left_list'] = []
    D['right_list'] = []
    D['left_ready'] = False
    D['stats'] = {}
    D['stats']['call'] = 0
    D['stats']['success'] = 0
    D['stats']['fail a'] = 0
    D['stats']['fail b'] = 0
    D['stats']['fail c'] = 0

    def _function_limit_list_lengths(max_len,min_len):
        for list_side in ['left_list','right_list']:
            if len(D[list_side]) > max_len:
                D[list_side] = D[list_side][-min_len:]


    def _function_build_quartet(label_frames=True):
        D['stats']['call'] += 1
        if True:#try:

            for i in [-1,-2,-3]:

                dt_now = D['left_list'][i]['ts'] - D['right_list'][-1]['ts']
                if dt_now > -0.01 and dt_now < 0.02:
                    break
            else:
                D['stats']['fail c']+=1
                return None

            dt_left = D['left_list'][i]['ts'] - D['left_list'][i-1]['ts']
            dt_right = D['right_list'][-1]['ts'] - D['right_list'][-2]['ts']
            
            if dt_left > 0.025 and dt_left < 0.04:
                if dt_right > 0.025 and dt_right < 0.04:

                    Q = Quartet(name='from ROS')

                    Q['left']['now']['full'] = D['left_list'][i]['img'].copy() # temp?
                    Q['right']['now']['full'] = D['right_list'][-1]['img'].copy()
                    Q['left']['prev']['full'] = D['left_list'][i-1]['img'].copy()
                    Q['right']['prev']['full'] = D['right_list'][-2]['img'].copy()

                    if label_frames:
                        for side in ['left','right']:
                            for when in ['now','prev']:
                                color = (0,255,0)
                                if when == 'now':
                                    color = (255,0,0)
                                cv2.putText(
                                    Q[side][when]['full'],
                                    d2s(side,when),
                                    (10,20),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1.0,color,2)


                    Q['left']['now']['small'] = \
                        cv2.resize(Q['left']['now']['full'],(meta_width,meta_height))
                    Q['right']['now']['small'] = \
                        cv2.resize(Q['right']['now']['full'],(meta_width,meta_height))
                    Q['left']['prev']['small'] = \
                        cv2.resize(Q['left']['prev']['full'],(meta_width,meta_height))
                    Q['right']['prev']['small'] = \
                        cv2.resize(Q['right']['prev']['full'],(meta_width,meta_height))
                    D['stats']['success']+=1

                    return Q
                else:
                    D['stats']['fail a']+=1
                    return None
            else:
                D['stats']['fail b']+=1
                return None

        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            return None

    D['limit_list_lengths'] = _function_limit_list_lengths
    D['build_quartet'] = _function_build_quartet

    return D


Zed = ZED()


def left_callback(data):
    Zed['left_list'].append(Camera_Shot(data))
    Zed['limit_list_lengths'](6,4)
    Zed['left_ready'] = True


def right_callback(data):
    Zed['right_list'].append(Camera_Shot(data))



bcs = '/bair_car'

rospy.Subscriber(
    bcs+"/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber(
    bcs+"/zed/left/image_rect_color",Image,left_callback,queue_size = 1)



QUIT = False

def maintain_quartet_list(Q_list):

    hz = Timer(60)
    print_timer = Tr(60)
    timer = Timer()
    
    while True:
        if rospy.is_shutdown():
            break
        if QUIT == True:
            break
        try:
            if len(Zed['left_list']) > 3 and Zed['left_ready']:

                Zed['left_ready'] = False
                Q = Zed['build_quartet']()
                if Q != None:
                    Q_list.append(Q)
                while len(Q_list) > 3:
                    Q_list.pop(0)
                hz.freq()
                print_timer.message(
                    d2s(
                        dp(timer.time()),
                        dp(100*Zed['stats']['success']/(1.0*Zed['stats']['call'])),'%'))
            else:
                time.sleep(1/10000.)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

    cg('\nExiting maintain_quartet_list thread.\n')


Q_list = []

threading.Thread(target=maintain_quartet_list,args=[Q_list]).start()




if __name__ == '__main__':

    rospy.init_node('camera',anonymous=True,disable_signals=True)

    metadata = torch.from_numpy(zeros((1,256,23,41)))
    metadata = metadata.cuda().float()
    metadata = torch.autograd.Variable(metadata)

    camera_data = torch.from_numpy(zeros((1,12,23,41)))
    camera_data = camera_data.cuda().float()
    camera_data = torch.autograd.Variable(camera_data)

    hz = Timer(30)
    wait = Timer()
    wait2 = Timer(30)
    size_ = 'full'

    while True:

        if rospy.is_shutdown():
            break

        if QUIT == True:
            break

        if wait.time() > 10:
            if wait2.check():
                cr('wait.time() =',int(wait.time()))
                wait2.reset()
        if True:#try:
            if len(Q_list) > 0:
                Q = Q_list[-1]
                if Q['ready']:
                    Q['ready'] = False
                    #Q['display'](1000,1000,1000,size_,4)
                    hz.freq(' (main) ')
                    wait.reset()
                    camera_data = Q['to_torch'](size_=size_)
                    U = Quartet(name='from torch '+size_)
                    if size_ == 'small':
                        metadata[0,128+1+4:128+1+4+12,:,:] = camera_data
                        offset = 128+1+4   
                        U['from_torch'](metadata,offset=offset)
                    else:
                        offset = 0   
                        U['from_torch'](camera_data,offset=offset)

                    U['display'](1000,1000,1000,size_,4)
                    continue
            time.sleep(1./100000.)
        """
        except KeyboardInterrupt:
            QUIT = True
            cr('\n\n*** KeyboardInterrupt ***\n')
            time.sleep(1)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            #QUIT = True
            #cr('\n\n*** Exception ***\n')
            #time.sleep(1)
        """
        
        

#EOF