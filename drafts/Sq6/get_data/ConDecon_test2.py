from kzpy3.vis3 import *
exec(identify_file_str)

r = 'Mr_Black_27Jul18_18h46m35s' #.net_projections.h5py'
p = opjD('temp_data')
O = h5r(opj(p,r,'original_timestamp_data.h5py'))
J = h5r(opj(p,d2p(r,'net_projections.h5py')))
ctr = 0
length = len(O['left_image']['vals'])
assert len(J['normal']) == length

def get_data_function(P):
    ctr = rndint(length)
    input_data =  J['normal'][ctr].transpose(2,1,0)
    target_data =  O['left_image']['vals'][ctr]
    target_data = cv2.resize(target_data ,(41,23)).transpose(2,1,0)

    input_data = 1/255.0*input_data
    input_data = input_data - 0.5
    target_data = 1/255.0*target_data
    #target_data = target_data - 0.5
    #print target_data.min().min(),target_data.max().max()
    #ctr += 1
    #if ctr >= length:
    #    ctr = 0

    return {
        'input':input_data,
        'target':target_data,
    }




#EOF
