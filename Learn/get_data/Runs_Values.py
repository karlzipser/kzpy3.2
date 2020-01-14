from kzpy3.vis3 import *
exec(identify_file_str)





__started__ = False
def get_data_function(P):
    
    global __started__

    if not __started__:
        __started__ = True
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

    n = np.random.choice([2,3,4,5,6,7,8])
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






#EOF
