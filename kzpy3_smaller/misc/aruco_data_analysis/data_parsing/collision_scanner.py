'''
Created on May 8, 2017

@author: picard
'''
from trajectory_generator.trajectory_tools import *
import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from collections import defaultdict
import sys
from timeit import default_timer as timer
from cv_bridge import CvBridge, CvBridgeError
import rosbag
from tensorflow.contrib.learn.python.learn.graph_actions import run_n
from kzpy3.data_analysis.data_parsing.Image_Bagfile_Handler import Image_Bagfile_Handler
import angles


distance = 8  # m
fov_angle = 66.0  # deg
smooth_heading_over_timesteps = 30 

class MyIter():
    
    _iterator = None
    _current_value = None
    
    def __init__(self, iterable_object):
        self._iterator = iter(iterable_object)
        self._current_value = self._iterator.next() 
        
    def next(self):
        tmp = self._current_value
        try:
            self._current_value = self._iterator.next()
        except StopIteration:
            self._current_value = None
            return None
        return tmp
    
    def peek(self):
        return self._current_value




gyro_corr_x = 0.0


def convert_encoder(encoder_list):
    
    encoder_values = {}
    
    for encoder_value in encoder_list:
        encoder_values[encoder_value['timestamp']]=encoder_value['encoder']

    return encoder_values

def convert_gyro(gyro_list):
    
    gyro_values = {}
    
    for gyro_value in gyro_list:
        gyro_values[gyro_value['timestamp']]=gyro_value['gyro_xyz']

    return gyro_values


def align_dict(dict_values, timestamps):
    '''
    Alignes the entries in the dict, which should be indexed by timestamps
    to fit to the given list of timestamps. It is right now expected
    that the dict_values are less than the nr. of timestamps and dict_values
    have to be spread to fit this
    '''
    aligned_values = {}
    
    sorted_dict_keys = sorted(dict_values.keys())
    sorted_values = [dict_values[key] for key in sorted(dict_values)]
    
    current_dict_value = sorted_values[0]
    current_dict_key = sorted_dict_keys[0]
    
    progress_checker = 0
    
    sorted_timestamps = sorted(timestamps)
    
    for item_timestamp in sorted_timestamps:
        progress_checker += 1
        
        # The -1 is used to signify the end of the current_dict_key list. Not
        # the best way to solve this, I have to admit
        if current_dict_key == -1:
            aligned_values[item_timestamp] = current_dict_value
            continue
        
        if item_timestamp == current_dict_key:
            
            aligned_values[item_timestamp] = current_dict_value
            
            sorted_values.pop(0)
            sorted_dict_keys.pop(0)
            
            if len(sorted_dict_keys) == 0:
                current_dict_key = -1
                continue
            
            current_dict_key = sorted_dict_keys[0]
            current_dict_value=sorted_values[0]
            
            #print "* Adding " + str(current_dict_value) + " at " + str(item_timestamp)
        else:
            #print "+ Adding " + str(current_dict_value) + " at " + str(item_timestamp)
            aligned_values[item_timestamp] = current_dict_value
            
        if progress_checker % 5000 == 0:
            print str(np.round(((item_timestamp-sorted_timestamps[0])*100.0)/(sorted_timestamps[-1]-sorted_timestamps[0]),2))+ "% of dict aligned"  
             
    return aligned_values



def get_heading_from_gyro(gyro_value):
    '''
    There are different ways to implement this. There is a drift of the gyro values
    and also they will be in degree and just go over 360 until infinity.
    Since right now a correction term is calculated this will not be corrected
    but only the x part of the gyro value is used and converted to rad
    '''
    x_gyro_value = gyro_value[0]
    #y_norm = gyro_xyz[1]%360.0
    #z_norm = gyro_xyz[2]%360.0
         
    return np.deg2rad(x_gyro_value)
     
    


