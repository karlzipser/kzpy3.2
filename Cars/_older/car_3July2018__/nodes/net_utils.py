#!/usr/bin/env python
"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

from kzpy3.utils2 import *
import torch
import torch.nn as nn
from torch.autograd import Variable
from nets.squeezenet import SqueezeNet
import runtime_parameters as rp

verbose = False

#nframes = 2 # default superseded by net



def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def init_model():
    print "def init_model():"
    global solver, scale, nframes
    # Load PyTorch model
    save_data = torch.load(rp.weight_file_path)
    print("Loaded "+rp.weight_file_path)
    # Initializes Solver
    solver = SqueezeNet().cuda()
    solver.load_state_dict(save_data['net'])
    solver.eval()
    nframes = solver.N_FRAMES
    # Create scaling layer
    scale = nn.AvgPool2d(kernel_size=3, stride=2, padding=1).cuda()

init_model()





@static_vars(torch_motor_previous=49, torch_steer_previous=49)
def run_model(input, metadata):
    """
    Runs neural net to get motor and steer data. Scales output to 0 to 100 and applies an IIR filter to smooth the
    performance.

    :param input: Formatted input data from ZED depth camera
    :param metadata: Formatted metadata from user input
    :return: Motor and Steering values
    """
    #print "run_model"
    output = solver(input, Variable(metadata))  # Run the neural net

    if verbose:
        print(output)

    # Get latest prediction
    #torch_motor = 100 * output[0][19].data[0]
    #torch_steer = 100 * output[0][9].data[0]
    torch_motor = 100 * output[0][11].data[0] ########################!!!!!!!!!!!!!!!!!!!!!
    torch_steer = 100 * output[0][2].data[0] ########################!!!!!!!!!!!!!!!!!!!!!
    #torch_motor /= 7.0
    #torch_motor += 49
    #torch_motor = (torch_motor+nonlinear_motor(torch_motor))/2.0

    if verbose:
        print('Torch Prescale Motor: ' + str(torch_motor))
        print('Torch Prescale Steer: ' + str(torch_steer))
    
    # Scale Output
    #torch_motor = int((torch_motor - 49.) * rp.motor_gain + 49. + rp.motor_offset)
    #torch_steer = int((torch_steer - 49.) * rp.steer_gain + 49.)

    # Bound the output
    torch_motor = max(0, torch_motor)
    torch_steer = max(0, torch_steer)
    torch_motor = min(99, torch_motor)
    torch_steer = min(99, torch_steer)

    # Apply an IIR Filter
    if False:
        torch_motor = int((torch_motor + run_model.torch_motor_previous) / 2.0)
        run_model.torch_motor_previous = torch_motor
        torch_steer = int((torch_steer + run_model.torch_steer_previous) / 2.0)
        run_model.torch_steer_previous = torch_steer

    return torch_motor, torch_steer

def format_camera_data(left_list, right_list):
    """
    Formats camera data from raw inputs from camera.

    :param l0: left camera data from time step 0
    :param l1: right camera data from time step 1
    :param r0: right camera dataa from time step 0
    :param r1: right camera data from time step 0
    :return: formatted camera data ready for input into pytorch z2color
    """
    #print "format_camera_data"
    camera_start = time.clock()
    half_img_height = int(shape(left_list[-1])[0]/2)
    listoftensors = []
    for i in range(nframes):
        for side in (left_list, right_list):
            side[-i - 1][:188,:,:] = 128  #*= 0 ####################!!!!!!!!!!!!!!!!!!!!!!!!!
            listoftensors.append(torch.from_numpy(side[-i - 1]))
    camera_data = torch.cat(listoftensors, 2)
   
    camera_data = camera_data.cuda().float()/255. - 0.5
    camera_data = torch.transpose(camera_data, 0, 2)
    camera_data = torch.transpose(camera_data, 1, 2)
    camera_data = camera_data.unsqueeze(0)
    camera_data = scale(Variable(camera_data))
    camera_data = scale(camera_data)

    return camera_data


def format_metadata(raw_metadata):
    """
    Formats meta data from raw inputs from camera.
    :return:
    """
    #print "format_metadata"
    metadata = torch.FloatTensor()
    for mode in raw_metadata:
        metadata = torch.cat((torch.FloatTensor(1, 23, 41).fill_(mode), metadata), 0)
    zero_matrix = torch.FloatTensor(1, 23, 41).zero_()
    for i in range(126):
        metadata = torch.cat((zero_matrix, metadata), 0) 
    return metadata.cuda().unsqueeze(0)
#
########################################################
