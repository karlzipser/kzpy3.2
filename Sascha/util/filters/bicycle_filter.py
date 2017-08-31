'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''

import numpy as np
import os
import sys
from os.path import expanduser
import time
from pykalman import KalmanFilter
import pylab as pl

class Simple_Kalman_Estimator():

    number_of_observations = 40
    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)
    observations = []

    def get_xy_position(self,position_xy,heading,steering_angle):
        
        self.observations = np.append(self.observations,position_xy)
        
        if len(self.observations == 1):
            self.observations = np.append(self.observations,position_xy)
        
        
        
        # create a Kalman Filter by hinting at the size of the state and observation
        # space.  If you already have good guesses for the initial parameters, put them
        # in here.  The Kalman Filter will try to learn the values of all variables.
        kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                          transition_covariance=0.01 * np.eye(2))
        
        states_pred = kf.em(observations).smooth(observations)[0]
        
        return states_pred

if __name__ == '__main__':
    
    filter = Simple_Kalman_Estimator()
    
    rnd = np.random.RandomState(0)
        
    # generate a noisy sine wave to act as our fake observations
    n_timesteps = 100
    x = np.linspace(0, 3 * np.pi, n_timesteps)
    src_observations = 20 * (np.sin(x) + 0.5 * rnd.randn(n_timesteps))
    
    observations = src_observations[0]
    
    pl.ion()
    
    for i in range(1,len(src_observations)):
    
        states_pred = filter.get_xy_position(src_observations[i], np.pi/.2, np.pi/6.)
        
        x = np.linspace(0, 3 * np.pi, i+1)
        fig = pl.figure(figsize=(16, 6))
        
        obs_scatter = pl.scatter(x, observations, marker='x', color='b',
                                 label='observations')
        position_line = pl.plot(x, states_pred[:, 0],
                                linestyle='-', marker='o', color='r',
                                label='position est.')
        velocity_line = pl.plot(x, states_pred[:, 1],
                                linestyle='-', marker='o', color='g',
                                label='velocity est.')
        pl.legend(loc='lower right')
        pl.xlim(xmin=0, xmax=x.max())
        pl.xlabel('time')
        pl.show()
        pl.pause(1)
        pl.close()
            
    