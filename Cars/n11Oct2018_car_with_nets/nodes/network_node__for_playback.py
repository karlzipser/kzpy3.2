#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)

import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.net_utils as net_utils
import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.Activity_Module
import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.default_values as default_values
N = default_values.P

dts = []

show_timer = Timer(1)


left_list = []
right_list = []
nframes = 2 #figure out how to get this from network




behavioral_mode = 'direct'
drive_mode = 0
direct = 0.0
follow = 0.0
furtive = 0.0
play = 0.0
left = 0.0
right = 0.0
center = 0.0




#############################################################################################
#############################################################################################
##        Making metadata tensors in advance so they need not be constructed during runtime.
##        For SqueezeNet40 models
TP = {}
TP['behavioral_modes_no_heading_pause'] = ['direct','follow','furtive','play','left','right']
# note, 'center' is not included in TP['behavioral_modes_no_heading_pause'] because 'center' is converted to 'direct' below.
TP['behavioral_modes'] = TP['behavioral_modes_no_heading_pause']+['heading_pause']

zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()

Metadata_tensors = {}

for the_behaviorial_mode in TP['behavioral_modes']:

    Metadata_tensors[the_behaviorial_mode] = torch.FloatTensor().cuda()

    mode_ctr = 0

    metadata = torch.FloatTensor().cuda()

    for cur_label in TP['behavioral_modes']:

        if cur_label == the_behaviorial_mode:
                
            metadata = torch.cat((one_matrix, metadata), 1); mode_ctr += 1
        else:
            metadata = torch.cat((zero_matrix, metadata), 1); mode_ctr += 1

    num_metadata_channels = 128
    num_multival_metas = 5

    for i in range(num_metadata_channels - num_multival_metas - mode_ctr):

        metadata = torch.cat((zero_matrix, metadata), 1)

    meta_gradient1 = zero_matrix.clone()
    for x in range(23):
        meta_gradient1[:,:,x,:] = x/23.0
    metadata = torch.cat((meta_gradient1, metadata), 1)

    meta_gradient2 = zero_matrix.clone()
    for x in range(23):
        meta_gradient2[:,:,x,:] = (1.0-x/23.0)
    metadata = torch.cat((meta_gradient2, metadata), 1)

    meta_gradient3 = zero_matrix.clone()
    for x in range(41):
        meta_gradient3[:,:,:,x] = x/41.0
    metadata = torch.cat((meta_gradient3, metadata), 1)

    meta_gradient4 = zero_matrix.clone()
    for x in range(41):
        meta_gradient4[:,:,:,x] = (1.0-x/41.0)
    metadata = torch.cat((meta_gradient4, metadata), 1)
    
    for topic in ['encoder']:
        
        typical_encoder_value = 2.0
        d = typical_encoder_value / 100.0 / 5.0

        meta_gradient5 = zero_matrix.clone() + d
        metadata = torch.cat((meta_gradient5, metadata), 1)
        
    Metadata_tensors[the_behaviorial_mode] = torch.cat((metadata, Metadata_tensors[the_behaviorial_mode]), 0)
##
#############################################################################################
#############################################################################################



##############################################
#
# visualization only
rgb_spacer = zeros((94,2),np.uint8)+128
t_spacer = zeros((4,508),np.uint8)+128
lr_spacer = zeros((200,8),np.uint8)+128
def rgbcat(L,s,t):
    return np.concatenate(( L[s][t][:,:,0],rgb_spacer, L[s][t][:,:,1],rgb_spacer, L[s][t][:,:,2] ),axis=1)
def tcat(t0,tn1):
    return np.concatenate( (t_spacer,t0,t_spacer,tn1,t_spacer), axis=0)
def lrcat(l,r):
    return np.concatenate( (lr_spacer,l,lr_spacer,r,lr_spacer), axis=1)
#
##############################################



net_input_width = 168
net_input_height = 94


rLists = {}
rLists['left'] = []
rLists['right'] = []


print_timer = Timer(5)

Torch_network = None

loaded_net = False







#####################################################################
#####################################################################
###    

N['weight_file_path'] = most_recent_file_in_folder(opjD('net_15Sept2018_1Nov_with_reverse_/SqueezeNet40'))

Torch_network = net_utils.Torch_Network(N)

###
#####################################################################
#####################################################################
    

if False:

    O=h5r('/media/karlzipser/rosbags/tu_15to16Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_12Nov18_20h56m16s/original_timestamp_data.h5py' )        
    i = 10000
    left = O['left_image']['vals']
    right = O['right_image']['vals']
    rLists['left'] = [left[i-1],left[i]]
    rLists['right'] = [right[i-1],right[i]]

    """
    ####################################################
    ####################################################
    ####################################################
    ##

    for side in ['left','right']:
        for i in [-1]:#,-2]:
            advance(rLists[side], cv2.resize(Lists[side][i],(net_input_width,net_input_height)), 4 )

    if N['show_net_input']:# in Arguments:                   
        if True:#'show_net_input' in ppc.A:
            if True:#ppc.A['show_net_input']:
                if even:
                    l0 = rgbcat(rLists,'left',-1)
                    ln1 = rgbcat(rLists,'left',-2)
                    r0 = rgbcat(rLists,'right',-1)
                    rn1 = rgbcat(rLists,'right',-2)
                    l = tcat(l0,ln1)
                    r = tcat(r0,rn1)
                    lr = lrcat(l,r)
                    mci((z2o(lr)*255).astype(np.uint8),scale=1.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')
                    even = False
                else:
                    even = True

    ##
    ####################################################
    ####################################################
    ####################################################
    """


    camera_data = Torch_network['format_camera_data__no_scale'](rLists['left'],rLists['right'])

    metadata = Metadata_tensors[behavioral_mode]

    full_output = Torch_network['run_model'](camera_data, metadata, N, True)





#EOF

    