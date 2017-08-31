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

    number_of_observations = 10
    
    kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
    observations = []

    def get_xy_position(self, position_xy, heading, steering_angle):
        
        self.observations = np.append(self.observations, position_xy)
        
        if len(self.observations) == 1:
            #self.observations = np.append(self.observations, position_xy)
            return [position_xy]
            
        if len(self.observations) > self.number_of_observations:
            self.observations = np.delete(self.observations,0)
            
        states_pred = self.kf.em(self.observations).smooth(self.observations)[0]
        
        return states_pred[:, 0]

if __name__ == '__main__':
    
    filter = Simple_Kalman_Estimator()

    rnd = np.random.RandomState(0)
    plt.ion()

    
    # generate a noisy sine wave to act as our fake observations
    n_timesteps = 100
    x = np.linspace(0, 3 * np.pi, n_timesteps)
    observations = 20 * (np.sin(x) + 0.5 * rnd.randn(n_timesteps))
    actual_values = 20 * (np.sin(x) + 0.5)
    for i in range(0,len(observations)):
        plt.figure(figsize=(16, 6))
        result = filter.get_xy_position(observations[i], np.pi / .2, np.pi / 6.)
        x = np.arange(0,len(result))
        
        plt.plot(x,result, color='b')
        plt.plot(x,actual_values[max(0,i-9):i+1], color='r')
        plt.plot(x,observations[max(0,i-9):i+1],color='g')
        plt.show()
        plt.pause(0.1)
        plt.close()
        
    
