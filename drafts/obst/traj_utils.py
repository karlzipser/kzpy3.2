from kzpy3.vis3 import *


def vec(heading,encoder,motor,vec_sample_frequency,vel_encoding_coeficient):
    velocity = encoder * vel_encoding_coeficient
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/vec_sample_frequency
    return array(a)





def get_predictions2D(headings,encoders,motors,sample_frequency,vec_sample_frequency,vel_encoding_coeficient):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],vec_sample_frequency,vel_encoding_coeficient)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step





def distance_between_points(pt0,pt1):
    x0 = pt0[1]
    y0 = pt0[0]   
    x1 = pt1[1]
    y1 = pt1[0]
    d = np.sqrt((x1-x0)**2+(y1-y0)**2)
    return d

#EOF

