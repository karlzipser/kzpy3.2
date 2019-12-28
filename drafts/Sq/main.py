from kzpy3.vis3 import *
import kzpy3.drafts.Sq.network as network    
import Menu.main
exec(identify_file_str)

########################################
########################################
###
M = Menu.main.start_Dic(
    dic_project_path=pname(opjh(__file__)), 
    Arguments={
        'menu':False,
        'read_only':True,
    }
)
M['load']()
P = M['Q']['network_parameters']
#kprint(M['Q'])
#kprint(P)
###
########################################
########################################

def make_inputs_and_outputs():
    a = random.choice([0,1])
    b = random.choice([0,1])
    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0
    #cy(a,b,c,ra=1)
    input_data =    zeros((P['NUM_IN_BATCH'], P['NUM_INPUT_CHANNELS'], P['INPUT_WIDTH'],P['INPUT_HEIGHT']))
    input_data[:,0,:] += 1 * a 
    input_data[:,1,:] += 1 * b

    meta_data = None
    target_data =   zeros((P['NUM_IN_BATCH'], P['NUM_OUTPUTS']))
    target_data += 1 * c

    return input_data,meta_data,target_data


N = network.SqueezeNet(
    P['NUM_INPUT_CHANNELS'],
    P['NUM_OUTPUTS'],
    P['NUM_METADATA_CHANNELS'],
    )

import torch.nn.utils as nnutils

losses = []
for i in range(200):
    print i

    input_data,meta_data,target_data = make_inputs_and_outputs()

    N.optimizer.zero_grad()
    N.forward(input_data,meta_data,target_data)
    #N.loss = N.criterion(N.A['final_output'],target_torch)
    N.loss.backward()
    nnutils.clip_grad_norm(N.parameters(), 1.0)
    l = N.extract('loss',None)
    if l < 1:
        losses.append( N.extract('loss',None) )
    N.optimizer.step()
    print losses[-1]
    #N.backward()

plot(losses,'.')
spause()
raw_enter()
#EOF
