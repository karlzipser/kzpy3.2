from kzpy3.vis3 import *
exec(identify_file_str)


Values=loD('Values')
Runs=loD('Runs')
Os = {}
for r in Runs.keys():
    p = opjD('Data',Runs[r],r,'original_timestamp_data.h5py')
    Os[r] = h5r(p)
Keys = {}
for n in Values.keys():
    Keys[n] = Values[n].keys()
    np.random.shuffle(Keys[n])



def make_Runs_Values_input_target(P):
    n = np.random.choice(Values.keys())
    ky = Keys[n][randint(len(Keys[n]))]
    f0 = ky[0][0]
    f1 = ky[1][0]
    i0 = ky[0][1]
    i1 = ky[1][1]
    img0 = Os[f0]['left_image']['vals'][i0]
    img1 = Os[f1]['left_image']['vals'][i1]
    d = Values[n][ky]
    #mi(img0,0);mi(img1,1,img_title=d2s(d));spause()
    #return na([img0, img1]), None, na([d])
    input_data = np.concatenate((img0,img1),2).transpose(2,1,0)
    #kprint(shape(input_data),title='input_data')
    return input_data, None, na([d])




def make_XOR_input_target(P):
    a = random.choice([0,1])
    b = random.choice([0,1])

    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0

    input_data =    0.1*rndn(P['NUM_INPUT_CHANNELS'], P['INPUT_WIDTH'],P['INPUT_HEIGHT'])
    input_data[0,:] += a
    input_data[1,:] += b

    meta_data = None
    target_data =   0.1*rndn(P['NUM_OUTPUTS'])
    target_data += c
    kprint(shape(input_data),title='input_data')
    return input_data,meta_data,target_data



#EOF
