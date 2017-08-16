'''
Created on Jul 11, 2017

@author: Sascha Hornauer
'''

import rospy

from marvelmind_nav.msg import hedge_pos as hedge_pos_msg
from marvelmind_nav.msg import beacon_pos_a as beacon_pos_a_msg
from collections import defaultdict
from time import sleep
import numpy as np
from operator import div, add, mul
from geometry_msgs.msg import Vector3
from kzpy3.data_analysis.trajectory_generator import trajectory_planer
from kzpy3.data_analysis.trajectory_generator import trajectory_tools
from kzpy3.data_analysis.trajectory_generator.trajectory_tools import get_center

debug = True


class Beacon_Driver():
    
    beacon_positions = defaultdict(int)

    own_pos = None
    goal_pos = None
    
    gyro_heading = 0.0
    heading_correction = 0.0
    pos_heading = 0.0
    min_speed_for_heading_calc = 0.1
    center = None
    
    recent_positions = []
    recent_pos_length = 5 # No of positions kept in the list
    
    def __init__(self):
        
        #if debug: rospy.init_node('hedge_listener', anonymous=True)
        #print "Starting beacon driver"
        rospy.Subscriber("/bair_car/hedge_pos", hedge_pos_msg, self.hedge_pos_callback)
        rospy.Subscriber("/bair_car/beacons_pos_a", beacon_pos_a_msg, self.beacons_pos_a_callback)
        rospy.Subscriber("/bair_car/gyro_heading", Vector3, self.gyro_heading_callback)
        
        #if debug: rospy.spin()
    
    def get_speed(self,recent_positions):
    
        speed = 0.0
    
        for i in range(0,len(recent_positions)-1):
            
            x = recent_positions[i][0]
            y = recent_positions[i][1]
            x_ = recent_positions[i+1][0]
            y_ = recent_positions[i+1][1]
            
            speed += np.hypot(x_-x,y_-y)
            
    
        return speed    
    
    def set_own_pos(self,own_pos):
        '''
        Will actualize the current pos and also update the list of recent pos
        '''
        self.own_pos = own_pos
        if len(self.recent_positions) > self.recent_pos_length:
            self.recent_positions.pop(0)
        self.recent_positions.append(own_pos)
        
        # If the list of recent positions is full
        if len(self.recent_positions) >= self.recent_pos_length:
            
            # calculate the speed of the vehicle
            avg_speed = self.get_speed(self.recent_positions)
            
            if avg_speed > self.min_speed_for_heading_calc:

                # Calculate heading according to the changes in the position
                pos_heading = trajectory_tools.get_heading(self.recent_positions)
                # Calculate the heading correction term according to that heading
                self.heading_correction = pos_heading - self.gyro_heading
                self.set_heading(pos_heading)
    
    # The property setter did not work for own_pos
    def get_own_pos(self):
        return self.own_pos
    
    def get_heading(self):
        print "heading is now " + str(self.pos_heading)
        return self.pos_heading
    
    def set_heading(self, heading):
        #return self.gyro_heading + self.heading_correction
        self.pos_heading = heading
        
    def gyro_heading_callback(self,data):
        # Make a deg to rad conversion
        self.gyro_heading = np.deg2rad(data.x)
    
    def hedge_pos_callback(self,data):
        self.set_own_pos([data.x_m,data.y_m])

    def beacons_pos_a_callback(self,data):
        self.beacon_positions[int(data.address)] = [data.x_m,data.y_m]
        self.center = get_center(self.beacon_positions.values())
    
    def _get_steering_cmd(self, steer_input, motor_input):
        
        # Check if too close to boundary.
        
        # If yes steer towards center
        
        # If no just pass on the steer and motor signal

        #####
        
        # Goal calculations 
        
        # If the center is unknown yet pass the network signal through
        if self.center == None:
            return steer_input, motor_input
        
        # Check if position out of circle
        center_x = self.center[0]
        center_y = self.center[1] 
        own_x = self.center[0] 
        own_y = self.center[0]  
        
        ######
                
        # If the beacon driver did not receive all the needed information we just pass the
        # network signal through
        if self.own_pos == None or self.goal_pos == None or self.get_heading() == None:
            return steer_input, motor_input
        steering_deltas = trajectory_planer.get_trajectory_simple(self.own_pos, self.goal_pos, self.get_heading(), 10)
        
        return self._convert_to_car_steering(steering_deltas)
    
    def convert_delta_to_steer(self,delta_values):
    
        # delta values are assumed to be in +pi/2,-pi/2
        
        max_left_command = 0
        max_right_command = 100
        
        value_range = max_left_command-max_right_command
        
        norm_values = map(div,delta_values,[np.pi]*np.ones(len(delta_values)))
        norm_values = map(add,norm_values,[0.5]*np.ones(len(delta_values)))
        norm_values = map(mul,norm_values,[value_range]*np.ones(len(delta_values)))
        norm_values = map(add,norm_values,[max_right_command]*np.ones(len(delta_values)))
        
        return norm_values
        
    def _convert_to_car_steering(self, steering_deltas):
        
        return self.convert_delta_to_steer(steering_deltas)
        
    def get_steer_motor_cmd(self):
        
        # TODO: get actual motor value
        motor_cmd = 55
        
        # Get from the list of steering commands only the most recent
        steering_cmd = self._get_steering_cmd()
        if type(steering_cmd) is list:
            steering_cmd = steering_cmd[0]
        
        return steering_cmd,motor_cmd, self.center
    

# unittest
if __name__ == '__main__':
    
    beacon_driver = Beacon_Driver()
    
    hedge_pub = rospy.Publisher("/bair_car/hedge_pos", hedge_pos_msg, queue_size=10)
    beacon_pub = rospy.Publisher("/bair_car/beacons_pos_a", beacon_pos_a_msg,queue_size=10)
    heading_pub = rospy.Publisher("/bair_car/gyro_heading", Vector3,queue_size=10)
    
    rospy.init_node('hedge_tester', anonymous=True)
    
    rate = rospy.Rate(10) # 10hz
    
    i = 0
    
    
    while not rospy.is_shutdown():
        
        i += 1
        
        beacon_pos1 = beacon_pos_a_msg(1,0.0,0.0,0.0)
        beacon_pos2 = beacon_pos_a_msg(2,3.0,0.0,0.0)
        beacon_pos3 = beacon_pos_a_msg(3,0.0,3.0,0.0)
        beacon_pos4 = beacon_pos_a_msg(4,3.0,3.0,0.0)
        
        beacon_pub.publish(beacon_pos1)
        beacon_pub.publish(beacon_pos2)
        beacon_pub.publish(beacon_pos3)
        beacon_pub.publish(beacon_pos4)
        
        hedge_pos = hedge_pos_msg(i,1.0+i,1.5+i,0.0,0)
        hedge_heading = Vector3(80.0,0.0,0.0)
        
        hedge_pub.publish(hedge_pos)
        heading_pub.publish(hedge_heading)
        
        #print beacon_driver.get_steer_motor_cmd()
        
        rate.sleep()

    
    
    #while True:
    #    #print beacon_driver.get_motor_steering_cmd()
    #    sleep(1)
    