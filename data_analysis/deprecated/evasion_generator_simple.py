'''
Created on May 8, 2017

@author: Sascha Hornauer
'''
from omgtools import *
from kzpy3.data_analysis.trajectory_generator.trajectory_tools import *
import cv2
import sys
import matplotlib.pyplot as plt
from omgtools.problems.point2point import FreeEndPoint2point
from operator import add
import copy
import time
from timeit import default_timer as timer

framerate = 1. / 30.



def get_state(own_xy, timestep_start, timestep_end):

    # Init our own position
    init_xy = own_xy[timestep_start]
         
    # Get our intended heading based on three timesteps in the future
    # which add as slight smoothing
    heading = get_heading(own_xy[timestep_start:timestep_start + timestep_end])
    # Get the velocity over the first two timesteps
    velocity = get_velocities([own_xy[timestep_start], own_xy[timestep_start + 1]], framerate)
    return init_xy, heading, velocity

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
            pos_diffs = get_pos_diff(np.transpose(trajectory))
            
            for pos_diff in pos_diffs:
                trajectory_angles.append(np.arctan2(pos_diff[1], pos_diff[0]))
            
            trajectories.append(trajectory_angles)
        else:
            # If the trajectory contains angles, add it as it is
            trajectories.append(trajectory)
    return trajectories


def get_emergency_trajectories(obstacle_pos, current_xy_own, number):
    
    angle_of_obstacle = np.arctan2(obstacle_pos[1] - current_xy_own[1], obstacle_pos[0] - current_xy_own[0])
      
    if angle_of_obstacle > 0:
        return np.ones(number) * -np.pi / 2.
    else:
        return np.ones(number) * np.pi / 2.

    


def get_center_trajectory(heading,current_xy_own, trajectory_length):
    
    x,y =  cv2.polarToCart(1.0,heading)
    
    angle_towards_center =  np.arctan2(-current_xy_own[1]-y[0],-current_xy_own[0]-x[0])
    
    if angle_towards_center < 0:
        return np.ones(trajectory_length) * -np.pi / 2.
    else:
        return np.ones(trajectory_length) * np.pi / 2.

    



def get_center_circle_points(own_xys):
    
    goalxys = []
    goal_offset = -(np.pi/8.0)
    circle_radius = 3 # m
    
    # calculate positions on a circle near the center
    for pos in own_xys:
        own_x = pos[0]
        own_y = pos[1]
            
        # Get a point on the circle
        distance_goalpoint = circle_radius
        
        # Now take the distance to the goalpoint in combination with the angle to the 
        # goalpoint to make out the intersection of the straight line in between the
        # car and that circle
        angle_center = np.arctan2(own_y,own_x)
        
        # Change the angle to be in front of the vehicle like the carrot on a stick
        angle_goalpoint = angle_center + goal_offset
        
        # Next calculate that new point
        goal_xy = cv2.polarToCart(distance_goalpoint,angle_goalpoint)
        goal_xy = [goal_xy[0][0][0],goal_xy[1][0][0]]
        
        # If the distance of that new goalpoint is too far from our position
        
        goalxys.append(goal_xy)
        
    return goalxys
    
    


def get_straight_line(current_xy_own, goal_xy):
    # We observe the goal and our own position
    own_x = current_xy_own[0]
    own_y = current_xy_own[1]
    goal_x = goal_xy[0]
    goal_y = goal_xy[1]
    
    # Then we create the straight line path towards our goal
    traj_x = np.linspace(own_x, goal_x, 30)
    traj_y = np.linspace(own_y, goal_y, 30)
    
    






    return [traj_x,traj_y]
    

