'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''

import rospy
from std_msgs.msg import Float32, Int32
from kzpy3.Sascha.util.position_filter_interface import Position_Filter
import numpy as np
import matplotlib.pyplot as plt

class Test_Me():
    
    # It is important to use the position filter as a class because
    # it needs to keep track of a number of values.
    # The amount of previous positions it bases its estimation on can be
    # set. 10 seems to be a good tradeoff between performance and speed
    test_filter = Position_Filter(10)
    
    aruco_x = None
    aruco_y = None
    steering = None
    
    def aruco_x_callback(self, data):
        self.aruco_x = data.data
        
    def aruco_y_callback(self, data):
        self.aruco_y = data.data
        
    def steering_callback(self,data):
        self.steering = data.data
        
    def __init__(self):
        rospy.Subscriber("/bair_car/aruco_position_x", Float32, self.aruco_x_callback)
        rospy.Subscriber("/bair_car/aruco_position_y", Float32, self.aruco_y_callback)
        rospy.Subscriber("/bair_car/cmd/steer", Int32, self.steering_callback)
        rospy.init_node('aruco_tester', anonymous=True)
    
        # In this example file the filter is queried with a specific rate. It can also
        # be queried at a different 
        rate = rospy.Rate(10)
                
        # For visualization
        fig, ax = plt.subplots()
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)            
        kalman, = ax.plot([], [], marker='o', linestyle='None', color='r')
        original, = ax.plot([], [], marker='o', linestyle='None', color='b')        
        #plt.ion()
        #plt.show()
        
        
        while not rospy.is_shutdown():
            
            if not self.aruco_x or not self.aruco_y:
                continue

            position_xy = (self.aruco_x, self.aruco_y)
            
            # The filtered position is actually not yet based on heading or steering
            # but purely on position information. Still the same heading which is put
            # in is right now also returned
            mock_up_heading = np.pi / 2.
            
            filtered_position, heading = self.test_filter.get_xy_position(position_xy, mock_up_heading , self.steering)
            
            if filtered_position:
                kalman.set_data([[filtered_position[0]], [filtered_position[1]]])
                original.set_data([[position_xy[0]], [position_xy[1]]])
                
                plt.draw()
                
                plt.pause(0.001)
            rate.sleep()
            
    

if __name__ == '__main__':
    
    test = Test_Me()
    
    
    
    
    
    
    
    
