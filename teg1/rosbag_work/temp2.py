"""



"""
import rospy
import rosbag
from kzpy3.vis import *
import cv2
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()

class Bair_Car_Recorded_Data:
    """ """
    def __init__(self, bag_folder_path, num_data_steps, target_topics):
        self.bag_folder_path = bag_folder_path
        self.bag_files = sorted(glob.glob(opj(self.bag_folder_path,'*.bag')))
        file_path = opj(bag_folder_path,'.preprocessed','left_image_bound_to_data')
        print "loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        self.bag_file_num = 0 # not the same as the number in the bag file name
        self.timestamp_num = 0 # refers to timestamp count within a bag file
        self.bag_img_dic = None
        self.timestamps = None
        self.data_dic = None
        self.img = None
        self.num_data_steps = num_data_steps
        self.target_topics = target_topics

    def get_data(self):
        if self.bag_img_dic == None:
            self.bag_img_dic = load_images_from_bag(self.bag_files[self.bag_file_num],'bgr8')
            self.timestamp_num = 0
            self.timestamps = sorted(self.bag_img_dic['left'].keys())
        t = self.timestamps[self.timestamp_num]
        self.data_dic = {}
        if t in self.left_image_bound_to_data:
            #print (self.left_image_bound_to_data[t]['state_one_steps'],self.left_image_bound_to_data[t]['steer'])
            if self.left_image_bound_to_data[t]['state_one_steps'] > self.num_data_steps:
                if self.timestamp_num+self.num_data_steps <= len(self.timestamps):
                    for topic in self.target_topics:
                        target_data = []
                        for tn in range(self.timestamp_num,self.timestamp_num+self.num_data_steps):
                            try:
                                data = self.left_image_bound_to_data[self.timestamps[tn]][topic]
                                target_data.append(data)
                            except:
                                print tn,len(self.timestamps)
                        self.data_dic[topic] = target_data
                    #target_data = [item for sublist in target_data for item in sublist]
                        print self.data_dic[topic]
                self.img = self.bag_img_dic['left'][t]
                delay = 1/30.
            else:
                self.img = self.bag_img_dic['left'][t]
                self.img[:,:,0] = self.img[:,:,1]
                self.img[:,:,2] = self.img[:,:,1]

                delay = 1/30.
            #mi(self.img,'left')
            cv2.imshow('left',self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass
            plt.pause(delay)
        self.timestamp_num += 1
        if self.timestamp_num >= len(self.timestamps):
            self.bag_img_dic = None
            self.bag_file_num += 1
        return self.data_dic




def load_images_from_bag(bag_file_path,color_mode="rgb8"):
    print "loading " + bag_file_path
    bag_img_dic = {}
    bag_img_dic['left'] = {}
    bag_img_dic['right'] = {}
    sides=['left','right']
    bag = rosbag.Bag(bag_file_path)
    for side in sides:
        for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color']):
            t = round(m.timestamp.to_time(),3)
            bag_img_dic[side][t] = bridge.imgmsg_to_cv2(m[1],color_mode)
    return bag_img_dic


"""
bag_folder_path = '/home/karlzipser/Desktop/bair_car_data/direct_7Sept2016_Mr_Orange_Tilden'

d = Bair_Car_Recorded_Data(bag_folder_path,2,2,['steer','motor','encoder','acc','gyro','sonar'])

for i in range(10000):
    d.get_data()
"""
