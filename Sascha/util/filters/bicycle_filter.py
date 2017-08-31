'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''

import numpy as np
import os
import sys
from os.path import expanduser
import time

# The third party module filterpy is added with full source so it is not necessary
# to install it on all cars. This is just an experiment, maybe another filter is used
# in the future.
if not 'filterpy' is sys.path:
    filterpath = str(os.path.join(expanduser("~"),'kzpy3','Sascha','util','filters','third_party','filterpy')) 
    sys.path.append(filterpath)
else:
    print "Filterpy was in path" 
    
from kzpy3.Sascha.util.filters.third_party.filterpy.filterpy.kalman import KalmanFilter
from kzpy3.Sascha.util.filters.third_party.filterpy.filterpy.common import Q_discrete_white_noise

def get_xy_position(position_xy,heading,steering_angle):
    
    my_filter = KalmanFilter(dim_x=2, dim_z=2)
    
    dt = 0.5
    
    my_filter.x = np.array([[2.],
                            [0.]])       # initial state (location and velocity)

    my_filter.F = np.array([[1.,1.],
                    [0.,1.]])    # state transition matrix
    
    my_filter.H = np.array([[1.,1.]])    # Measurement function
    my_filter.P *= 1000.                 # covariance matrix
    my_filter.R = 5                      # state uncertainty
    my_filter.Q = Q_discrete_white_noise(2, dt, .1) # process uncertainty
     
    i = 0.
    '''
        ----------
    x : numpy.array(dim_x, 1)
        State estimate vector

    P : numpy.array(dim_x, dim_x)
        Covariance matrix

    R : numpy.array(dim_z, dim_z)
        Measurement noise matrix

    Q : numpy.array(dim_x, dim_x)
        Process noise matrix

    F : numpy.array()
        State Transition matrix

    H : numpy.array(dim_x, dim_x)
        Measurement function
    '''
     
    while True:
        
        i += 1.
        
        time.sleep(1)
        my_filter.predict()
        my_filter.update(np.array([2.*i]))
     
        # do something with the output
        x = my_filter.x
        print x
        
        if i > 20:
            break
    

if __name__ == '__main__':
    
    print get_xy_position((23.0,4.0), np.pi/.2, np.pi/6.)
    
    