def calculate_headings(gyro_xyz_list, encoder_list, mid_xy, timestamps):
    '''
    This method calculates a list of headings for the timestamps based on 
    either the change in position if the car is fast enough moving in a certain
    direction or based on the gyro_heading information.
    
    The moving heading is usually quite good as the car can only move into the direction
    into which it is headed, however when the car is standing or going backwards
    the information is unreliable
    
    The gyro heading information has a constant drift and changes also by a margin
    when the car at any point was flipped over. Also these information are relative to
    the first heading, meaning that once the system is started, this is where the
    gyro heading will assume 0 degree. 
    
    The gyro heading will be used in the cases where the move-heading can not be
    used, however while the move-heading is used, it will constantly calculate a 
    correction factor for the gyro information, to remove the drift.
    '''
        
    headings = []
    smooth_over_no_timesteps = 3
    
    # This is a temporary fix since the encoder values are not in a 
    # dict, index by timestamps, but in a list. It takes one hour to generate
    # the original file so this is a temporary workaround.
    encoder_values = convert_encoder(encoder_list)
    gyro_values = convert_gyro(gyro_xyz_list)
    
    # The encoder and gyro values are not received at exactly the same timestamps as
    # the xyz information because the ROS messages come just a few microseconds
    # later. Even though this is a bit of a hack,the encode timestamps will be shifted
    # slightly to align to the xyz values.
    
    # TODO: For some reason and against expectation the values are actually aligned already.
    # This might be a bug in the "pipeline_Bag_To_Trajectories" class and has to be checked.
    # Also because the dicts are not ordered there seems to be a bug
    encoder_values_aligned = align_dict(encoder_values, timestamps)
    
    gyro_values_aligned = align_dict(gyro_values,timestamps)
    gyro_correction_value = 0.0

    mid_xy_list = np.transpose(mid_xy).tolist()            
    tmp_xy_list = mid_xy_list[0:smooth_over_no_timesteps]
    mid_xy_index = smooth_over_no_timesteps
    
    # If the encoder is above 2 the speed is sufficient so the heading can be 
    # used to determine the heading and the correction term for the gyro values
    # will be fit to correct them
    for timestamp in timestamps:
        
        # Move a sliding window over the xy values
        if mid_xy_index < len(mid_xy_list):
            # Keep it fixed over the last 3 entries in the list 
            # at the end 
            tmp_xy_list.pop(0)
            tmp_xy_list.append(mid_xy_list[mid_xy_index])
            mid_xy_index += 1
        
        if encoder_values_aligned[timestamp] > 1.:
            # If the speed is sufficient use the xy values to get the heading
            # and also to correct the gyro headings
            
            current_heading = get_heading(tmp_xy_list)
            gyro_correction_value = get_heading_from_gyro(gyro_values_aligned[timestamp]) - current_heading 
            headings.append(current_heading)
            
        else:
            # If the speed is too slow we use the gyro values as heading instead
            headings.append(get_heading_from_gyro(gyro_values_aligned[timestamp]) - gyro_correction_value)
        
        
    return headings
        

