'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''

import numpy as np
import os
import sys
from os.path import expanduser
import time
from kzpy3.Sascha.util.filters.third_party.pykalman.pykalman import KalmanFilter
import pylab as plt

class Simple_Kalman_Estimator():

    trans_matrix = np.array([[1,1], [0,1]])

    kf_x = KalmanFilter(transition_matrices=trans_matrix,
                  transition_covariance=0.1 * np.eye(2))
    kf_y = KalmanFilter(transition_matrices=trans_matrix,
                  transition_covariance=0.1 * np.eye(2))
    observations_x = []
    observations_y = []
    
    def __init__(self, number_of_observations = 10):
        self.number_of_observations = number_of_observations

    def get_xy_position(self, position_xy, heading, steering_angle):
        
        self.observations_x = np.append(self.observations_x, position_xy[0])
        
        if len(self.observations_x) == 1:
            return position_xy
            
        if len(self.observations_x) > self.number_of_observations:
            self.observations_x = np.delete(self.observations_x,0)
        
        self.kf_x = KalmanFilter(transition_matrices=self.trans_matrix,
                  transition_covariance=0.01 * np.eye(2))
        
        states_pred_x = self.kf_x.em(self.observations_x).smooth(self.observations_x)[0]
        
        
        self.observations_y = np.append(self.observations_y, position_xy[1])
        
        if len(self.observations_y) == 1:
            return position_xy
            
        if len(self.observations_y) > self.number_of_observations:
            self.observations_y = np.delete(self.observations_y,0)
        
        self.kf_y = KalmanFilter(transition_matrices=self.trans_matrix,
                  transition_covariance=0.01 * np.eye(2))
        
        states_pred_y = self.kf_y.em(self.observations_y).smooth(self.observations_y)[0]

        return (states_pred_x[:, 0][-1],states_pred_y[:,0][-1])
