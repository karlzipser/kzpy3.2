from kzpy3.vis import *
import rospy
import rosbag
import cv2
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()


def preview(bag_folder_path,dst_folder=opjD('previews')):

    dst_folder_bag_folder = opj(dst_folder,fname(bag_folder_path))
    unix('mkdir -p '+dst_folder_bag_folder)
    time.sleep(0.1)
    bag_files = sorted(glob.glob(opj(bag_folder_path,'*.bag')))



    for bag_file_path in bag_files:

        bag = rosbag.Bag(bag_file_path)
        side = 'left'

        color_mode="rgb8"

        t0 = time.time()
        ctr = 0
        for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color']): #rospy.rostime.Time(1481244304734196051)):
            t = m.timestamp
            if ctr == 0:
                img1= bridge.imgmsg_to_cv2(m[1],color_mode)
                break
            ctr += 1
        """
        t_sec = rospy.rostime.Time.to_sec(m.timestamp)
        ST = rospy.rostime.Time.from_sec(t_sec-1/15.)
        img2 = 0*img1

        for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color'], start_time=ST): #rospy.rostime.Time(1481244304734196051)):
            print('here')
            t = m.timestamp
            print t
            img2 = bridge.imgmsg_to_cv2(m[1],color_mode)

        print time.time()-t0
        sp = shape(img1)
        img3 = zeros((sp[0],2*sp[1],3),np.uint8)
        img3[:,:sp[1],:] = img1
        img3[:,sp[1]:,:] = img2
        """
        dst_png = opj(dst_folder_bag_folder,fname(bag_file_path))
        dst_png = dst_png.replace('.bag','.png')
        print(dst_png)
        imsave(dst_png,img1)
