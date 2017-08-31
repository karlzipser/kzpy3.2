'''
Created on Aug 30, 2017

@author: Sascha Hornauer
'''
from kzpy3.Sascha.util.filters.simple_kalman import Simple_Kalman_Estimator

class Position_Filter():

    filter = Simple_Kalman_Estimator()

    def get_xy_position(self,position_xy,heading,steering_angle):
        return filter.get_xy_position(position_xy,heading,steering_angle)

if __name__ == '__main__':
    
    
    
    test_filter = Position_Filter()
    
    
    



