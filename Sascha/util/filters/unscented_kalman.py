import numpy as np
import os
import sys
from os.path import expanduser
import time
import pylab as pl
from kzpy3.Sascha.util.filters.third_party.pykalman.pykalman import UnscentedKalmanFilter
from kzpy3.data_analysis.trajectory_generator.beacon_navigator.dynamic_model import getXYFor
from kzpy3.data_analysis.trajectory_generator import trajectory_tools
'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''



class Unscented_Kalman_Filter():

    min_speed_for_heading_calc = 0.1
    recent_positions = []
    recent_pos_length = 10
    speed = None
    heading = None

    def __init__(self, number_of_observations = 10):
        self.number_of_observations = number_of_observations
       
        self.transition_covariance = np.eye(2)
        self.random_state = np.random.RandomState(0)
        self.observation_covariance = np.eye(2) + self.random_state.randn(2, 2) * 0.1
        self.initial_state_mean = [0, 0]
        self.initial_state_covariance = [[1, 0.1], [-0.1, 1]]
        
        # draw estimates
        #pl.figure()
        #lines_true = pl.plot(states, color='b')
        #lines_filt = pl.plot(filtered_state_estimates, color='r', ls='-')
        #lines_smooth = pl.plot(smoothed_state_estimates, color='g', ls='-.')
        #pl.legend((lines_true[0], lines_filt[0], lines_smooth[0]),
        #          ('true', 'filt', 'smooth'),
        #          loc='lower left'
        #)
        #pl.show()
        

    old_time = time.time()
    poll_time_difference = 0.0
    
    kf = None
    
    def detect_hz(self):        
        self.poll_time_difference = time.time()-self.old_time
        
    
    def get_xy_position(self, position_xy, heading, steering_angle):
        
        # Outside speed without encoder is unknown
        # so it will be calculated from difference in pos
        
        # Outside heading is ignored right now
        self.detect_hz()
        self.set_own_pos(position_xy)
        self.steering = steering_angle
        
        if self.heading:
            if not self.kf:
                # sample from model
                self.kf = UnscentedKalmanFilter(
                    self.transition_function, self.observation_function,
                    self.transition_covariance, self.observation_covariance,
                    self.initial_state_mean, self.initial_state_covariance,
                    random_state=self.random_state
                )
                
                
            states, observations = self.kf.sample(1, self.initial_state_mean)
        
            # estimate state with filtering and smoothing
            filtered_state_estimates = self.kf.filter(observations)[0]
            smoothed_state_estimates = self.kf.smooth(observations)[0]
            
            return (smoothed_state_estimates[:, 0][-1],smoothed_state_estimates[:,0][-1])
        
        else:
            print "Not enough information to get heading"
            
        
    
    # initialize parameters
    def transition_function(self, state, noise):
        
        # That can be changed in the future
        a = 0.0
        
        x_0 = state[0]
        y_0 = state[1]
        
        v = self.speed
        delta = self.steering
        
        x_new, y_new, v, psi = getXYFor(x_0, y_0, 0.0, v, self.heading, self.poll_time_difference, a, delta)
        
        #a = np.sin(state[0]) + state[1] * noise[0]
        #b = state[1] + noise[1]
        return np.array([x_new, y_new])
    
    def observation_function(self,state, noise):
        
        x = self.recent_positions[-1][0]+noise[0]
        y = self.recent_positions[-1][1]+noise[1]
        
        return np.array([x,y])

    def set_own_pos(self,own_pos):
        '''
        Will actualize the current pos and also update speed and heading
        '''
        
        self.own_pos = own_pos

        # Speed calculation        
        if len(self.recent_positions) > 0:
            
            x = own_pos[0]
            y = own_pos[0]
    
            x_old = self.recent_positions[-1][0]
            y_old = self.recent_positions[-1][1]

            # v = s / t
            self.speed = np.hypot(x - x_old,y - y_old) / self.poll_time_difference
            
        if len(self.recent_positions) > self.recent_pos_length:
            self.recent_positions.pop(0)
        self.recent_positions.append(own_pos)
                

        if not self.speed:
            self.speed = 0.0
        
        # If the list of recent positions is full
        if len(self.recent_positions) >= self.recent_pos_length:
            
            if self.speed > self.min_speed_for_heading_calc:
    
                # Calculate heading according to the changes in the position
                pos_heading = trajectory_tools.get_heading(self.recent_positions)
                # Calculate the heading correction term according to that heading
                self.heading = pos_heading
                
    

if __name__ == "__main__":
    filter = Unscented_Kalman_Filter()
    
    