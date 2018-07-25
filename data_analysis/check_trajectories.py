'''
Created on May 15, 2017

@author: Sascha Hornauer
'''
from data_parsing.Trajectory_From_Pkl import *
import os
import cPickle as pickle
from aruco_tools.mode import behavior
from kzpy3.vis import apply_rect_to_img
import sys
import rospy
from operator import add
import numpy as np
import cv2
import matplotlib.pyplot as plt
from kzpy3.data_analysis.data_parsing.Bagfile_Handler import Bagfile_Handler

def animate(resulting_trajectories):
    
    
    #bagfile_name = '/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-28-10_10.bag'
    #bagfile_name = '/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-28-38_11.bag'
    #bagfile_name = '/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-29-10_12.bag'
    
    #bagfile_name = '/media/karlzipser/ExtraDrive1/Mr_Black_28April2017/processed/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-28-19_10.bag'
    #'/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-28-19_10.bag'
    #bagfile_name = '/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-28-49_11.bag'
    #bagfile_name = '/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-29-18_12.bag'
    #bagfile_name = '/home/picard/2ndDisk/carData/rosbags/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-29-49_13.bag'
    
    bagfile_name = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-23-52_1.bag'

    bagfile_handler = Bagfile_Handler(bagfile_name)
    paused_video = False
    
    bar_color = [0, 0, 255]
    if not paused_video:
        cv_image, bagfile_timestamp = bagfile_handler.get_image()
        
    for cars, modes in resulting_trajectories:
                 
        blue_circle = resulting_trajectories[('Mr_Blue', modes)]
        
        if (modes == behavior.follow):
            for i in range(0, len(blue_circle)):
                trajectory_data = blue_circle[i]
        else:
            trajectory_data = blue_circle
        
        traj_per_timestamp = zip(trajectory_data['timestamps'], trajectory_data['trajectories'], trajectory_data['motor_cmds'], trajectory_data['pos'],trajectory_data['path'])
       
        for i in range(0, len(traj_per_timestamp)):
              
            if True:  # try:        
                # we ignore synchronization for a second
                
                timestamp = traj_per_timestamp[i][0]
                trajectory = traj_per_timestamp[i][1]
                motor_cmd = traj_per_timestamp[i][2]
                pos = traj_per_timestamp[i][3]
                path = traj_per_timestamp[i][4]
                
                try:
                    if timestamp + 0.05 < bagfile_timestamp.to_sec() +1.3:
                        #print "OUT OF SYNC " + str(timestamp -  bagfile_timestamp.to_sec())
                        
                        continue
                    
                    if timestamp - 0.05 > bagfile_timestamp.to_sec() +1.3:
                        cv_image, bagfile_timestamp = bagfile_handler.get_image()
                        #print "OUT OF SYNC " + str(timestamp -  bagfile_timestamp.to_sec())
                        
                        continue
                except AttributeError:
                    print "End of Bagfile"
                #print trajectory
                steer = 49.0 + np.sum(np.diff(trajectory[0:10]))
                motor = np.average(motor_cmd)
                #print motor
                
                cv_image, timestamp = bagfile_handler.get_image()
                
                if not cv_image == None:
                     
                    apply_rect_to_img(cv_image, steer, 0, 99, bar_color, bar_color, 0.9, 0.1, center=True, reverse=True, horizontal=True)
                
                    apply_rect_to_img(cv_image, motor, 0, 99, bar_color, bar_color, 0.9, 0.1, center=True, reverse=True, horizontal=False)
                    
                    height = 367
                    width = height  # 672
                    radius_arena = 4.28
                    pos_x= map(add,path[0],[8.0]*len(path[0]))
                    pos_y= map(add,path[1],[8.0]*len(path[1]))
                    
                    pos_x = map(add,pos_x,[height/2.]*np.ones(len(pos_x)))
                    pos_y = pos_y * -1
                    
                    polypath = np.array(zip(pos_x,pos_y))*30.0
                    #print polypath
                    pts = np.array(polypath, np.int32)
                    pts = pts.reshape((-1,1,2))
                    
                    cv2.polylines(cv_image,[pts],False,(0,255,255),thickness=5)
                    posx = int((pos[0] * width / (2.*radius_arena)) + 672 / 2.)
                    posy = int(-(pos[1] * height / (2.*radius_arena)) + height / 2.)
                    cv2.circle(cv_image, (posx, posy), 10, (0, 0, 255), -1)
                    cv2.circle(cv_image, (672 / 2, height / 2), int(height / 2.0), (255, 0, 0), 3)
                    

                if cv_image == None:
                    continue
                cv2.imshow('frame', cv_image)
                key = cv2.waitKey(1000 / 30) & 0xFF
                if key == ord('q'):
                    break
                if key == ord(' '):
                    paused_video = not paused_video
                if key == ord('w'):
                    bagfile_handler.fast_forward()

        


if __name__ == '__main__':    
    
    home = os.path.expanduser("~")
    #pickle_path = home + '/kzpy3/teg9/trajectories.pkl'
    #pickle_path = home + '/2ndDisk/N.pkl'
    pickle_path = '/home/picard/2ndDisk/carData/run_28apr/trajectories.pkl'
 
    t1 = 1493425694.71 + 5
    t2 = 1493425899.676476 - 100
     
    #selected_modes = [behavior.follow, behavior.circle]
    #selected_modes = [behavior.circle, behavior.follow]
    #selected_modes = [behavior.follow]
    selected_modes = [behavior.circle]
    
    show_graphics = True
    calculate_new = True
    
    if calculate_new:
        resulting_trajectories = get_trajectories(pickle_path, t1, t2, selected_modes, show_graphics)
        pickle.dump(resulting_trajectories, open("tmp_traj_data.p", "wb"))
    else:
        resulting_trajectories = pickle.load(open("tmp_traj_data", "rb"))
    
    animate(resulting_trajectories)
    