class Trajectory_List():
    
    unaligned_trajectories = {}
    aligned_trajectories = {}
    
    def add_trajectory(self, car_name, trajectories_dict):
        
        # There is right now only one run name for each trajectory
        run_name = trajectories_dict[car_name].keys()[0]
        self.unaligned_trajectories[car_name] = self.get_timestamped_trajectories(car_name, run_name, trajectories_dict)
    
    def get_timestamped_trajectories(self, car_name, run_name, traj_dictionary):
        
        left_x = traj_dictionary[car_name][run_name]['self_trajectory']['left']['x']
        left_y = traj_dictionary[car_name][run_name]['self_trajectory']['left']['y']
        
        right_x = traj_dictionary[car_name][run_name]['self_trajectory']['right']['x']
        right_y = traj_dictionary[car_name][run_name]['self_trajectory']['right']['y']
        
        mid_xy = (((right_x + left_x) / 2.), ((left_y + right_y) / 2.))
        timestamps = traj_dictionary[car_name][run_name]['self_trajectory']['ts']
        
        gyro_values = traj_dictionary[car_name][run_name]['self_trajectory']['left']['gyro_xyz']
        encoder = traj_dictionary[car_name][run_name]['self_trajectory']['left']['encoder']
        
        headings = calculate_headings(gyro_values, encoder, mid_xy, timestamps)
        
        
        return zip(timestamps, zip(mid_xy[0], mid_xy[1]), headings)
    
    def align_trajectories(self):
        
        # After this step the aligned_trajectories will contain the same lists as unaligned trajectories
        # though the index and length will be the same for each (timestamp, (x,y)) entry. They will be
        # aligned so they can be handled easier in subsequent steps
        
        # Initialise the aligned list with empty lists
        for trajectory in self.unaligned_trajectories:
            self.aligned_trajectories[trajectory] = []
        
        
        timestamp_accuracy = 1 / 30.
        fringe = {}
        for trajectory in self.unaligned_trajectories:
            fringe[trajectory] = MyIter(self.unaligned_trajectories[trajectory])
        
        while True:
        
            # Find the minimum timestamp of any list
            min_timestamp = None
            finished_trajectories = 0
            
            for trajectory in fringe:
                current_trajectory = fringe[trajectory].peek()
                
                if current_trajectory == None:
                    finished_trajectories += 1
                    if finished_trajectories == len(fringe):
                        return self.aligned_trajectories
                    continue
                
                timestamp = current_trajectory[0]
                
                if min_timestamp == None:
                    min_timestamp = timestamp
                else:
                    min_timestamp = np.minimum(min_timestamp, timestamp)
        
            # Add a None to any list where the value is larger then the minimum + an allowed distance
            for trajectory in self.unaligned_trajectories:
                current_trajectory = fringe[trajectory].peek()
                if current_trajectory == None:
                    continue
                
                timestamp = current_trajectory[0]
                
                # If the timestamp of the currently viewed trajectory is bigger than the
                # minimum add an empty 'None' entry
                if (timestamp - timestamp_accuracy) > min_timestamp:
                    self.aligned_trajectories[trajectory].append(None)
                else:
                    # If the timestamp is smaller or equal append that value and iterate in that trajectory to the
                    # next entry
                    self.aligned_trajectories[trajectory].append(fringe[trajectory].next())
                    
            

class Collision_Scanner():
        
    def __init__(self):
        pass
    
    def get_fov_triangle(self, xy, heading, fov_angle, distance):
        '''
        returns the field of view as triangle, based on a sequence of
        coordinates. It will always regard the last coordinates in that list
        '''    
        limit_left = heading - np.deg2rad(fov_angle / 2.0)
        limit_right = heading + np.deg2rad(fov_angle / 2.0)
        
        a = xy  # Point a is the latest known position
        b = cv2.polarToCart(distance, limit_left)  # Point b is distance in front and half of fov to the left
        c = cv2.polarToCart(distance, limit_right)  # Point c is distance in front and half of fov to the right
        
        # Needed extraction of the values from the polarToCart method
        # and adding of a as the origin 
        b = b[0][0][0] + a[0], b[1][0][0] + a[1]
        c = c[0][0][0] + a[0], c[1][0][0] + a[1]
        
        return Triangle(to_point(a), to_point(b), to_point(c))
    
    
    
    def get_encounters(self, trajectories_dict):
        
        global distance
        global fov_angle
        
        encounters_cars_timesteps_xy = defaultdict(lambda: dict())
        for own_carname in trajectories_dict:
            for other_carname in trajectories_dict:
                if own_carname != other_carname:
                    encounters_cars_timesteps_xy[own_carname][other_carname] = []
            
        traj_list = Trajectory_List()
    
        for car_name in trajectories_dict:
            traj_list.add_trajectory(car_name, trajectories_dict)
    
        aligned_list = traj_list.align_trajectories()
        
        for own_carname in aligned_list:
            
            list_index = 0
                    
            # Search for the first position in time where the own trajectory begins
            # and iterate the other index appropriately
            while aligned_list[own_carname][list_index] == None:
                list_index += 1
                
            own_trajectory = aligned_list[own_carname]
            smooth_factor = smooth_heading_over_timesteps            
            
            while list_index < len(own_trajectory):
                
                # If the own trajectory at that position is None, that is the end or a gap
                # in the own trajectory. We skip and increase the counter
                if own_trajectory[list_index] == None:
                    list_index += 1
                    continue
                
                if len(own_trajectory) < (list_index + smooth_factor):
                    smooth_factor = len(own_trajectory) - list_index
                
                # Calculate the heading based on values in the future or past, depending
                # on whether we are close to the beginning or end of the trajectory
                local_own_xys = [own_xy[1] for own_xy in own_trajectory[list_index:list_index + smooth_factor] if own_xy != None]
                heading = own_trajectory[list_index][2]
                
                #heading = heading - np.pi/12.
                
