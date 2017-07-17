'''
Created on May 8, 2017

@author: Sascha Hornauer
'''

from scipy.ndimage import gaussian_filter1d
from kzpy3.data_analysis.trajectory_generator.trajectory_tools import *
import cv2
import sys
import matplotlib.pyplot as plt
from kzpy3.data_analysis.aruco_tools.dynamic_model import *
from operator import add
import copy
import time
import numpy as np
import numpy.linalg
from timeit import default_timer as timer
from kzpy3.data_analysis.trajectory_generator.data_structure.entities import Obstacle
from kzpy3.data_analysis.aruco_tools.mode import behavior
import angles
import sys, random, math

max_v = 4.47  # approximate max speed according to the internet for the axial bomber
distance_from_boundary_of_circle = 2.  #
desired_speed = 2.0  # m/s

def get_trajectory_simple(own_xy, goal_xy, own_heading, steps):
    # Very simple prototype. Heading is assumed to be 0 deg
    t_0 = 0
    v=0
    a = 0
    
    steering_deltas = []
    # TODO THIS IS A HACK
    heading = own_heading
    
    act_xy = own_xy    
    
    for i in range(steps):
        t = i
    
        # Get distance to current goal
        # goal_diff = np.hypot(goal_xy[0] - own_xy[0], goal_xy[1] - own_xy[1])
        
        # Get the straight angle to the current goal
        angle_own_goal = np.arctan2(goal_xy[1] - act_xy[1], goal_xy[0] - act_xy[0])
                
        # Compare our angle, get the difference to the heading against the goal
        angle_diff = angle_own_goal - heading
        
        # Calculate steering angle 
        delta = np.arctan2(np.sin(angle_diff), np.cos(angle_diff))
        
        if(delta > np.pi / 2.):
            delta = np.pi / 2.
        if delta < -np.pi / 2.:
            delta = -np.pi / 2.
        
        steering_deltas.append(delta)
        
        # TODO do this later
        # Since this technique leads to a dog leg (bend) we will correct this by the distance to the center line
        #distance_to_center_line = np.linalg.norm(np.cross(np.array(current_xy_own) - np.array(goal_xy), np.array(goal_xy) - (act_pos_x, act_pos_y)) / np.linalg.norm(np.array(current_xy_own) - np.array(goal_xy)))
        
        # We make the assumption that no single point is further away from 
        # the center line than the center line is actually long, for normalization
        #distance_cl_norm = distance_to_center_line / (goal_diff)
        
        # Finaly steering is reduced, according to the distance
    #     delta = delta * distance_cl_norm
    #     if math.isnan(delta):
    #         delta = 0.0print "hihi"
        x,y,v,psi = getXYFor(act_xy[0], act_xy[1], t_0, v, heading, t, a, delta)
        
        act_xy[0] = x
        act_xy[1] = y
        heading = psi
    
    return steering_deltas


def get_emergency_trajectories(obstacle_pos, current_xy_own, length):
    
    angle_of_obstacle = np.arctan2(obstacle_pos[1] - current_xy_own[1], obstacle_pos[0] - current_xy_own[0])
      
    if angle_of_obstacle < 0:
        return np.ones(length) * -np.pi / 2.
    else:
        return np.ones(length) * np.pi / 2.


def convert_to_motor(resulting_motor_cmds):
    
    max_motor = 75.0
    min_motor = 49.0
    range = max_motor - min_motor
    
    # normalize
    resulting_motor_cmds = map(div, resulting_motor_cmds, [desired_speed] * np.ones(len(resulting_motor_cmds)))
    resulting_motor_cmds = map(mul, resulting_motor_cmds, [range] * np.ones(len(resulting_motor_cmds)))
    resulting_motor_cmds = map(add, resulting_motor_cmds, [49.0] * np.ones(len(resulting_motor_cmds)))
    
    return resulting_motor_cmds
    

def close_to_boundary(current_xy_own, radius_arena, allowed_own_distance):
    return distance_2d(current_xy_own, [0.0, 0.0]) > (radius_arena - allowed_own_distance)


def get_slowdown_cmd(trajectory_length):
    # A more sophisticated behavior can be planned later, based on the following lines
    # distance_boundary_norm = (distance_2d(current_xy_own, [0.0, 0.0]) / radius_arena)
    # resulting_motor_cmds.append(np.ones(trajectory_length)*(1-distance_boundary_norm))
    # resulting_motor_cmds.append(np.ones(trajectory_length) * (1 - distance_boundary_norm))
    return np.linspace(0.4, 0.0, trajectory_length)



    