def get_evasive_trajectory(own_xy, other_xy, timestep_start, d_timestep_goal, plot_video, end_timestep):
    '''
    Returns a short term evasion trajectory, in steering commands for 
    as many timesteps ahead as given in between timestep_start and timestep_ahead.
    Note that the trajectory will start one timestep further than timestep_start because
    one timestep is needed to retrieve information about the start conditions
     
    FOR NOW, OTHER_XY IS ONLY ONE OTHER VEHICLE    
    '''
    safety_distance = 0.2
    allowed_goal_distance = 0.2
    allowed_own_distance = 1.0
    obstacle_segment_factor = int(2999 / 10)  # This factor should be made dependent on the length of the dataset
    no_datapoints = len(own_xy)
    framerate = (1. / 30.)
    diameter_arena = 4.28
    sample_time = 1. / 4.
    update_time = 1. / 4.
    goal_offset_limit = 150
    goal_ideal_distance = 50
    trajectory_length = 30
    resulting_trajectories = []
    simulate = True
    goal_xys = get_center_circle_points(own_xy)
    
    
    # For each obstacle in the obstacle trajectory list we create segments from
    # the trajectories to improve computability.

    environment = Environment(room={'shape': RegularPolyhedron(diameter_arena, 24), 'draw': False})
    test_obstacle_pos = []
    for i in range(0, len(other_xy)):
        
        obstacle_xy = other_xy[i]
        # For each obstacle, get its segments
        samplepoints = np.linspace(timestep_start, no_datapoints - 1, num=obstacle_segment_factor, dtype=np.int32)
        
        segments_trajectory = np.array(obstacle_xy)[samplepoints]

        # Calculate start and end time of the segment 
        #obstacle_start_times = np.linspace(timestep_start, framerate * no_datapoints, num=obstacle_segment_factor)
        # obstacle_end_times = obstacle_start_times[1:]
        # obstacle_start_times = obstacle_start_times[:len(obstacle_start_times)-1]
        
        test_obstacle_pos.append(np.array(obstacle_xy))
        #offset_diffs = get_pos_diff(segments_trajectory)

        # Create a trajectory for that obstacle
        #traj = ({'position': {'time':obstacle_start_times, 'values': offset_diffs}})

        # add it to the environment
        # environment.add_obstacle(Obstacle({'position': segments_trajectory[0]}, shape=Circle(0.25),
        #    simulation={'trajectories': traj}))
        environment.add_obstacle(Obstacle({'position': segments_trajectory[0]}, shape=Circle(0.2)))
    
    vehicle = Holonomic(shapes=Circle(0.2),options={'plot_type': 'car'}) 
    
    init_xy_own = own_xy[timestep_start] 
    #goal_xy = own_xy[timestep_start + d_timestep_goal] 
    goal_xy = goal_xys[timestep_start + d_timestep_goal]

    # Plan from the initial position
    vehicle.set_initial_conditions(state=[init_xy_own[0], init_xy_own[1]])  
    vehicle.set_terminal_conditions([goal_xy[0], goal_xy[1]])
    vehicle.set_options({'safety_distance': safety_distance})
    
    # Create a point-to-point problem
    problem = Point2point(vehicle, environment, freeT=False)
    
    problem.set_options({'solver_options':
    {'ipopt': {'ipopt.hessian_approximation': 'limited-memory'}}})
    
    
    problem.init()
    
    # simulate, plot some signals and save a movie
    simulator = Simulator(problem, sample_time=sample_time, update_time=update_time)
    if plot_video:
        problem.plot('scene')
    
    for timestep in range(timestep_start, end_timestep):
    #for timestep in range(timestep_start, timestep_start + 10):
                   

        for i in range(0, len(simulator.problem.environment.obstacles)):
            obstacle = simulator.problem.environment.obstacles[i]
            obstacle.set_state({'position':test_obstacle_pos[i][timestep], 'velocity':[0., 0.], 'acceleration':[0., 0.]})
              
        if plot_video:
            problem.update_plot('scene', 0)
            #circle2 = plt.Circle((0,0), diameter_arena, color='b', fill=False)
            #plt.scatter(goal_xy[0],goal_xy[1])
            #straight_line = get_straight_line(own_xy[timestep],goal_xy)
            #plt.scatter(straight_line[0],straight_line[1])
            #print goal_xy
            #axis = plt.gca()
            #axis.set_xlim((-5, 5))
            #axis.set_ylim((-5, 5))
            #axis.add_artist(circle2)
            #plt.savefig("scene" + "_" + str(timestep) + ".png")
            
        
        if timestep > timestep_start + 1:
            
            current_xy_own = own_xy[timestep]
            
            # The goal is in front on the observed trajectory, further in time.
            # If it is to far than a certain value, keep it at that value
            if d_timestep_goal > goal_offset_limit:
                d_timestep_goal = goal_offset_limit            
            
            # If the end of the trajectory is reached, the endpoint will 'wait' at the last timestamp 
            if timestep + d_timestep_goal >= len(own_xy):
                d_timestep_goal = len(own_xy) - timestep 
            
            # Every time we try to get the goal distance towards the ideal goal distance
            # when it quite far in front without reasons
            if d_timestep_goal > goal_ideal_distance:
                d_timestep_goal -= 1
            try:
                goal_xy = goal_xys[timestep + d_timestep_goal]
            except IndexError:
                goal_xy = goal_xys[len(own_xy) - 1]
                print "IndexError: " + str(timestep + d_timestep_goal)
                
            continue_outer_loop = False
            # Check if obstacle is too close to the goal or to the vehicle
            while True:
                goal_near_obstacle = False 
                vehicle_near_obstacle = False
                
                for obstacle in simulator.problem.environment.obstacles:
                    obstacle_pos = (obstacle.signals['position'][0][-1], obstacle.signals['position'][1][-1])
                
                    goal_near_obstacle = goal_near_obstacle or distance_2d(obstacle_pos, goal_xy) < allowed_goal_distance
                    vehicle_near_obstacle = vehicle_near_obstacle or distance_2d(current_xy_own, obstacle_pos) < allowed_own_distance
                    
                # If we are far away from an obstacle, continue
                if not goal_near_obstacle and not vehicle_near_obstacle:
                    break
                
                if goal_near_obstacle:
                    # Look for a new goal along the trajectory
                    # TODO. Handle end of trajectory here
                    d_timestep_goal += 10 
                    goal_xy = goal_xys[timestep + d_timestep_goal]
                    
                if vehicle_near_obstacle:
                    # Skip a number of simulation runs, create emergency
                    # trajectories and check again
                    resulting_trajectories.append(get_emergency_trajectories(obstacle_pos, current_xy_own, trajectory_length))
                    
                    timestep += 1
                    simulator.deployer.reset()
                    # self.current_time, self.update_time, self.sample_time)
                    # simulation_time, sample_tim
                    # print simulator.current_time
                    
                    # simulator.problem.environment.simulate(update_time,sample_time)
                    print "Skipping timestamp " + str(timestep)
                    continue_outer_loop = True  # Guido the great has spoken there shall be no continuation to the outer loop in this language. I don't like python. :(
                
                if goal_near_obstacle or vehicle_near_obstacle:
                    break
                
            if continue_outer_loop:
                continue
                        
            # Check if goal is too close to the boundary or rather if the distance to
            # the center is too large
            while (distance_2d(goal_xy, [0.0, 0.0]) > (diameter_arena - allowed_goal_distance)):
                # Otherwise, look for a new goal along the trajectory
                d_timestep_goal += 10
                if timestep + d_timestep_goal > no_datapoints:
                    # The goal at the end of the trajectory is outside the boundary. 
                    # This can not be avoided by looking further in the future
                    goal_xy = goal_xys[no_datapoints - 1]
                    print "Goal at end of trajectory"
                    break;
                else:
                    goal_xy = goal_xys[timestep + d_timestep_goal]                
                
                # todo change allowed_goal distance to allowed vehicle distance
            
            continue_outer_loop = False
            if (distance_2d(current_xy_own, [0.0, 0.0]) > (diameter_arena - allowed_goal_distance)):
                # Skip a number of simulation runs, create emergency
                # trajectories and check again
                # Try to get the heading. Use try and except for the beginning and end of own_Xy
                try:
                    heading = get_heading(own_xy[timestep:timestep+3])
                except:
                    try:
                        heading = get_heading(own_xy[timestep-3:timestep])
                    except:
                        heading = 0.0 
                        
                resulting_trajectories.append(get_center_trajectory(heading, current_xy_own,trajectory_length))
                
                timestep += 1
                simulator.deployer.reset()
                print "Skipping timestamp " + str(timestep)
                continue_outer_loop = True  # Guido the great has spoken there shall be no continuation to the outer loop in this language. I don't like python. :(
            
            if continue_outer_loop:
                continue
            try:    
                simulator.problem.vehicles[0].overrule_state(current_xy_own)
                vehicle.set_terminal_conditions([goal_xy[0], goal_xy[1]])
            except AttributeError:
                pass
            
        
        if simulate:
            simulator.update()
    
            simulator.update_timing()
            #output = get_straight_line(own_xy[timestep],goal_xy)
            
            #plt.scatter(output[0],output[1])
            
            
            # return trajectories and signals
            trajectories, signals = {}, {}
            for vehicle in simulator.problem.vehicles:
                trajectories[str(vehicle)] = vehicle.traj_storage
                signals[str(vehicle)] = vehicle.signals
                
                # Calculate the resulting trajectory and sample it to 30 values
                trajectory_xs = trajectories[str(vehicle)]['pose'][-1][0]
                trajectory_ys = trajectories[str(vehicle)]['pose'][-1][1]
                
                trajectory_30_x = sample_values(trajectory_xs, trajectory_length)
                trajectory_30_y = sample_values(trajectory_ys, trajectory_length)
            
                resulting_trajectories.append((trajectory_30_x, trajectory_30_y))
        else:
            # Calculate the resulting trajectory and sample it to 30 values
            
            resulting_trajectories.append(get_straight_line(own_xy[timestep],goal_xy))
        
        
    
    return convert_path_to_steeering_angles(resulting_trajectories)


    