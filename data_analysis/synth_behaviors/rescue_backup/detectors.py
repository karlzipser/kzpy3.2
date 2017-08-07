'''
Created on Jun 5, 2017

@author: Sascha Hornauer
'''


verbose = False
tilt_x_threshold = 6.

class Detector:
    
    def __init__(self):
        pass
    
    def check_state(self, state_info):
        pass
    
class Obstacle_Crash_Detector(Detector):
    
    def __init__(self):
        Detector.__init__(self)
        
    def check_state(self, incoming_state_info):
        #print incoming_state_info.__repr__()
        return False, self.__class__.__name__
        
    
class Side_Tilted_Detector(Detector):
    
    def __init__(self):
        Detector.__init__(self)
        
    def check_state(self, incoming_state_info):
        
        global tilt_x_threshold 
        
        rescue_needed = False
        
        try:
            if -tilt_x_threshold > incoming_state_info.acc_data.x or incoming_state_info.acc_data.x > tilt_x_threshold:
                print "Tilted!!!" + str(incoming_state_info.acc_data.x)
                rescue_needed = True
        except AttributeError as error:
            if verbose:
                print error
        
        return rescue_needed, self.__class__.__name__