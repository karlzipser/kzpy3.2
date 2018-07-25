'''
Created on Jun 5, 2017

@author: Sascha Hornauer
'''

import rospy
from geometry_msgs.msg import Vector3
from std_msgs.msg import Int32
from timeit import default_timer as timer
from enum import Enum
from kzpy3.data_analysis.synth_behaviors.rescue_backup.detectors import Obstacle_Crash_Detector, Side_Tilted_Detector
import numpy as np
import matplotlib.pyplot as plt
import kzpy3.data_analysis.aruco_tools.dynamic_model as dynamic_model
import copy
debug_mode = True

class Rescue_State(Enum):
    OBSERVING = 1
    EXECUTING = 2    


class State_Info():
    
    state = None
    steer_signal = None 
    motor_signal = None
    gyro_heading = None
    acc_data = None
    

class Rescue_Handler:

    rescue_state = Rescue_State.OBSERVING

    cycle_time = 1/10. # update time in ms  

    execute_behavior = False
    last_update_time = 0
    
    _steer_cmd = 49
    _motor_cmd = 49
    
    state_publisher = None
    state_info = State_Info()    
    detector_list = []
    past_behavior_list = []
    max_listsize_past = 30 # 
    steer_max = 100.
    steer_min = 0.
    steer_min_ang = np.deg2rad(-35.)
    steer_max_ang = np.deg2rad(35.)
    
    visualize = True
    
    def __init__(self):
        
        rospy.Subscriber("/bair_car/gyro_heading", Vector3, self.heading_callback, queue_size=1)
        rospy.Subscriber("/bair_car/acc", Vector3, self.acc_callback, queue_size=1)
        rospy.Subscriber('/bair_car/state', Int32, self.state_callback)
        rospy.Subscriber('/bair_car/steer', Int32, self.steer_callback,queue_size=100)
        rospy.Subscriber('/bair_car/motor', Int32, self.motor_callback,queue_size=100)
        self.state_publisher = rospy.Publisher('/bair_car/state', Int32,queue_size=100)
        self.last_update_time = timer()
       
        # Add all detectors
        self.detector_list.append(Obstacle_Crash_Detector())
        self.detector_list.append(Side_Tilted_Detector())
        
        if self.visualize:
            plt.ion()

    def update(self):        
        
        if timer() - self.last_update_time > self.cycle_time:
            
            # Add the current state at a fixed time. Make a copy
            # so the callbacks will not change the state while we 
            # check with the detectors if there is something wrong with it
            copy_state_info = copy.deepcopy(self.state_info)
            
            self.past_behavior_list.append(copy_state_info)
            if len(self.past_behavior_list) > self.max_listsize_past:
                self.past_behavior_list.pop(0)
            
            if self.visualize:
                self.visualize_commands(self.past_behavior_list)
                        
            rescue_needed = False
            
            # Check with all detectors if rescue is needed
            for detector in self.detector_list:
                rescue_needed_new, detector_type = detector.check_state(copy_state_info)
                rescue_needed = rescue_needed or rescue_needed_new
                
            # Execute a rescue behavior, depending on the detector
            if rescue_needed:
                self.rescue_state = Rescue_State.EXECUTING
                self.execute_rescue(detector_type)
            
            # select the correct rescue behavior
            # execute the correct rescue behavior
            # Signal return to normal net mode
            # return to observance
            
            self.last_update_time = timer()
    
    def execute_rescue(self,detector_type):
        
        print "Handler to the rescue !!!" + str(detector_type)
        pass


    def state_callback(self, state):
        self.state_info.state = state
        
    def acc_callback(self, acc):
        self.state_info.acc_data = acc

    def heading_callback(self, heading):
        self.state_info.gyro_heading = heading
            
    def steer_callback(self, steering):
        self.state_info.steer_signal = steering
    
    def motor_callback(self,motor):
        self.state_info.motor_signal = motor
            
    def get_next_steer_cmd(self):
        return self._steer_cmd
            
    def get_next_motor_cmd(self):
        return self._motor_cmd
    

    
    def visualize_commands(self, past_behavior_list):
        
        
        x_pos = []
        y_pos = []
        
        initial_state = past_behavior_list[0]
        
        x = 0
        y = 0
        t_0 = 0
        t = t_0
        
        if initial_state.acc_data == None:
            return
        if initial_state.gyro_heading == None:
            return
        
        speed_old = Vector3(0.,0.,0.)
        
        a = self.get_avg_acc(initial_state.acc_data)  
        v = self.get_speed_from_acc(initial_state.acc_data,speed_old,self.cycle_time)
        print v
        psi = initial_state.gyro_heading 
        delta = self.get_angle_from_steering(initial_state.steer_signal)                
            
        for state in past_behavior_list[1:-1]:
            
            t =+ + self.cycle_time
            new_state = dynamic_model.getXYFor(x, y, t_0, v, psi.x, t, a, delta)
            # [x,y,v,psi]
            #steer_signal = state.steer_signal
            #motor_signal = state.motor_signal
            #x = state.
            
            x = new_state[0]
            y = new_state[1]
            v = new_state[2]
            psi.x = new_state[3]
            
            x_pos.append(x)
            y_pos.append(y)
        
        
        plt.scatter(x_pos,y_pos)
        plt.show()
    def get_avg_acc(self, acc_data):
        
        return np.sqrt(acc_data.x*acc_data.x+acc_data.y*acc_data.y+acc_data.z*acc_data.z)

   
    def get_angle_from_steering(self, steer_signal):
        
        if steer_signal == None:
            return 0.0
        
        steer_value = float(steer_signal.data)

        return ((steer_value / self.steer_max) * (self.steer_max_ang-self.steer_min_ang))+self.steer_min_ang
        

    def get_speed_from_acc(self,acc_data,speed_old,dt):
        
        self.remove_gravity(acc_data)
        
        speed = Vector3()
        if acc_data != None:
                            
            speed.x = speed_old.x + acc_data.x * dt
            speed.y = speed_old.y + acc_data.y * dt
            speed.z = speed_old.z + acc_data.z * dt
         
        return np.sqrt(speed.x*speed.x+speed.y*speed.y+speed.z*speed.z)
            
            
    # In this example it is assured that calls of the remove gravity function
    # will happen in one trajectory, in consecutive timesteps. If that ever changes
    # this function has to be redone since gravity will not change as expected
    gravity = Vector3()
    def remove_gravity(self,acc_data):
        
        if acc_data != None:
                    
            alpha = 0.8;
           
            self.gravity.x = alpha * self.gravity.x + (1. - alpha) * acc_data.x;
            self.gravity.y = alpha * self.gravity.y + (1. - alpha) * acc_data.y;
            self.gravity.z = alpha * self.gravity.z + (1. - alpha) * acc_data.z;

            acc_data.x =- self.gravity.x;
            acc_data.y =- self.gravity.y;
            acc_data.z =- self.gravity.z;
                    

            
if debug_mode and __name__ == '__main__':
    rospy.init_node('run_caffe',anonymous=True)
    
    rescue_behavior = Rescue_Handler()
    
    while not rospy.is_shutdown():
        
        rate = rospy.Rate(30)
        
        rescue_behavior.update()
        
        if rescue_behavior.execute_behavior:
            
            caf_steer = rescue_behavior.get_next_steer_cmd()
            caf_motor = rescue_behavior.get_next_motor_cmd()
            
        rate.sleep()