#               heading = get_heading(local_own_xys)
#                 
#                 print heading- headingA
                own_fov = self.get_fov_triangle(local_own_xys[0], heading, fov_angle, distance)
                
                for other_carname in aligned_list:
                    if own_carname != other_carname:
                        
                        # If the other trajectory has already ended, skip
                        if len(aligned_list[other_carname]) <= list_index:
                            continue
                        
                        other_xy = aligned_list[other_carname][list_index]
                        
                        # If other_xy is None then there is no other trajectory recorded at that point in time
                        if other_xy == None:
                            continue
                        
                        if own_fov.isInside(Point(other_xy[1][0], other_xy[1][1])):
                            encounters_cars_timesteps_xy[own_carname][other_carname].append({'run_name':trajectories_dict[own_carname].keys()[0],'fov':own_fov,'timestamp':own_trajectory[list_index][0],'own_xy':own_trajectory[list_index][1],'other_ts_xy':other_xy})
    
                list_index += 1
                
        return encounters_cars_timesteps_xy
    

def show_video_image(timestamp,run_name):
    
    # Use Image Bagfile Handler
    # Change so a certain timestep can be given and the bagfile is automatically opened, searched and displayed
    
    pass

def onClick(event):
    global pause
    pause ^= True
    
    
def draw_content(plot,i):
    fov_a = own_fov[i].a
    fov_b = own_fov[i].b
    fov_c = own_fov[i].c            
    show_video_image(timestamps[i],run_names[i])
    fov_plot_a = plot.plot([fov_a.x,fov_b.x], [fov_a.y,fov_b.y],'g-')
    fov_plot_b = plot.plot([fov_b.x,fov_c.x], [fov_b.y,fov_c.y],'g-')
    fov_plot_c = plot.plot([fov_c.x,fov_a.x], [fov_c.y,fov_a.y],'g-')
    old_pos_own = plot.plot(own_xy[i][0], own_xy[i][1],'ro')
    old_pos_other = plot.plot(other_xy[i][0], other_xy[i][1],'bo')
    #current_figure = plot.gcf()
    text = plot.text(-2, -3, timestamps[i], fontsize=10)
    plot.show()
    plot.pause(1/30.)
    old_pos_own.pop(0).remove()
    old_pos_other.pop(0).remove()
    fov_plot_a.pop(0).remove()
    fov_plot_b.pop(0).remove()
    fov_plot_c.pop(0).remove()
    text.remove()

    
    
def visualise(encounter_situations):
    
    plt.figure('top', figsize=(6, 6))
    
    own_xy = []
    other_xy = []
    own_fov = []
    timestamps = []
    run_names = []
    
    for own_carname in encounter_situations:
        for other_carname in encounter_situations[own_carname]:
            for entry in encounter_situations[own_carname][other_carname]:
                timestamps.append(entry['timestamp'])
                own_xy.append(entry['own_xy'])
                other_xy.append(entry['other_ts_xy'][1])
                own_fov.append(entry['fov'])
                run_names.append(entry['run_name'])

    
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.ion()
    fig = plt.gcf()
    fig.canvas.mpl_connect('button_press_event', onClick)
    for i in range(len(other_xy)):
        if not pause:
            draw_content(plt,i)
        else:
            while pause:
                draw_content(plt,i)


