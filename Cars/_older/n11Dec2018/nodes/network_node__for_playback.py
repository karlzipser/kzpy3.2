#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)

try:
    print_Arguments()
    for r in ['run_folder','dst_folder','graphics']:
        assert r in Arguments

except Exception as e:
    cr("*** Supposed to have command line argument '",r,"'. ***")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    CS_('Exception!',emphasis=True)
    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

os.system(d2s("mkdir -p",Arguments['dst_folder']))
if len(sggo(opj(Arguments['dst_folder'],fname(Arguments['run_folder'])+'.in_progress'))) > 0:
    sys.exit()
if len(sggo(opj(Arguments['dst_folder'],fname(Arguments['run_folder'])+'.net_predictions.pkl'))) > 0:
    sys.exit()

sys_str = d2s("touch",opj(Arguments['dst_folder'],fname(Arguments['run_folder'])+'.in_progress'))
cg(sys_str)
os.system(sys_str)

"""
python kzpy3/Cars/n11Dec2018/nodes/network_node__for_playback.py graphics False dst_folder /home/karlzipser/Desktop/Data/Network_Predictions run_folder '/media/karlzipser/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_15h04m54s' 
"""




import kzpy3.Cars.n11Dec2018.nodes.net_utils as net_utils
#import kzpy3.Cars.n11Oct2018_car_with_nets.nodes.Activity_Module
import kzpy3.Cars.n11Dec2018.nodes.default_values as default_values
N = default_values.P
import torch
N['GPU'] = 1
torch.cuda.set_device(N['GPU'])
torch.cuda.device(N['GPU'])



Color = {}
Color['direct'] = 'k'
Color['left'] = 'b'
Color['right'] = 'r'


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
freqency = Timer(5)

Torch_network = None

loaded_net = False




def dic_of_(list_or_dic,keys):

    D = {}
    for k in keys:
        if list_or_dic == 'lists':
            D[k] = []
        elif list_or_dic == 'dics':
            D[k] = {}
        else:
            cr("***** Error, expected 'lists' or 'dics' as first argument *****")
            assert False
    return D


#####################################################################
#####################################################################
###    

N['weight_file_path'] = most_recent_file_in_folder(opjD('Networks/net_15Sept2018_1Nov_with_reverse_/SqueezeNet40'))
N['weight_file_path'] = opjD('Networks/networks/net_15Sept2018_1Nov_with_reverse___SqueezeNet40/net_22Nov18_13h59m27s.infer')

Torch_network = net_utils.Torch_Network(N)

###
#####################################################################
#####################################################################


if True:

    run_folder = Arguments['run_folder']
    try:
        O.close()
    except:
        pass

    O = h5r(opj(run_folder,'original_timestamp_data.h5py'))

    left = O['left_image']
    right = O['right_image']
    behavioral_modes = ['left','direct','right']
    D = dic_of_('lists',['index','ts']+behavioral_modes)

    D['run_name'] = fname(run_folder)

    for i in range(0,min(len(O['left_image']['vals']),len(O['right_image']['vals']))):

        #cy(i)

        D['index'].append(i)
        D['ts'].append(left['ts'][i])

        if i == 0:
            for behavioral_mode in behavioral_modes:
                D[behavioral_mode].append(None)
            continue

        rLists['left'] = [left['vals'][i-1],left['vals'][i]]
        rLists['right'] = [right['vals'][i-1],right['vals'][i]]

        

        


        camera_data = Torch_network['format_camera_data__no_scale'](rLists['left'],rLists['right'])

        for behavioral_mode in behavioral_modes:

            freqency.freq()

            metadata = Metadata_tensors[behavioral_mode]

            full_output = Torch_network['run_model'](camera_data,metadata,N,return_full_output=True)
            full_output = na(full_output)

            E = {}
            E['full_output'] = full_output
            E['steer'] = (99*full_output[0:10]).astype(int)
            E['motor'] = (99*full_output[10:20]).astype(int)
            E['heading'] = 90.0*full_output[20:30]
            E['encoder'] = 5.0*full_output[30:40]                 

            D[behavioral_mode].append(E)


            if print_timer.check() and Arguments['graphics']:
                #pprint(E)
                
                if behavioral_mode == 'left':
                    figure(1);clf();xylim(0,40,-1,1)
                plot(full_output,Color[behavioral_mode]+'.');spause()
                ####################################################
                ####################################################
                ####################################################
                ##

                if behavioral_mode == 'direct':
                    l0 = rgbcat(rLists,'left',-1)
                    ln1 = rgbcat(rLists,'left',-2)
                    r0 = rgbcat(rLists,'right',-1)
                    rn1 = rgbcat(rLists,'right',-2)
                    l = tcat(l0,ln1)
                    r = tcat(r0,rn1)
                    lr = lrcat(l,r)
                    mci((z2o(lr)*255).astype(np.uint8),scale=1.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')


                ##
                ####################################################
                ####################################################
                ####################################################
                print_timer.reset()



    so(D,opj(Arguments['dst_folder'],D['run_name']+'.net_predictions'))
    os.system(d2s("rm",opj(Arguments['dst_folder'],fname(Arguments['run_folder'])+'.in_progress')))

    O.close()
#EOF

    