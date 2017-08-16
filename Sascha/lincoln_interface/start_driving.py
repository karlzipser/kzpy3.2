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
from dbw_mkz_msgs.msg import SteeringCmd, ThrottleCmd, GearCmd, BrakeCmd, Gear
from timeit import default_timer as timer


'''
/vehicle/brake_cmd
/vehicle/gear_cmd
/vehicle/steering_cmd
/vehicle/throttle_cmd
'''
    
    


throttle_pub = rospy.Publisher('/vehicle/throttle_cmd', ThrottleCmd, queue_size=10)
gear_cmd_pub = rospy.Publisher('/vehicle/gear_cmd', GearCmd, queue_size=10)
brake_pub = rospy.Publisher('/vehicle/brake_cmd', BrakeCmd, queue_size=10)

# That is the state of the system before the program runs

    

def brake_on_off(brake_on):
    ''' Brake

    # Brake pedal
    # Options defined below
    float32 pedal_cmd
    uint8 pedal_cmd_type
    
    # Brake On Off (BOO), brake lights
    bool boo_cmd
    
    # Enable
    bool enable
    
    # Ignore driver overrides
    bool ignore
    
    # Watchdog counter (optional)
    uint8 count
    
    uint8 CMD_NONE=0
    uint8 CMD_PEDAL=1   # Unitless, range 0.15 to 0.50
    uint8 CMD_PERCENT=2 # Percent of maximum torque, range 0 to 1
    uint8 CMD_TORQUE=3  # Nm, range 0 to 3250
    
    float32 TORQUE_BOO=520  # Nm, brake lights threshold
    float32 TORQUE_MAX=3412 # Nm, maximum torque
    
    '''
    if not brake_on:
        brake_msg = BrakeCmd()
        brake_msg.pedal_cmd_type = 1
        brake_msg.pedal_cmd = 0.15
        brake_msg.boo_cmd = False
        brake_msg.enable = True
        brake_on = False
    else:
        brake_msg = BrakeCmd()
        brake_msg.pedal_cmd_type = 1
        brake_msg.pedal_cmd = 0.5
        brake_msg.boo_cmd = True
        brake_msg.enable = True
        brake_on = True
        
    brake_pub.publish(brake_msg)
    print("Brake on " + str(brake_msg))
    
    

    
def gear_shift_to(gear_no):
    
    ''' Gear
    uint8 gear
    
    uint8 NONE=0
    uint8 PARK=1
    uint8 REVERSE=2
    uint8 NEUTRAL=3
    uint8 DRIVE=4
    uint8 LOW=5
    '''
    
    ''' GearCmd
    # Gear command enumeration
    Gear cmd
    '''
    gear = Gear()
    gear.gear = gear_no
    gear_msg = GearCmd()
    gear_msg.cmd = gear
    gear_cmd_pub.publish(gear_msg)
    print("Gear shifted")
def accelerate():
    
    ''' Throttle 

    # Throttle pedal
    # Options defined below
    float32 pedal_cmd
    uint8 pedal_cmd_type
    
    # Enable
    bool enable
    
    # Ignore driver overrides
    bool ignore
    
    # Watchdog counter (optional)
    uint8 count
    
    uint8 CMD_NONE=0
    uint8 CMD_PEDAL=1   # Unitless, range 0.15 to 0.80
    uint8 CMD_PERCENT=2 # Percent of maximum throttle, range 0 to 1
    
    '''

    
    throttle_msg = ThrottleCmd()
    throttle_msg.pedal_cmd_type = 2
    throttle_msg.pedal_cmd = 0.05 # 5 percent throttle
    throttle_msg.enable = True
    throttle_pub.publish(throttle_msg)
    
    
    stop_msg = ThrottleCmd()
    stop_msg.pedal_cmd_type = 2
    stop_msg.pedal_cmd = 0.0 # 5 percent throttle
    stop_msg.enable = True
    
    print("Accelerate by " + str(throttle_msg))
    throttle_pub.publish(throttle_msg)
    
    sleep(1)
    throttle_pub.publish(stop_msg)
    print("Accelerartion stopped again")
    
    # Accelerate slightly, wait a second, stop

''' Gear
uint8 gear

uint8 NONE=0
uint8 PARK=1
uint8 REVERSE=2
uint8 NEUTRAL=3
uint8 DRIVE=4
uint8 LOW=5
'''


rospy.init_node('little_driver', anonymous=True)

#gear_shift_to(1)
#sleep(1) 
brake_on_off(True) # Turn on the brake
sleep(1)
gear_shift_to(4) 
sleep(1)
brake_on_off(False) # Turn off the brake
sleep(1)
accelerate() # Accelerate slightly
sleep(3)
gear_shift_to(1) # Come to a halt again
# The final brake will be done by the driver because the brake method would brake rather suddenly
