'''
Created on May 8, 2017

@author: Sascha Hornauer
'''

from scipy.ndimage import gaussian_filter1d
from kzpy3.data_analysis.trajectory_generator.trajectory_tools import *
import cv2
import sys
import matplotlib.pyplot as plt
from aruco_tools.dynamic_model import *
from operator import add
import copy
import time
import numpy as np
import numpy.linalg
from timeit import default_timer as timer
from trajectory_generator.data_structure.entities import Obstacle
from aruco_tools.mode import behavior
import angles
import sys, random, math, pygame
from pygame.locals import *


framerate = 1. / 30.
max_v = 4.47  # approximate max speed according to the internet for the axial bomber
distance_from_boundary_of_circle = 2.  #
desired_speed = 2.0  # 
radius_arena = 4.28

def get_state(own_xy, timestep_start, timestep_end):

    # Init our own position
    init_xy = own_xy[timestep_start]
         
    # Get our intended heading based on three timesteps in the future
    # which add as slight smoothing
    heading = get_heading(own_xy[timestep_start:timestep_start + timestep_end])
    # Get the velocity over the first two timesteps
    # velocity = get_velocities([own_xy[timestep_start], own_xy[timestep_start + 1]], framerate)
    return init_xy, heading

def sample_values(values, no_of_samples):
    
    if len(values) == no_of_samples:
        return values
    if len(values) < no_of_samples:
        raise NotImplementedError("The case that there are less trajectory points has not been implemented")
    else:
        n = len(values)
        m = no_of_samples
        # substract one for the 0 value which we want to have
        index = [i * n // m + n // (2 * m) for i in range(m)]
        index.pop(len(index) - 1)
        index.insert(0, 0)
        return np.array(values)[index]
    

def convert_path_to_steeering_angles(resulting_trajectories):
    
    trajectories = []
    
    for trajectory in resulting_trajectories:
        if len(trajectory) == 2:
            trajectory_angles = []
            xy_positions = np.transpose(trajectory)
            
            for i in range(0, len(xy_positions) - 2):
                x1 = xy_positions[i][0]
                y1 = xy_positions[i][1]
                x2 = xy_positions[i + 1][0]
                y2 = xy_positions[i + 1][1]
                x3 = xy_positions[i + 2][0]
                y3 = xy_positions[i + 2][1]
                
                side_a = np.hypot(x3 - x2, y3 - y2)
                side_b = np.hypot(x2 - x1, y2 - y1)
                side_c = np.hypot(x3 - x1, y3 - y1)
            
                trajectory_angle = np.arccos((np.power(side_a, 2) + np.power(side_b, 2) - np.power(side_c, 2)) / (2.*side_a * side_b))
                # The arccos outputs the angle in 0, pi it is however expected in -pi, pi
                trajectory_angle = (trajectory_angle * 2.) - np.pi

                trajectory_angles.append(trajectory_angle)
            
            trajectories.append(trajectory_angles)
        else:
            # If the trajectory contains angles, add it as it is
            trajectories.append(trajectory)
    return trajectories


def get_emergency_trajectories(obstacle_pos, current_xy_own, number):
    
    angle_of_obstacle = np.arctan2(obstacle_pos[1] - current_xy_own[1], obstacle_pos[0] - current_xy_own[0])
      
    if angle_of_obstacle < 0:
        return np.ones(number) * -np.pi / 2.
    else:
        return np.ones(number) * np.pi / 2.


def get_center_trajectory(own_xy, other_xys, act_timestep, trajectory_length):
    try:
        heading = get_heading(own_xy[act_timestep:act_timestep + 3])
    except:
        try:
            heading = get_heading(own_xy[act_timestep - 3:act_timestep])
        except:
            heading = 0.0 
            # own_xy, other_xys, timestep, heading_own,delta, goal_xy, desired_speed, ideal_distance, min_distance_to_goal):
    center_traj, dismissed_motor, steering_deltas, safe_path = get_trajectory_to_goal(own_xy, other_xys, act_timestep, heading, 0.0, [0.0, 0.0], 2.0, 1.0 , 0.2, trajectory_length)

    return center_traj, steering_deltas, safe_path

def get_center_circle_points(own_xys):
    
    goalxys = []
    goal_offset = -(np.pi / 8.0)
    circle_radius = radius_arena - distance_from_boundary_of_circle  # meter
    
    # calculate positions on a circle near the center
    for pos in own_xys:
        own_x = pos[0]
        own_y = pos[1]
            
        # Get a point on the circle
        distance_goalpoint = circle_radius
        
        # Now take the distance to the goalpoint in combination with the angle to the 
        # goalpoint to make out the intersection of the straight line in between the
        # car and that circle
        angle_center = np.arctan2(own_y, own_x)
        
        # Change the angle to be in front of the vehicle like the carrot on a stick
        angle_goalpoint = angle_center + goal_offset
        
        # Next calculate that new point
        goal_xy = cv2.polarToCart(distance_goalpoint, angle_goalpoint)
        goal_xy = [goal_xy[0][0][0], goal_xy[1][0][0]]
        
        # If the distance of that new goalpoint is too far from our position
        
        goalxys.append(goal_xy)
        
    return goalxys
    

########################################################## 
# Modified after Steve LaValle
# 2011
# http://msl.cs.illinois.edu/~lavalle/sub/rrt.py
#
#########                         

class Node():
    
    _next_p = None
    _previous_p = None
    _point = None
    
    def __init__(self, point, previous_p, next_p):
        
        if not isinstance(point,tuple):
            raise Exception("Wrong type of point, should be tuple but is " + str(type(point)) + " - " + str(point))
        
        self._next_p = next_p
        self._previous_p = previous_p
        self._point = point

def dist(p1, p2):
    if not isinstance(p1, Node):
        raise Exception("Wrong type of p1, should be Node but is " + str(type(p1)) + " - " + str(p1))
    if not isinstance(p2, Node):
        raise Exception("Wrong type of p2, should be Node but is " + str(type(p2)) + " - " + str(p2))
    
        
    p1 = p1._point
    p2 = p2._point
    
    return np.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def step_from_to(p1, p2, epsilon):
    
        previous_node = p1

        if dist(p1, p2) < epsilon:
            return Node(p2._point, previous_node, None)
        else:
                    
            p1 = p1._point
            p2 = p2._point
            
            theta = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
            return Node((p1[0] + epsilon * np.cos(theta), p1[1] + epsilon * np.sin(theta)), previous_node, None)



def get_safe_path(own_xy, other_xys, goal_xy, safety_range, distance_to_goal, timestep):
    
    visualize = False
    
    XDIM = 640
    YDIM = 480
    WINSIZE = [XDIM, YDIM]
    
    if visualize:
        pygame.init()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption('RRT      S. LaValle    May 2011')
        white = 255, 240, 200
        black = 20, 20, 40
        red = 255,0,0
        screen.fill(black)
    seed = 42
    np.random.seed(seed)
    numnodes = 5000
    nodes = []
    other_current_xy = []
    epsilon = 0.4
    own_point = Node((own_xy[0], own_xy[1]), None, None)
    scale_factor = 50
    shift_factor = 50
    nodes.append(own_point)

    # Add the other positions to a short list
    for other_xy in other_xys:
            # Right now we look at the current situation and search a path. 
            # It is repeated each time in the future we look for a path.
            other_current_xy.append(other_xy[timestep])

    for i in range(numnodes):
        
        next_node = nodes[0]
        
        random_point_safe = False
        while not random_point_safe:
            random_point = Node((np.random.uniform(low=-1.0,high=1.0) * radius_arena, np.random.uniform(low=-1.0,high=1.0) * radius_arena), None, None)
            random_point_safe = True
            # Check if new point is not too close to obstacle
            for other_xy in other_current_xy:
                if dist(random_point, Node(other_xy, None, None)) < safety_range:
                    random_point_safe = False
                    break
        
        for act_node in nodes:
        
            if dist(act_node, random_point) < dist(next_node, random_point):
                next_node = act_node
                
        newnode = step_from_to(next_node, random_point, epsilon)
            
        # Check if new point is not too close to obstacle
        newnode_safe = True
        for other_xy in other_current_xy:
            if dist(newnode, Node(other_xy, None, None)) < safety_range:
                # If it is too close, the node will not be appended
                newnode_safe = False
                break
            
        if not newnode_safe:
            continue
            
        nodes.append(newnode)
        
        if visualize:
          
            vis_point_a = (next_node._point[0]*scale_factor+4*shift_factor,next_node._point[1]*scale_factor+shift_factor)
            vis_point_b = (newnode._point[0]*scale_factor+4*shift_factor,newnode._point[1]*scale_factor+shift_factor)
            
            pygame.draw.line(screen, white, vis_point_a,vis_point_b)
            pygame.display.update()

        if dist(newnode, Node(goal_xy,None,None)) < distance_to_goal:
            return_path = []
            
            previous = newnode._previous_p
            return_path.append(newnode)
            
            while(previous != None):
                return_path.append(previous)
                previous = previous._previous_p
                
            return return_path
            

#########
# Modified after Steve LaValle
# 2011
# http://msl.cs.illinois.edu/~lavalle/sub/rrt.py
#
##########################################################

def get_trajectory_to_goal(own_xy, other_xys, timestep, heading_own, delta, goal_xy, desired_speed, ideal_distance, min_distance_to_goal, trajectory_length):
    
    max_allowed_distance_to_obstacle = 0.3
    start_evasion_range = 1.0
    
    safe_path = None
    
    # We might have a number of sub-goals if we encounter problems on our way.
    # So we initialise a list
    goal_xys = []
    goal_xys.append(goal_xy)

    new_traj, motor_speeds, deltas, is_colliding = get_model_based_path(own_xy, other_xys, timestep, heading_own, delta, goal_xys, desired_speed, 
                                                                             ideal_distance, min_distance_to_goal, trajectory_length, max_allowed_distance_to_obstacle)
    
    if is_colliding:
        
        # Get first goal
        goal_x = goal_xys[0][0]
        goal_y = goal_xys[0][1]
        
        own_x = own_xy[timestep][0]
        own_y = own_xy[timestep][1]
        
        # since the direct way is colliding, we plan a different route
        safe_path = get_safe_path((own_x,own_y), other_xys, (goal_x, goal_y), max_allowed_distance_to_obstacle, 0.4, timestep)
        
        if safe_path == None:
            # No safe path could be found, we take the original instead
            return new_traj, motor_speeds, deltas, safe_path
        
        intermediate_goals = []
        for node in safe_path:
            intermediate_goals.append(node._point)
                    
        new_traj, motor_speeds, deltas, is_colliding = get_model_based_path(own_xy, other_xys, timestep, heading_own, delta, intermediate_goals, desired_speed, 
                                                                             ideal_distance, min_distance_to_goal, trajectory_length, max_allowed_distance_to_obstacle)
        
        
        
    return new_traj, motor_speeds, deltas, safe_path
    
    

def get_model_based_path(own_xy, other_xys, timestep, heading_own, delta, goal_xys, desired_speed, ideal_distance, min_distance_to_goal, trajectory_length, allowed_distance):

    current_xy_own = own_xy[timestep] 
    heading = heading_own

    own_x = current_xy_own[0]
    own_y = current_xy_own[1]
    
    final_traj_x = []
    final_traj_y = []
    motor_speeds = []
    
    act_pos_x = own_x
    act_pos_y = own_y
    deltas = []
    
    goal_x = goal_xys[-1][0]
    goal_y = goal_xys[-1][1]
    goal_xy = goal_xys[-1]

    is_colliding = False
    
    for i in range(trajectory_length):
        
        # Get nearest goal
        goal_x = goal_xys[-1][0]
        goal_y = goal_xys[-1][1]
        goal_xy = goal_xys[-1]
        
        
    
        # Get distance to current goal
        goal_diff = np.hypot(goal_x - own_x, goal_y - own_y)
        
        # Get the straight angle to the current goal
        angle_own_goal = np.arctan2(goal_y - act_pos_y, goal_x - act_pos_x)
                
        # Compare our angle, get the difference to the heading against the goal
        angle_diff = angle_own_goal - heading
        
        # Calculate steering angle 
        delta = np.arctan2(np.sin(angle_diff), np.cos(angle_diff))
        
        if(delta > np.pi / 2.):
            delta = np.pi / 2.
        if delta < -np.pi / 2.:
            delta = -np.pi / 2.
        
        # Since this technique leads to a dog leg (bend) we will correct this by the distance to the center line
        distance_to_center_line = np.linalg.norm(np.cross(np.array(current_xy_own) - np.array(goal_xy), np.array(goal_xy) - (act_pos_x, act_pos_y)) / np.linalg.norm(np.array(current_xy_own) - np.array(goal_xy)))
        
        # We make the assumption that no single point is further away from 
        # the center line than the center line is actually long, for normalization
        distance_cl_norm = distance_to_center_line / (goal_diff)
        
        # Finaly steering is reduced, according to the distance
        delta = delta * distance_cl_norm
        if math.isnan(delta):
            delta = 0.0
        
        # The speed is calculated depending on the distance to the last goal and desired speed
        final_goal_diff = np.hypot(goal_xys[0][0] - act_pos_x, goal_xys[0][1] - act_pos_y)
        if final_goal_diff > ideal_distance:
            speed = desired_speed
        else:
            goal_diff_norm = (final_goal_diff - min_distance_to_goal) / (ideal_distance - min_distance_to_goal)
            speed = goal_diff_norm * desired_speed
        
        answer = getXYFor(act_pos_x, act_pos_y, i * 0.033, speed, heading, (i + 1) * 0.033, 0.0, delta)
        
        for other_xy in other_xys:
            if distance_2d((answer[0],answer[1]),(other_xy[timestep][0],other_xy[timestep][1])) < allowed_distance:
                is_colliding = True
        
        final_traj_x.append(answer[0])
        final_traj_y.append(answer[1])
        motor_speeds.append(speed)
        act_pos_x = answer[0]
        act_pos_y = answer[1]        
        heading = answer[3]
        deltas.append(delta)    
        
        
        # Pop old goal if it is reached and update data to it
        goal_diff = np.hypot(goal_x - act_pos_x, goal_y - act_pos_y)
        if goal_diff < min_distance_to_goal:
            goal_xys.pop(-1)
        if not goal_xys:
            break
               
    
    return [final_traj_x, final_traj_y], motor_speeds, deltas, is_colliding
    

def convert_to_motor(resulting_motor_cmds):
    
    max_motor = 75.0
    min_motor = 49.0
    range = max_motor - min_motor
    
    
    # normalize
    resulting_motor_cmds = map(div, resulting_motor_cmds, [desired_speed] * np.ones(len(resulting_motor_cmds)))
    resulting_motor_cmds = map(mul, resulting_motor_cmds, [range] * np.ones(len(resulting_motor_cmds)))
    resulting_motor_cmds = map(add, resulting_motor_cmds, [49.0] * np.ones(len(resulting_motor_cmds)))
    
    return resulting_motor_cmds
    
goal_offset_limit = 150
allowed_goal_distance = 0.3
goal_ideal_distance = 50
d_timestep_goal = 60

def get_goal_position(goal_xys, own_xy, other_xys, timestep, exact_following):      
    global d_timestep_goal
    
    if other_xys:
        goal_near_obstacle = True
    else:
        goal_near_obstacle = False 
        
    if exact_following:
        return goal_xys[timestep]
        
    while (goal_near_obstacle):
    # The goal is in front on the observed trajectory, further in time.
    # If it is too far than a certain value, keep it at that value
        if d_timestep_goal > goal_offset_limit:
            d_timestep_goal = goal_offset_limit            
        
        # Every time we try to get the goal distance towards the ideal goal distance
        # when it quite far in front without reasons
        if d_timestep_goal > goal_ideal_distance:
            d_timestep_goal -= 1
      
        # If the end of the trajectory is reached, the endpoint will 'wait' at the last timestamp 
        if timestep + d_timestep_goal >= len(own_xy):
            d_timestep_goal = 0
      
        goal_xy = goal_xys[timestep + d_timestep_goal]   
                
        # Check if obstacle is too close to the goal or to the vehicle
        for other_position in other_xys:
            obstacle_pos = (other_position[timestep][0], other_position[timestep][1])        
            goal_near_obstacle = distance_2d(obstacle_pos, goal_xy) < allowed_goal_distance
            
            # If the end of the timesteps is reached the last found goal will be returned
            # anyway. This information can be retreived through the length of own_xy
            # The -1 is for the -1 we substract each run
            if len(own_xy) <= timestep + d_timestep_goal + 1:
                return goal_xy

        if goal_near_obstacle:
            # Look for a new goal along the trajectory if there is no explicit trajectory
            # to follow for the goal
            d_timestep_goal += 10 
    
    goal_xy = goal_xys[timestep + d_timestep_goal]   
    
    return goal_xy



def close_to_boundary(current_xy_own, radius_arena, allowed_own_distance):
    return distance_2d(current_xy_own, [0.0, 0.0]) > (radius_arena - allowed_own_distance)


def get_slowdown_cmd(trajectory_length):
    # A more sophisticated behavior can be planned later, based on the following lines
    # distance_boundary_norm = (distance_2d(current_xy_own, [0.0, 0.0]) / radius_arena)
    # resulting_motor_cmds.append(np.ones(trajectory_length)*(1-distance_boundary_norm))
    # resulting_motor_cmds.append(np.ones(trajectory_length) * (1 - distance_boundary_norm))
    return np.linspace(0.4, 0.0, trajectory_length)


def get_batch_trajectories(own_xy, other_xys, timestep_start, plot_graphics, end_timestep, goal_xys, act_behavior):
    '''
    Returns a short term evasion trajectory, in steering commands for 
    as many timesteps ahead as given in between timestep_start and timestep_ahead.
    Note that the trajectory will start one timestep further than timestep_start because
    one timestep is needed to retrieve information about the start conditions
  
    '''
    allowed_own_distance = 1.5
    min_distance_to_goal = 0.4
    ideal_distance = 2.0  # meter in following and to the boundary
    framerate = (1. / 30.)
    

    trajectory_length = 30
    resulting_trajectories = []
    resulting_motor_cmds = []
    resulting_deltas = []

    plt_vehicle = None
    plt_boundary = None
        
    init_xy_own, heading_own = get_state(own_xy, timestep_start, 4)  # smooth heading over 3 timesteps in the future
     
    if plot_graphics:
        plt.ion()
        if plt_boundary == None:
            plt_boundary = plt.Circle((0, 0), radius_arena, color='b', fill=False)
            axis = plt.gca()
            axis.add_artist(plt_boundary)
        plt.axis([-5, 5, -5, 5])
        plt.show()

    
    ############### Iterate over all timesteps in the data
    for timestep in range(timestep_start, end_timestep):
        
        # If the behavior is follow, we fast-forward until we find a vehicle position in the goal_xys array
        # where the other positions are stored
        if goal_xys[timestep] == None:
            timestep += 1
            if timestep > end_timestep:
                break
            continue

        current_xy_own, heading_own = get_state(own_xy, timestep, 4)  # smooth heading over 3 timesteps in the future
        
        # A number of checks are performed to make sure the goal is clear of vehicles,
        # and not planned within the boundary. If behavior is follow, now dynamic goal is used,
        # which tries to avoid other vehicles
        goal_xy = get_goal_position(goal_xys, own_xy, other_xys, timestep, act_behavior == behavior.follow)
        
        if close_to_boundary(current_xy_own, radius_arena, allowed_own_distance):
            new_trajectory, new_deltas, safe_path = get_center_trajectory(own_xy, other_xys, timestep, trajectory_length)   
            resulting_deltas.append(new_deltas)         
            resulting_trajectories.append(new_trajectory)
            resulting_motor_cmds.append(get_slowdown_cmd(trajectory_length))
            color = 'r'
        else:
            new_trajectory, new_motor_cmds, new_deltas, safe_path = get_trajectory_to_goal(own_xy, other_xys, timestep, heading_own, 0.0, goal_xy, desired_speed, ideal_distance, min_distance_to_goal, trajectory_length)
            resulting_deltas.append(new_deltas)    
            resulting_trajectories.append(new_trajectory)
            resulting_motor_cmds.append(new_motor_cmds)
            color = 'b'
            
        
        if plot_graphics:
            lines = plt.plot(new_trajectory[0], new_trajectory[1], color)
            vehicle = plt.plot(current_xy_own[0], current_xy_own[1], 'bo')
            goal = plt.plot(goal_xy[0], goal_xy[1], 'go')
            obstacle_plot = []
            plt_safe_path_points = []
            if safe_path != None:
                for node in safe_path:
                    plt_safe_path_points.append(node._point)
            
            plt_safe_path_points = np.transpose(plt_safe_path_points)
            
            if safe_path != None:
                plt_safe_path = plt.scatter(plt_safe_path_points[0],plt_safe_path_points[1])
            
            for other in other_xys:
                obstacle_plot.append(plt.plot(other[timestep][0], other[timestep][1], 'ro'))
                
            plt.pause(0.0001)
            plt.show()
            
            for other_plot in obstacle_plot:
                other_plot.pop(0).remove()
            lines.pop(0).remove()
            if safe_path != None:
                plt_safe_path.remove()
            vehicle.pop(0).remove()
            goal.pop(0).remove()
        
    # steering_angles = convert_path_to_steeering_angles(resulting_trajectories)
    steering_angles = resulting_deltas
    motor_commands = convert_to_motor(resulting_motor_cmds)
    
    return steering_angles, motor_commands, resulting_trajectories


    
