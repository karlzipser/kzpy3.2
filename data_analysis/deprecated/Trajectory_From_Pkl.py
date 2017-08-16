'''
Created on May 10, 2017

@author: Sascha Hornauer
'''
import os
import cPickle as pickle
import numpy as np
from operator import add, div
from trajectory_generator import collision_scanner
from trajectory_generator import evasion_generator_bicycle as evasion_generator
from aruco_tools.mode import *
from trajectory_generator.trajectory_tools import *
import sys

import copy
from timeit import default_timer as timer



class Trajectory_From_Pkl:
    fake_more_entries = False
    calculation_horizon = 20  # timesteps
    
    timestep_offset = 0
    # adding furtive and play later TODO FIXIT
    trajectories = {}
    
    
    def __init__(self, pkl_filename, start_timestamp, end_timestep, modes_selected, show_graphics):
        
        print "Calculating trajectories ..."
        actual_trajectories = self.process_pkl_file(pkl_filename, start_timestamp, end_timestep)
       
        start = timer()
        start_timestep = self.timestep_offset
        end_timestep = len(actual_trajectories.itervalues().next()['timestamps'])
        
        
        resulting_trajectories = self.get_trajectory(actual_trajectories, show_graphics, int(start_timestep), int(end_timestep), modes_selected)
        
        end = timer()
        print ("Finished in " + str(end - start) + " seconds.")
        self.trajectories = resulting_trajectories
         
                
    
    def process_pkl_file(self, pkl_file, start_timestamp, end_timestamp):
        
        pickle_file = pickle.load(open(pkl_file, "rb"))
        
        timestamps = np.arange(start_timestamp, end_timestamp, 1 / 30.)
                
        actual_trajectories = {}
        
        # Enter here the carnames which should be considered
        for car in ['Mr_Black', 'Mr_Blue']:
            
            car_left_x = [pickle_file[car]['left'][0](timestamps)]
            car_right_x = [pickle_file[car]['right'][0](timestamps)]
            car_left_y = [pickle_file[car]['left'][1](timestamps)]
            car_right_y = [pickle_file[car]['right'][1](timestamps)]
            car_x, car_y = self.get_average_position(car_left_x, car_left_y, car_right_x, car_right_y)
        
            actual_trajectories[car] = {'timestamps':timestamps, 'position': (car_x, car_y)}
        
        return actual_trajectories


    def get_continous_segments(self, encounter_situations):
        
        # We go through the list of encounter situations and allow
        # for a certain gap where the other car is not visible
        segments = []
        
        allowed_gap = 3
        segment_counter = 0
        inner_segment_list = []
        
        for i in range(0, len(encounter_situations)):
            
            if i == len(encounter_situations) - 1:
                if inner_segment_list:
                    segments.append(inner_segment_list)
                break
            else:
                # There is a gap in between sightings
                if encounter_situations[i + 1] - encounter_situations[i] > 1: 
                    if encounter_situations[i + 1] - encounter_situations[i] > allowed_gap:
                        # The gap is too big, we start a new inner segment
                        # add the last of the old segment
                        inner_segment_list.append(encounter_situations[i])
                        # append that list
                        segments.append(inner_segment_list)
                        # increase counter
                        segment_counter += 1
                        # reset inner list
                        inner_segment_list = []
                        continue
                    else:
                        # we interpolate the numbers in between
                        inner_segment_list.extend(range(encounter_situations[i], encounter_situations[i + 1]))
                        segments.append(inner_segment_list)
                else:
                    inner_segment_list.append(encounter_situations[i])
                
            
        
        return segments
    
    def get_trajectory(self, actual_trajectories, plot_video, start_timestep, end_timestep, modes_selected):
        self.timestep_offset = start_timestep
        evasion_trajectory_data = {}
        
        # For all cars in actual trajectories
        for car in actual_trajectories:
            print "Calculating trajectories for " + str(car)
            # Add all other trajectories into a list
            other_trajectories = actual_trajectories.copy()
            del other_trajectories[car]
            
            # Create a list containing all other trajectories
            other_positions = []
            # As long as there is only one other car we fake second one by taking its trajectory 
            # and turning it around
            
            if self.fake_more_entries:
                first_trajectory_in_dict = other_trajectories.itervalues().next()
                fake_timestamps = first_trajectory_in_dict['timestamps']
                fake_positions = first_trajectory_in_dict['position'][::-1]
                 
                fake_trajectory = {'timestamps':fake_timestamps, 'position':fake_positions}
                other_trajectories['Mr_Fake'] = fake_trajectory
                 
            for other_cars in other_trajectories:
                other_positions.append(zip(other_trajectories[other_cars]['position'][0][0], other_trajectories[other_cars]['position'][1][0]))
                
            # Now calculate the evasive trajectory for the car
            own_trajectories = actual_trajectories[car]
            
            resulting_trajectories = {}
            
            # Get the short term trajectory
            own_trajectory = own_trajectories['position']
      
            own_x = (own_trajectory[0][0])
            own_y = (own_trajectory[1][0])
            own_xy = zip(own_x, own_y)
                    
            for act_mode in modes_selected:
                
                if act_mode == behavior.circle:
                    goal_xys = evasion_generator.get_center_circle_points(own_xy)
                                                                             
                    trajectories_in_delta_angles, motor_cmds, path_data = evasion_generator.get_batch_trajectories(own_xy, other_positions, self.timestep_offset, plot_video, end_timestep, goal_xys, act_mode)
                    resulting_trajectories = convert_delta_to_steer(trajectories_in_delta_angles)
                    timestamps = actual_trajectories[car]['timestamps']
                    evasion_trajectory_data[(car, act_mode)] = {'timestamps':timestamps, 'trajectories':resulting_trajectories, 'motor_cmds':motor_cmds, 'pos':own_xy, 'path':path_data}
                 
                elif act_mode == behavior.follow:
                    
                    # First find all the points in the dataset where another car is actually close
                    
                    encounter_timestep, closest_xys, _ = collision_scanner.get_close_encounters_in_list(own_xy, other_positions, start_timestep, end_timestep)
                    
                    time_segments = self.get_continous_segments(encounter_timestep)
                    # Add those points to the goal trajectory. 
                    print time_segments
                    goal_xys = [None] * (time_segments[-1][-1] + 1)
                    
                    i = 0
                    for time_segment in time_segments:
                        old_timepoint = time_segments[0]
                        for timepoint in time_segment:
                            if timepoint not in closest_xys.keys():
                                # The other vehicle is temporarily not visible. we assume the old position
                                goal_xys[timepoint] = goal_xys[old_timepoint]
                            else:
                                goal_xys[timepoint] = points_to_list(closest_xys[timepoint])
                                old_timepoint = timepoint
                            i += 1
                    
                    evasion_segment_data = []
                    for segment in time_segments:

                        start_time = segment[0]
                        end_time = segment[len(segment) - 1]
                        if start_time == end_time:
                            continue
                        try:
                            trajectories_in_delta_angles, motor_cmds, path_data = evasion_generator.get_batch_trajectories(own_xy, other_positions, self.timestep_offset, plot_video, end_timestep, goal_xys, act_mode)
                            resulting_trajectories = convert_delta_to_steer(trajectories_in_delta_angles)
                            timestamps = actual_trajectories[car]['timestamps']
                            evasion_segment_data.append({'mode':act_mode, 'timestamps':timestamps[start_time:end_time], 'trajectories':resulting_trajectories, 'motor_cmds':motor_cmds, 'pos':own_xy, 'path':path_data})
                        except IndexError as ix:
                            print "IndexError, end of timesteps reached"
                            break

                    evasion_trajectory_data[(car, act_mode)] = evasion_segment_data
                
        
        return evasion_trajectory_data
        
    
    
    def get_average_position(self, left_x, left_y, right_x, right_y):
        '''
        Returns 
        '''
        return np.array(map(add, left_x, right_x)) / 2., np.array(map(add, left_y, right_y)) / 2.
    
    
def get_trajectories(pkl_filename, start_timestamp, end_timestep, modes_selected, show_graphics): 
    trajectory_parser = Trajectory_From_Pkl(pkl_filename, start_timestamp, end_timestep, modes_selected, show_graphics)
    resulting_trajectories = trajectory_parser.trajectories
    
    return resulting_trajectories
    
if __name__ == '__main__':
    pass
    
    
    

    
    
