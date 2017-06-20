'''
Created on Apr 26, 2017

@author: Sascha Hornauer
'''
import roslib

roslib.load_manifest('dbw_mkz_msgs')

import rospy
import std_msgs.msg
import numpy as np
import threading
from time import sleep
from collections import deque
from dbw_mkz_msgs.msg import SteeringCmd
from timeit import default_timer as timer


debug = False
if debug:
    send_with_rate = 1
else:
    send_with_rate = 10



class Lilliput_steering():
    
    print("LILLIPUT PUBLISHER STARTED +++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    steeringCmd_msg = None
    steer_pub = rospy.Publisher('/vehicle/steering_cmd', SteeringCmd, queue_size=10)
    
    counter = 0
    watchdog_counter_used = False
    watchdog_throttle = False
    throttle_value = 0.5
    
while(True):

    # The five previous steering commands are used to smooth the response. They
    # are initialised by 49, because that is by definition, straight.
    # A deque ist used for its efficient list-shift
    previous_steering_commands = deque([49,49,49,49,49,49,49,49])
    smoothing_vector = np.array([0.05,0.05,0.10,0.10,0.15,0.15,0.2,0.2])
    last_execution_time = timer()
    thread_started = False
    
    
    def __init__(self):
        self.lilliput_steering()
        
        

    def steering_callback(self,steering_model_data):
        #print("CALLBACK")        
        '''
        The dbw_mkz SteeringCmd message looks like this:
        # Steering Wheel
        float32 steering_wheel_angle_cmd        # rad, range -8.2 to 8.2
        float32 steering_wheel_angle_velocity   # rad/s, range 0 to 8.7, 0 = maximum
        
        # Enable
        bool enable
        
        # Ignore driver overrides
        bool ignore
        
        # Disable the driver override audible warning
        bool quiet
        
        # Watchdog counter (optional)
        uint8 count
        '''
        
        # Sometimes the neural net is faster, sometimes slower. Every time it processes an input
        # image it will publish a steering command and that would affect the smoothing of the
        # values. To produce a more stable behavior, a timer is used. 
        time_now = timer()
    
        max_update_frequency = 15 #hz
        time_passed = (time_now - self.last_execution_time)*100.0
        
        steeringCmd_msg = None
        
        if time_passed*max_update_frequency > 100.0:
            self.last_execution_time = time_now
        
            steeringCmd_msg = SteeringCmd()
            
            # The original steering values are in between 0 and 100 where 100 is max left and 0 is max right.
            # This is first smoothed over 5 previous values and then converted to the range -8.2 to 8.2
            
            # input from the callback
            steering_lilliput = steering_model_data.data
            
            # The queue is emptied on the left
            self.previous_steering_commands.popleft()
            
            # The newest value added
            self.previous_steering_commands.append(steering_lilliput)
            
            # The newest steering command is the weighted sum of the previous 6 input commands
            # with a weighting vector, designed to change the value first by a large, later by a minor margin
            steering_lilliput = np.sum(self.previous_steering_commands*self.smoothing_vector)
            
            # Norm to [0,1]
            steering_norm = steering_lilliput / 100.0
                    
            # Regard DMZ limits
            steer_max_left = -8.2 # rad
            steer_max_right = 8.2 # rad
            
            # Observe the range of the DMZ limits ( to make it possible to change those values later )
            steer_range = np.abs(steer_max_left-steer_max_right)
            
            # Map the normed steering values from lilliput to the dmz
            steer_output_rad = (steering_norm * steer_range) - (steer_range / 2.0)
            
            # Put it into a message
            steeringCmd_msg.steering_wheel_angle_cmd = steer_output_rad
            
            # Fill other fields
            steeringCmd_msg.steering_wheel_angle_velocity = 1.0
            
            steeringCmd_msg.enable = True
            
            steeringCmd_msg.ignore = False
            
            steeringCmd_msg.quiet = False
            
            # If the watchdog counter should be increased do so
            if(self.watchdog_counter_used):
                steeringCmd_msg.count = self.counter
                
                # If the watchdog counter rises to quickly there is
                # another trick here to make him rise slower 
                
                if(self.watchdog_throttle):
                    if(np.random() > self.throttle_value):
                        self.counter = self.counter + 1
                else:
                    self.counter = self.counter + 1
                
            self.steeringCmd_msg = steeringCmd_msg
            
            # The message has to be sent at a higher rate than
            # the net is working so that rate is realized here
            #if not self.thread_started:
            #    threading.Thread(target=self.sendMessageAtRate).start()
            #    self.thread_started = True
            
            self.steer_pub.publish(self.steeringCmd_msg)
            #print("Publish commands ++++++++++++++++++++++++++++++++++++++++++++++")
            # This will be tested first with the new watchdog counter
    
    def lilliput_steering(self):
        if debug:
            rospy.init_node('lilliput_steering', anonymous=True)
                
        rospy.Subscriber("/bair_car/cmd/steer", std_msgs.msg.Int32, self.steering_callback)
        
        if debug:
            rospy.spin()
               
    #def sendMessageAtRate(self):
    #    
    #    # Send 2 messages at a rate of 10hz. Since the net is throttle
    #    # to 10 hz we expect that this way enough messages should be produced
    #    # to achieve constantly 10 hz of commands. 
    #    for i in range(0,2):
    #        self.steer_pub.publish(self.steeringCmd_msg)
    #        sleep(1/send_with_rate)

if debug:
    test = Lilliput_steering()