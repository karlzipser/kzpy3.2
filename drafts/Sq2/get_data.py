from kzpy3.vis3 import *
exec(identify_file_str)



def make_XOR_input_target(P):
    a = random.choice([0,1])
    b = random.choice([0,1])

    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0

    input_data =    0.5*rndn(P['NUM_INPUT_CHANNELS'], P['INPUT_WIDTH'],P['INPUT_HEIGHT'])
    input_data[0,:] += a
    input_data[1,:] += b

    meta_data = None
    target_data =   0.5*rndn(P['NUM_OUTPUTS'])
    target_data += c

    return input_data,meta_data,target_data



#EOF
