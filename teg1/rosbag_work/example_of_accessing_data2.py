from kzpy3.vis import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files4 import *
import cv2
path = '/media/your_computer/rosbags/bair_car_data'
path = '/home/karlzipser/Desktop/Old_Desktop/bair_car_rescue/bair_car_data'
#path = opjD('temp_bags_saved')
path = '/home/karlzipser/Desktop/bair_car_data_6_min'
path = opjD('bair_car_data_min')
path = sys.argv[1]
num_bag_files_to_sample_from_given_run = 1
num_samples_from_given_bag_file = 1

num_frames = 32

topics = ['state','encoder','steer','motor','gyro','acc','left_right'] # images not included in this list

data_object = Bair_Car_Data(path, num_bag_files_to_sample_from_given_run, num_samples_from_given_bag_file, validation_set_flag=False)
plt.ion()

def apply_rect_to_img(img,value,min_val,max_val,pos_color,neg_color,rel_bar_height,rel_bar_thickness,center=False,reverse=False):
    h,w,d = shape(img)
    p = (value - min_val) / (max_val - 1.0*min_val)
    if reverse:
        p = 1.0 - p
    if p > 1:
        p = 1
    if p < 0:
        p = 0
    wp = int(p*w)
    bh = int((1-rel_bar_height) * h)
    bt = int(rel_bar_thickness * h)
    
    if center:
        if wp < w/2:
            img[(bh-bt/2):(bh+bt/2),(wp):(w/2),:] = neg_color
        else:
            img[(bh-bt/2):(bh+bt/2),(w/2):(wp),:] = pos_color
    else:
        img[(bh-bt/2):(bh+bt/2),0:wp,:] = pos_color

img = np.zeros((94, 168,3),np.uint8)

for i in range(10000):

    a_data_sequence = data_object.get_data(topics, num_frames, num_frames)
    """
        plt.figure('acc')
        plt.clf()
        plt.figure('acc')

        if not "NO DATA" == a_data_sequence['acc'][0]:
            plt.plot(a_data_sequence['acc'])
        plt.plot(a_data_sequence['state'])
        plt.plot(a_data_sequence['gyro'])
        plt.plot(a_data_sequence['motor'])
        plt.plot(np.array(a_data_sequence['steer']))
        plt.pause(0.00001)
    """
    for j in range(num_frames):
        im = a_data_sequence['left'][j]
        img[:,:,0] = im
        img[:,:,1] = im
        img[:,:,2] = im
        apply_rect_to_img(img,a_data_sequence['steer'][j],0,99,[255.0,0,0],[0,255,0.0],0.9,0.1,center=True,reverse=True)
        img4 = imresize(img,4.0)
        #apply_rect_to_img(img,a_data_sequence['acc'][j][1]-9.8,-20,20,[255.0,0,0],[0,255,0.0],0.8,0.1,center=True,reverse=False)
        #mi(img,'left',img_title=str(j))
        #plt.pause(0.00001)
        cv2.imshow('left',img4.astype('uint8'))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        time.sleep(0.0003)
