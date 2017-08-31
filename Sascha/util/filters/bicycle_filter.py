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
import pylab as pl

class Simple_Kalman_Estimator():

    number_of_observations = 5
    
    kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
    observations = []

    def get_xy_position(self, position_xy, heading, steering_angle):
        
        self.observations = np.append(self.observations, position_xy)
        
        if len(self.observations) == 1:
            self.observations = np.append(self.observations, position_xy)
            
        if len(self.observations) > self.number_of_observations:
            self.observations = np.delete(self.observations,0)
            
        states_pred = self.kf.em(self.observations).smooth(self.observations)[0]
        
        return states_pred[:, 0]

if __name__ == '__main__':
    
    filter = Simple_Kalman_Estimator()
    
    
    pl.ion()
    
   

    lower_bound = max(0,i-4)
    upper_bound = i+2
    
    observations = src_observations[lower_bound:upper_bound]
    
    states_pred = filter.get_xy_position(src_observations[i], np.pi / .2, np.pi / 6.)
    print len(states_pred)
    print len(observations)
    x = np.linspace(lower_bound, 3 * np.pi, upper_bound)
    print len(x)
    fig = pl.figure(figsize=(16, 6))
            
    obs_scatter = pl.scatter(x, observations, marker='x', color='b',
                             label='observations')
    position_line = pl.plot(x, states_pred,
                            linestyle='-', marker='o', color='r',
                            label='position est.')
    # velocity_line = pl.plot(x, states_pred[:, 1],
    #                        linestyle='-', marker='o', color='g',
    #                        label='velocity est.')
    pl.legend(loc='lower right')
    pl.xlim(xmin=0, xmax=x.max())
    pl.xlabel('time')
    pl.show()
    pl.pause(1)
    pl.close()
            
    
