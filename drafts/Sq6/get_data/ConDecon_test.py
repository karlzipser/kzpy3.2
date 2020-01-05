from kzpy3.vis3 import *
exec(identify_file_str)


def get_data_function(P):
    NUM_INPUT_CHANNELS = 3
    INPUT_WIDTH = 41#168
    INPUT_HEIGHT = 23#94
    #NUM_OUTPUTS = 3
    a = random.choice([0,1])
    b = random.choice([0,1])
    n = 0.3

    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0

    input_data =  n*rndn(NUM_INPUT_CHANNELS, INPUT_WIDTH,INPUT_HEIGHT)
    input_data[0,:] += a
    input_data[1,:] += b

    target_data =  0 * input_data
    target_data += c
    return {
        'input':input_data,
        'target':target_data,
    }




#EOF
