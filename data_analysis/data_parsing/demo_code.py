'''
Created on May 14, 2017

@author: Sascha Hornauer
'''
import cv2
from cv_bridge import CvBridge

from kzpy3.data_analysis.data_parsing.Bagfile_Handler import Bagfile_Handler


        


if __name__ == "__main__":
    my_bagfile = Bagfile_Handler('/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-33-12_20.bag', 
                                 ['/bair_car/zed/left/image_rect_color', '/bair_car/zed/right/image_rect_color'])
    
    bridge = CvBridge()
    
    topic, msg, timestamp = my_bagfile.get_bag_content()
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    
    cv2.imshow(topic,cv_image)
    
    topic2, msg2, timestamp2 = my_bagfile.get_bag_content()
    cv_image2 = bridge.imgmsg_to_cv2(msg, "bgr8")
    
    cv2.imshow(topic2,cv_image2)
    cv2.moveWindow(topic2,600,0)
    cv2.waitKey(0)
    
    
    cv2.destroyAllWindows()