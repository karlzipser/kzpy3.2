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
    
    kf_x = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
    kf_y = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
    observations_x = []
    observations_y = []

    def get_xy_position(self, position_xy, heading, steering_angle):
        
        self.observations_x = np.append(self.observations_x, position_xy[0])
        
        if len(self.observations_x) == 1:
            return [position_xy]
            
        if len(self.observations_x) > self.number_of_observations:
            self.observations_x = np.delete(self.observations_x,0)
            
        states_pred_x = self.kf_x.em(self.observations_x).smooth(self.observations_x)[0]
        
        
        self.observations_y = np.append(self.observations_y, position_xy[1])
        
        if len(self.observations_y) == 1:
            return [position_xy]
            
        if len(self.observations_y) > self.number_of_observations:
            self.observations_y = np.delete(self.observations_y,0)
            
        states_pred_y = self.kf_y.em(self.observations_y).smooth(self.observations_y)[0]
        
        
        return (states_pred_x[:, 0],states_pred_y[:,0])

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
        #plt.figure(figsize=(16, 6))
        result = filter.get_xy_position((observations[i],observations[i]), np.pi / .2, np.pi / 6.)
        #print result
        #print len(result)
        #x = np.arange(0,len(result))
        #print x
        #plt.plot(x,result[0], color='b')
        #plt.plot(x,actual_values[max(0,i-9):i+1], color='r')
        #plt.plot(x,observations[max(0,i-9):i+1],color='g')
        #plt.show()
        #plt.pause(0.1)
        #plt.close()
        print "--"
        print np.mean(observations[max(0,i-9):i+1]-result[0])
        print "--"
        time.sleep(1)
        
        
    