pause = False

if __name__ == '__main__':
    
    trajectories_path = sys.argv[1]
    print "Opening trajectories file " + str(trajectories_path)
    trajectories_dict = pickle.load(open(trajectories_path, "rb"))
    
    
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-23-52_1.bag'
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-24-14_2.bag'
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-28-10_10.bag'
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-28-38_11.bag'
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/bair_car_2017-04-28-17-29-10_12.bag'
    
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-28-19_10.bag'
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-28-49_11.bag'
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/bair_car_2017-04-28-17-29-18_12.bag'
    bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/new/direct_rewrite_test_28Apr17_17h23m15s_Mr_Black/'
    
    #bagfile_path = '/home/picard/2ndDisk/carData/run_28apr/direct_rewrite_test_28Apr17_17h23m10s_Mr_Blue/'
    bagfiles =  [os.path.join(bagfile_path,file) for file in os.listdir(bagfile_path) if os.path.isfile(os.path.join(bagfile_path,file))] 
    
    # Timestamps from the last car are taken. In the future it would be good to check
    # if the timestamps differ for different cars
    
    col_scanner = Collision_Scanner()
    encounter_situations = col_scanner.get_encounters(trajectories_dict)
    
    animate = True
    
    if animate:   
        plt.ion()
        
    skip_no_bagfiles = 0
    i = 0
    
    for bagfile in bagfiles:
        i += 1
        if i < skip_no_bagfiles:
            continue
        bag_handler = Image_Bagfile_Handler(bagfile)
        print "Loading bagfiles"

        timestamps = []
        run_names = []
        
    #     for own_carname in encounter_situations:
    
        own_xy = {}
        other_xy = {}
        own_fov = {}
        
        # TODO: Get this for all cars
        own_carname = 'Mr_Black'
        #for other_carname in encounter_situations[own_carname]:
        other_carname = 'Mr_Blue'
        for entry in encounter_situations[own_carname][other_carname]:
            timestamps.append(entry['timestamp'])
            own_xy[entry['timestamp']] = entry['own_xy']
            other_xy[entry['timestamp']] = entry['other_ts_xy'][1]
            own_fov[entry['timestamp']] = entry['fov']
            run_names.append(entry['run_name'])
        try:
            for timestamp in timestamps:
                
                cv_image, timestamp, synced = bag_handler.get_image(timestamp)
                if not synced:
                    continue
                if(cv_image == None):
                    continue
                cv2.imshow('frame', cv_image)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                
                
                if animate:   
                    delete_forms = []
                    delete_forms.append(plt.scatter(own_xy[timestamp][0],own_xy[timestamp][1],color='red'))
                    delete_forms.append(plt.scatter(other_xy[timestamp][0],other_xy[timestamp][1],color='blue'))
                    
                    triangle = own_fov[timestamp]
                    p1 = triangle.a
                    p2 = triangle.b
                    p3 = triangle.c
                    
                    delete_forms.append(plt.plot([p1.x, p2.x], [p1.y, p2.y], 'k-'))
                    delete_forms.append(plt.plot([p2.x, p3.x], [p2.y, p3.y], 'k-'))
                    delete_forms.append(plt.plot([p3.x, p1.x], [p3.y, p1.y], 'k-'))

                    delete_forms.append(plt.scatter(other_xy[timestamp][0],other_xy[timestamp][1],color='blue'))
                    
                    plt.pause(0.00001)
                    
                    for form in delete_forms:
                        try:
                            form.pop(0).remove()
                        except:
                            form.remove()
                
                
                
              
                
                        
                    
        except StopIteration:
            continue