#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy
import rosbag
import cv2

assert 'bag_folders_path' in Arguments
print_Arguments()
A = {}
A['bag_folders_path'] = Arguments['bag_folders_path']
A['use_images'] = True


timer0 = Timer(10)
timer1 = Timer(1)
"""
reflectivity is h_angle
t is r
intensity is intensity
"""

field_names = ['t','reflectivity','intensity']

width = 256
height = 16
width_times_height = width * height

for f in field_names:
    A[f] = zeros((height,width))


Resize = {}
Resize['a'] = (89,167)
Resize['b'] = (0,256)
Resize['c'] = (44,212)

#image_type_versions = ['t','intensity','t']
image_type_versions = ['t']#['intensity']
#resize_versions = ['a','b']
resize_versions = ['c']

Images = {}
for image_type in image_type_versions:
    Images[image_type] = None
######################################
#
Y = {}
mx = 2*np.pi*1000.0
extra = 500
for d in range(0,int(mx+extra)):
    v = int( width*d / (1.0*mx) )
    if v > (width-1):
        v = (width-1)
    Y[d] = v

j = 0
for i in range(sorted(Y.keys())[-1]):
    if i in Y:
        j = Y[i]
    Y[i] = j

Y[np.nan] = 0
#
######################################

img_bigger = zeros((95,168))

def points__from_msg(msg):   

    global img_bigger

    ctr = 0
    ctr3 = 0
    
    ary0 = A[field_names[0]]
    ary1 = A[field_names[1]]
    ary2 = A[field_names[2]]

    for point in pc2.read_points(msg,skip_nans=False,field_names=field_names):

        if ctr >= width:
            if ctr3 >= height-1:
                break
            ctr = 0

        ary0[ctr3,ctr] = point[0]  
        ary1[ctr3,ctr] = point[1]
        ary2[ctr3,ctr] = point[2]

        if ctr3 >= height-1:
            ctr3 = 0
            ctr += 1
        else:
            ctr3 += 1

    y = (A['reflectivity'][8,:]).astype(int)


    for image_type in ['t']:

        Output = {}

        if type(Images[image_type]) == type(None):
            Images[image_type] = A[image_type] * 0

        indicies = [Y[v] for v in y]

        Images[image_type][:,indicies] = A[image_type]

        for i in range(1,len(Images[image_type])):

            if Images[image_type][0,i] == 0:
                try:
                    Images[image_type][:,i] = Images[image_type+'_prev'][:,i]
                except:
                    Images[image_type][:,i] = Images[image_type][:,i-1]

            Images[image_type+'_prev'] = Images[image_type].copy()

            Output['real'] = Images[image_type].copy()

            log_min,log_max = -0.25,1.5
            img = np.log10(Output['real']+0.001)
            img[img>log_max] = log_max
            img[img<log_min] = log_min
            Output['log'] = img

            r = (44,212)
            img = cv2.resize(Output['log'][:,r[0]:r[1]],(168,94))
            img_bigger = img_bigger * 0
            img_bigger[:94,:] = img
            img_bigger[94,0] = log_min
            img_bigger[94,1] = log_max
            img = 255*z2o(img_bigger)[:94,:] # the 255 multiple is to put these images into same range as the rgb images
            assert shape(img) == (94,168)

            Output['resized'] = img

            Output['resized_flipped'] = cv2.flip(Output['resized'],1)

            


        if A['use_images']:
            if timer0.check():
                timer0.reset()
            if timer0.time() < 1:
                mci(
                    Output['resized'].astype(np.uint8),
                    scale=2.0,
                    color_mode=cv2.COLOR_GRAY2BGR,
                    title=image_type
                )

        return Output




def process(bag_folder_path):
    bag_filesv = sorted(glob.glob(opj(bag_folder_path,'*.bag')))
    
    cprint(d2s('Processing',len(bag_filesv),'bag files:'),'red')
    for bv in bag_filesv:
        cprint('\t'+bv,'blue')

    timerv = Timer(0)
    
    the_topics = ['index','log','real','resized','resized_flipped','ts']
    Data = {}
    for k in the_topics:
        Data[k] = []

    started = False
    s = 0.95
    smooth_encoder_value = 0.0
    index = 0

    for bv in bag_filesv:

        timerv.reset()

        cprint(bv,'yellow')

        bagv = rosbag.Bag(bv)



        for m_ in bagv.read_messages(topics=['/bair_car/encoder','/os1_node/points']):

            timestampv = round(m_[2].to_time(),3) # millisecond resolution

            assert(is_number(timestampv))

            if m_[0] == '/bair_car/encoder':
                encoder_value = m_[1].data
                smooth_encoder_value = (1-s)*encoder_value + s*smooth_encoder_value
                #print dp(smooth_encoder_value),not_started
                if started == False:
                    if smooth_encoder_value > 0.75:
                        cr(dp(smooth_encoder_value))
                        #raw_enter()
                        started = True
            

            if m_[0] == '/os1_node/points':

                Output = points__from_msg(m_[1])
                #print type(Output)

                try:
                    if started == True:
                        for k in Output.keys():
                            Data[k].append(Output[k])
                        Data['ts'].append(timestampv)
                        Data['index'].append(index)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

                index += 1


    file_path = opj(Arguments['dst'],fname(bag_folder_path)+".Depth_image.log.resize.flip.h5py")

    cg("\nPutting data into h5py file",file_path)

    H = h5w(file_path)

    for k in the_topics:

        H.create_dataset(k,data=na(Data[k]))

    H.close()


if __name__ == '__main__':

    bag_folders_paths = sggo(A['bag_folders_path'],'*')

    for b in bag_folders_paths:
        already_there = sggo(Arguments['dst'],'*')
        do_continue = False
        for a in already_there:
            if fname(b).split('.')[0] in a:
                do_continue = True
                cr(a,"already there, continuing...")
        if do_continue:
            continue
        if fname(b)[0] == '_':
            continue

        touch_name = opj(Arguments['dst'],fname(b)+'.work_in_progress')
        os.system("touch "+touch_name)
        process(b)
        os.system("rm "+touch_name)

#EOF
