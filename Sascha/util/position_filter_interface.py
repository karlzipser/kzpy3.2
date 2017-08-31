'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''
from kzpy3.Sascha.util.filters.simple_kalman import Simple_Kalman_Estimator

class Position_Filter():

    def __init__(self, number_of_observations):    
        self.filter = Simple_Kalman_Estimator(number_of_observations)

    def get_xy_position(self,position_xy,heading,steering_angle):
        
        position_filtered = self.filter.get_xy_position(position_xy,heading,steering_angle) 
        
        return position_filtered, heading


