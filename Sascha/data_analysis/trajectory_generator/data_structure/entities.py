'''
Created on May 16, 2017

@author: picard
'''

class Obstacle(object):
    '''
    classdocs
    '''


    def __init__(self, position, velocity,acceleration):
        '''
        Constructor
        '''
        self._position = position
        self._velocity = velocity
        self._acceleration = acceleration