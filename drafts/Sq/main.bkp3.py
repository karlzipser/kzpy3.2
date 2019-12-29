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

    input_data =    zeros((P['NUM_IN_BATCH'], P['NUM_INPUT_CHANNELS'], P['INPUT_WIDTH'],P['INPUT_HEIGHT']))
    input_data[:,0,:] += 1 * a #+0.1
    input_data[:,1,:] += 1 * b #+0.1

    meta_data = None
    target_data =   zeros((P['NUM_IN_BATCH'], P['NUM_OUTPUTS']))
    target_data += 1 * c

    return input_data,meta_data,target_data




N = network.SqueezeNet(
    P['NUM_INPUT_CHANNELS'],
    P['NUM_OUTPUTS'],
    P['NUM_METADATA_CHANNELS'],
    )


losses = []

for i in range(20000):

    input_data,meta_data,target_data = make_inputs_and_outputs()

    N.forward(input_data,meta_data,target_data)
    N.backward()
    l = N.extract('loss',None)
    losses.append( N.extract('loss',None) )

    if mod(i,100):
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
