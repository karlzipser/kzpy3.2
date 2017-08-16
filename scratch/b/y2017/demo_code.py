'''
Created on May 14, 2017

@author: Sascha Hornauer
'''
import cv2
from cv_bridge import CvBridge

from kzpy3.data_analysis.data_parsing.Bagfile_Handler import *


        


if __name__ == "__main__":
    my_bagfile = Bagfile_Handler('/media/karlzipser/ExtraDrive4/Mr_Silver_28April2017/processed/direct_rewrite_test_28Apr17_19h12m51s_Mr_Silver/bair_car_2017-04-28-19-15-30_5.bag' , 
                                 ['/bair_car/zed/left/image_rect_color', '/bair_car/zed/right/image_rect_color','/bair_car/gyro'])
    

    bridge = CvBridge()
    while True:
        #
        #print msg.data
        topic, msg, timestamp = my_bagfile.get_bag_content()
        print type(msg)
        #cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        #cv2.imshow(topic,cv_image)
        
        topic2, msg2, timestamp2 = my_bagfile.get_bag_content()
        print type(msg2)
        #cv_image2 = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        #cv2.imshow(topic2,cv_image2)
        #cv2.moveWindow(topic2,600,0)
        #k = cv2.waitKey(33)
        if k == ord('q'):
            break
        topic0, msg0, timestamp = my_bagfile.get_bag_content()
        print msg0
    cv2.destroyAllWindows()

    # 