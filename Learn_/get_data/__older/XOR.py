from kzpy3.vis3 import *
exec(identify_file_str)

NUM_INPUT_CHANNELS = 2
INPUT_WIDTH = 168
INPUT_HEIGHT = 94
NUM_OUTPUTS = 1

def get_data_function(P):

    a = random.choice([0,1])
    b = random.choice([0,1])
    n = 1/10.

    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0

    input_data =  n*rndn(NUM_INPUT_CHANNELS, INPUT_WIDTH,INPUT_HEIGHT)
    input_data[0,:] += a
    input_data[1,:] += b

    target_data =   n*rndn(NUM_OUTPUTS)
    target_data += c
    return {
        'input':input_data,
        'target':target_data,
    }




#EOF
