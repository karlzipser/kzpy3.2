#!/usr/bin/env python

from kzpy3.utils3 import *
import torch
import torch.nn as nn
from torch.autograd import Variable
import rospy
exec(identify_file_str)



def Torch_Network(N):
    try:
        D = {}
        D['save_data'] = torch.load(N['weight_file_path'])
        print("Torch_Network(N):: Loading "+N['weight_file_path'])
        if 'SqueezeNet40' in N['weight_file_path']:
            cs("Torch_Network(N)::'SqueezeNet40' in N['weight_file_path']")
            from kzpy3.Train_app.nets.SqueezeNet40 import SqueezeNet
        elif 'SqueezeNet20' in N['weight_file_path']:
            from kzpy3.Train_app.nets.SqueezeNet import SqueezeNet
            cs("Torch_Network(N)::'SqueezeNet20' in N['weight_file_path']")
        else:
            cs("Torch_Network(N)::Error, can't identify network type:\n",N['weight_file_path'])
        D['solver'] = SqueezeNet().cuda()
        D['solver'].load_state_dict(D['save_data']['net'])
        D['solver'].eval()
        print("Torch_Network(N):: Loading complete.")
        D['nframes'] = 2#D['solver'].N_FRAMES
        D['scale'] = nn.AvgPool2d(kernel_size=3, stride=2, padding=1).cuda()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)        
    def _run_model(input,metadata,N,return_full_output=False):
        D['output'] = D['solver'](input, Variable(metadata))
        torch_motor = 100 * D['output'][0][10+N['network_output_sample']].data[0]
        torch_steer = 100 * D['output'][0][N['network_output_sample']].data[0]
        torch_motor = max(0, torch_motor)
        torch_steer = max(0, torch_steer)
        torch_motor = min(99, torch_motor)
        torch_steer = min(99, torch_steer)

        if return_full_output:
            full_output = []
            for i in range(40):
                full_output.append(D['output'][0][i].data[0])
            return full_output
        else:
            return torch_motor, torch_steer

    def _format_camera_data(left_list, right_list):
        listoftensors = []
        for i in range(D['nframes']):
            for side in (left_list, right_list):
                if N['GREY_OUT_TOP_OF_IMAGE']:
                    side[-i - 1][:188,:,:] = 128
                if N['USE_LAST_IMAGE_ONLY']:
                    listoftensors.append(torch.from_numpy(side[-1]))
                else:
                    listoftensors.append(torch.from_numpy(side[-i - 1]))
        camera_data = torch.cat(listoftensors, 2)
        camera_data = camera_data.cuda().float()/255. - 0.5
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        camera_data = camera_data.unsqueeze(0)
        camera_data = D['scale'](Variable(camera_data))
        camera_data = D['scale'](camera_data)
        return camera_data




    ##################################################################
    #
    def _format_camera_data__no_scale(left_list, right_list):

        listoftensors = []
        for i in range(D['nframes']):
            for side in (left_list, right_list):
                #print shape(side)
                if N['GREY_OUT_TOP_OF_IMAGE']:
                    side[-i - 1][:188,:,:] = 128
                if N['USE_LAST_IMAGE_ONLY']:
                    listoftensors.append(torch.from_numpy(side[-1]))
                else:
                    listoftensors.append(torch.from_numpy(side[-i - 1]))
        camera_data = torch.cat(listoftensors, 2)
        camera_data = camera_data.cuda().float()/255. - 0.5
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        camera_data = camera_data.unsqueeze(0)
        camera_data = Variable(camera_data)
        return camera_data
    #
    ##################################################################



    def _format_metadata(raw_metadata):
        metadata = torch.FloatTensor()
        ctr = 0
        for mode in raw_metadata:
            metadata = torch.cat((torch.FloatTensor(1, 23, 41).fill_(mode), metadata), 0)
            ctr += 1
        zero_matrix = torch.FloatTensor(1, 23, 41).zero_()
        for i in range(128-ctr):
            metadata = torch.cat((zero_matrix, metadata), 0) 
        return metadata.cuda().unsqueeze(0)

    D['run_model'] = _run_model
    D['format_camera_data'] = _format_camera_data
    D['format_camera_data__no_scale'] = _format_camera_data__no_scale
    D['format_metadata'] = _format_metadata

    return D



