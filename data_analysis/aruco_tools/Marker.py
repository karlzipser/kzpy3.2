'''
Created on Apr 13, 2017

@author: Sascha Hornauer
'''

class Marker(object):
    '''
    Getter and setter are at the bottom of the class
    '''
    
    # Values for the confidence calculation
    max_distance = 10 # meter
    #max_angle = 
    def __init__(self, marker_id=None, confidence=None, corners_xy=None, rvec=None, tvec=None, pos_xy=None, shift_angle_trans=None, distance=None):
        '''
        Constructor
        '''
        self.marker_id = marker_id
        self.confidence = confidence
        self.corners_xy = corners_xy
        self.rvec = rvec
        self.tvec = tvec
        self.pos_xy = pos_xy
        self.shift_angle_trans = shift_angle_trans
        self.aquired_at_distance = distance
    
    def update_perception(self,corners_xy,rvec,tvec):
        self._corners_xy = corners_xy
        self._rvec = rvec
        self._tvec = tvec
    
    def update_pos_and_shift (self,pos_xy,aquired_at_distance,shift_angle_trans):
        self._pos_xy = pos_xy
        self._aquired_at_distance = aquired_at_distance
        self._shift_angle_trans = shift_angle_trans
        print(shift_angle_trans[0])
        
    
    def set_marker_id(self, value):
        self._marker_id = value
            
    def get_marker_id(self):
        return self._marker_id        
    
    def get_confidence(self):
        return self._confidence
    
    def set_confidence(self, value):
        self._confidence = value
    
    def get_corners_xy(self):
        return self._corners_xy
    
    def set_corners_xy(self, value):
        self._corners_xy = value
    
    def get_rvec(self):
        return self._rvec
    
    def set_rvec(self, value):
        self._rvec = value
    
    def get_tvec(self):
        return self._tvec
    
    def set_tvec(self, value):
        self._tvec = value
    
    def get_pos_xy(self):
        return self._pos_xy
    
    def set_pos_xy(self, value):
        self._pos_xy = value
    
    def get_shift_angle_trans(self):
        return self._shift_angle_trans
    
    def set_shift_angle_trans(self, value):
        self._shift_angle_trans = value
    
    def get_aquired_at_distance(self):
        return self._aquired_at_distance
    
    def set_aquired_at_distance(self, value):
        self._aquired_at_distance = value

    marker_id = property(get_marker_id, set_marker_id)
    confidence = property(get_confidence, set_confidence)
    corners_xy = property(get_corners_xy, set_corners_xy)
    rvec = property(get_rvec, set_rvec)
    tvec = property(get_tvec, set_tvec)
    pos_xy = property(get_pos_xy, set_pos_xy)
    shift_angle_trans = property(get_shift_angle_trans, set_shift_angle_trans)
    aquired_at_distance = property(get_aquired_at_distance, set_aquired_at_distance)

    def __repr__(self):
        '''
        Quick string out method
        '''
        
        return str(vars(self))
   
