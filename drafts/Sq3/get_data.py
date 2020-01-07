from kzpy3.vis3 import *
exec(identify_file_str)


Values=loD('Values')
Runs=loD('Runs')
Os = {}
Os_flip = {}
for r in Runs.keys():
    p = opjD('Data',Runs[r],r,'original_timestamp_data.h5py')
    Os[r] = h5r(p)
    q = opjD('Data',Runs[r],r,'flip_images.h5py')
    Os_flip[r] = h5r(q)
Keys = {}
for n in Values.keys():
    Keys[n] = Values[n].keys()
    np.random.shuffle(Keys[n])

categories = [2,3,4,5,6,7,8]
"""
for n in Keys.keys():
    if n < 1:
        continue
    if n > 9:
        continue
    l = len(Keys[n])
    print n,l
    if l > 1000:
        categories.append(n)
"""
kprint(categories,title('categories'))

def make_Runs_Values_input_target(P):
    #n = np.random.choice(Values.keys())
    n = np.random.choice(categories)#[2,3,4,5,6,7,8])
    ky = Keys[n][randint(len(Keys[n]))]
    f0 = ky[0][0]
    f1 = ky[1][0]
    i0 = ky[0][1]
    i1 = ky[1][1]
    if rndchoice([0,1]):
        B = Os
        ik = 'left_image'
    else:
        B = Os_flip
        ik = 'left_image_flip'
    img0 = B[f0][ik]['vals'][i0]
    img1 = B[f1][ik]['vals'][i1]
    d = Values[n][ky]
    input_data = np.concatenate((img0,img1),2).transpose(2,1,0)
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
