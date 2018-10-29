#!/usr/bin/env python

from kzpy3.utils3 import *
import torch
import torch.nn as nn
from torch.autograd import Variable
exec(identify_file_str)
import rospy
from kzpy3.Train_app.nets.SqueezeNet_flex import SqueezeNet

def Flex_Torch_Network(N):
    try:
        D = {}
        D['save_data'] = torch.load(N['flex_weight_file_path'])
        D['solver'] = SqueezeNet().cuda()
        D['solver'].load_state_dict(D['save_data']['net'])
        D['solver'].eval()
        print("Flex_Torch_Network(N):: Loading complete.")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)        
    def _run_model(input,N):
        print 'a'

        D['output'] = D['solver'](input)
        print 2
        torch_motor = 100 * D['output'][0][10+N['flex_network_output_sample']].data[0]
        print 3
        torch_steer = 100 * D['output'][0][N['flex_network_output_sample']].data[0]
        print 4
        torch_motor = max(0, torch_motor)
        print 5
        torch_steer = max(0, torch_steer)
        print 6
        torch_motor = min(99, torch_motor)
        print 7
        torch_steer = min(99, torch_steer)
        print 'b',torch_steer,torch_motor
        return torch_motor, torch_steer

    def _format_flex_data(img):
        flex_data = torch.FloatTensor().cuda()
        list_camera_input = []
        list_camera_input.append(torch.from_numpy(img))
        camera_data = torch.cat(list_camera_input, 2)
        camera_data = camera_data.cuda().float()/4000.0
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        flex_data = torch.cat((torch.unsqueeze(camera_data, 0), flex_data), 0)
        flex_data = Variable(flex_data)
        return flex_data

        """
        listoftensors = []
        for i in range(1):
            for side in (left_list,left_list):
                listoftensors.append(torch.from_numpy(side[-i - 1]))
        flex_data = torch.cat(listoftensors, 2)
        flex_data = flex_data.cuda().float()/4000.0
        #flex_data = torch.transpose(flex_data, 0, 2)
        #flex_data = torch.transpose(flex_data, 1, 2)
        flex_data = flex_data.unsqueeze(0)
        flex_data = D['scale'](Variable(flex_data))
        flex_data = D['scale'](flex_data)
        return flex_data

    
        Fs = fx.get_flex_segs(Fd,flip=False)
        img = fx.make_flex_image(Fs)
        list_camera_input = []
        list_camera_input.append(torch.from_numpy(img))
        camera_data = torch.cat(list_camera_input, 2)
        camera_data = camera_data.cuda().float()/4000.0
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)


    def _format_flex_data(left_list, right_list):
        listoftensors = []
        for i in range(D['nframes']):
            for side in (left_list, right_list):
                listoftensors.append(torch.from_numpy(side[-i - 1]))
        flex_data = torch.cat(listoftensors, 2)
        flex_data = flex_data.cuda().float()/4000.0
        flex_data = torch.transpose(flex_data, 0, 2)
        flex_data = torch.transpose(flex_data, 1, 2)
        flex_data = flex_data.unsqueeze(0)
        flex_data = D['scale'](Variable(flex_data))
        flex_data = D['scale'](flex_data)
        return flex_data
    """



    D['run_model'] = _run_model
    D['format_flex_data'] = _format_flex_data


    return D



