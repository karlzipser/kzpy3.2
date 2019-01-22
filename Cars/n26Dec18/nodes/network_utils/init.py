#!/usr/bin/env python

from kzpy3.vis3 import *
import torch
import torch.nn
import torch.autograd
import rospy
exec(identify_file_str)

def Torch_Network(weight_file_path):
    
    if True:#try:
        D = {}
        D['heading'] = {}
        D['encoder'] = {}
        D['motor'] = {}
        D['save_data'] = torch.load(weight_file_path)
        print("Torch_Network():: Loading "+weight_file_path)
        from kzpy3.Train_app.nets.SqueezeNet40 import SqueezeNet
        D['solver'] = SqueezeNet().cuda()
        D['solver'].load_state_dict(D['save_data']['net'])
        D['solver'].eval()
        print("Torch_Network():: Loading complete.")

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        cr('Exception!')
        cr(d2s(exc_type,file_name,exc_tb.tb_lineno))

    def _run_model(input,metadata):
        D['output'] = D['solver'](input, torch.autograd.Variable(metadata))       
        return D['output'][0][:].data[0]

    D['run_model'] = _run_model
    
    return D



def prepare_behavioral_metadata():
    """Making metadata tensors in advance so they 
need not be constructed during runtime.
For SqueezeNet40 models."""
    TP = {}
    TP['behavioral_modes_no_heading_pause'] = \
        ['direct','follow','furtive','play','left','right']
    # note, 'center' is not included in
    # TP['behavioral_modes_no_heading_pause']
    # because 'center' is converted to 'direct' below.
    TP['behavioral_modes'] = \
        TP['behavioral_modes_no_heading_pause']+['heading_pause']

    Metadata_tensors = {}
    cm(5)
    for the_behaviorial_mode in TP['behavioral_modes']:

        metadata = torch.from_numpy(zeros((1,128,23,41))).cuda()

        typical_encoder_value = 3.0

        metadata[0,0,:,:] = typical_encoder_value / 100.0 / 5.0

        for x in range(41):
            metadata[0,1,:,x] = (1.0-x/41.0)

        for x in range(41):
            metadata[:,2,:,x] = x/41.0

        for x in range(23):
            metadata[0,3,x,:] = (1.0-x/23.0)

        for x in range(23):
            metadata[0,4,x,:] = x/23.0

        mode_ctr = 1

        for b in TP['behavioral_modes']:
            if b == the_behaviorial_mode:
                metadata[0,-mode_ctr,:,:] = 1.0; mode_ctr += 1
            else:
                metadata[0,-mode_ctr,:,:] = 0.0; mode_ctr += 1

        Metadata_tensors[the_behaviorial_mode] = metadata

    return Metadata_tensors


#EOF
