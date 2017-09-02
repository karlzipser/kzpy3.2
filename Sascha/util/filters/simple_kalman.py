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
    
    model_observations = []
    model_observations_x = []
    model_observations_y = []
    
    observations_x = []
    observations_y = []
    
    def __init__(self, number_of_observations = 10, number_of_model_observations = 50):
        self.number_of_model_observations = number_of_model_observations
        self.number_of_observations = number_of_observations
        
        self.kf_x = KalmanFilter(transition_matrices=self.trans_matrix,
                  transition_covariance=0.01 * np.eye(2))
                
        self.kf_y = KalmanFilter(transition_matrices=self.trans_matrix,
                  transition_covariance=0.01 * np.eye(2))
        

    def get_xy_position(self, position_xy, heading, steering_angle):
        
        self.observations_x.append(position_xy[0])
        self.observations_y.append(position_xy[1])
        
        
        # If the maximum number of observations to build the model is not yet reached
        if not len(self.model_observations) > self.number_of_model_observations:
            self.model_observations_x.append(position_xy[0])
            self.model_observations_y.append(position_xy[1])


        
        # If there is only one observation so far return just that
        if len(self.observations_x) == 1:
            return position_xy
        
        # If the maximum number of observations is reached, delete the oldest
        if len(self.observations_x) > self.number_of_observations:
            #self.observations_x = np.delete(self.observations_x,0)
            self.observations_x.pop(0)
        

        # If there is only one observation so far return just that
        if len(self.observations_y) == 1:
            return position_xy
        
        # If the maximum number of observations is reached, delete the oldest
        if len(self.observations_y) > self.number_of_observations:
            #self.observations_y = np.delete(self.observations_y,0)
            self.observations_y.pop(0)
        

        
        states_pred_x = self.kf_x.em(self.model_observations_x).smooth(self.observations_x)[0]       
        states_pred_y = self.kf_y.em(self.model_observations_y).smooth(self.observations_y)[1]

        return (states_pred_x[:, 0][-1],states_pred_y[:,0][-1])
