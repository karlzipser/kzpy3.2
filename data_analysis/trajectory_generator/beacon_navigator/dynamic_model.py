import collections
import numpy as np
import math
try:
    from angles import normalize as normalize_angle # Adjust for different angles packages
except ImportError:
    from angles import normalize_angle #  Adjust for different angles packages
'''
Create datatype for position, speed into heading and heading (x,y,v,psi)
'''
ModelAnswer = collections.namedtuple('ModelAnswer', ['x', 'y', 'v', 'psi'])

lr = 0.14
lf = 0.14


def getXYFor(x_0, y_0, t_0, v, psi, t, a, delta):
    """
    Calculates the future position in meter, according to the model.
    Inputs: position at current time x_0, y_0
            current time t_0
            current speed in direction of movement v
            point in time to calculate t
            applied acceleration a
            steering angle over the front tire delta
    Note: The method is written for the model cars as used by Karl Zipser and Sascha Hornauer
    and the position of the center of gravity chosen respectively. Change lr and lf if it is elsewhere.
    """
    dt = t-t_0
    
    beta = np.arctan((lr/(lf+lr))*np.tan(delta))
    
    dpsi = (v/lr)*np.sin(beta)
    psi = psi + dpsi*dt
    
    dx = v * np.cos(psi+beta)

    x = x_0 + dx*dt

    dy = v * np.sin(psi+beta)
    y = y_0 + dy*dt

    dv = a
    v = v + dv*dt
    
    #answer = [x,y,v,psi]
    # Model implemented after http://www.me.berkeley.edu/~frborrel/pdfpub/IV_KinematicMPC_jason.pdf
    return x,y,v,psi

def getDistanceInPixel(offsetXInMeter,offsetYInMeter,posXInMeter,posYInMeter,pixelInOneMeterX,pixelInOneMeterY):
    #return [(posXInMeter-offsetXInMeter)*pixelInOneMeterX,(posYInMeter-offsetYInMeter)*pixelInOneMeterY]
    return [posXInMeter*pixelInOneMeterX,posYInMeter*pixelInOneMeterY]
    
