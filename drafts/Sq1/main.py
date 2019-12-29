from kzpy3.vis3 import *
import kzpy3.drafts.Sq.network as network    
import Menu.main
from input_target import make_XOR_input_target
exec(identify_file_str)

########################################
########################################
###
M = Menu.main.start_Dic(
    dic_project_path=pname(opjh(__file__)), 
    Arguments={'menu':False,'read_only':True}
)
M['load']()
P = M['Q']['network_parameters']
###
########################################
########################################


def make_batch(input_target_function):
    input_batch = []
    meta_batch = []
    target_batch = []
    for i in range(P['NUM_IN_BATCH']):
        input_data,meta_data,target_data = input_target_function()
        input_batch.append(input_data)
        target_batch.append(target_data)
    return na(input_batch),None,na(target_batch)


N = network.SqueezeNet(
    P['NUM_INPUT_CHANNELS'],
    P['NUM_OUTPUTS'],
    P['NUM_METADATA_CHANNELS'],
    )


losses = []

for i in range(20000):

    input_data,meta_data,target_data = make_batch(make_XOR_input_target)

    N.forward(input_data,meta_data,target_data)

    N.backward()

    losses.append( N.extract('loss',None) )

    if mod(i,1000):
        figure('loss')
        ab = N.extract('camera_input',0)
        a = ab[0,0,0]
        b = ab[1,0,0]
        c = N.extract('final_output',0)[0]
        print dp(a),dp(b),dp(c)

        clf()
        plot(losses,'.')
        m = meo(na(losses),100)
        if len(m) > 30:
            lm = na(m[-30:]).mean()
        else:
            lm = 1.
        plot(m)
        ylim(0,lm*10.)
        spause()

raw_enter()

#EOF
