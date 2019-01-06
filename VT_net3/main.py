
sample_frequency = 30.0


T = {}
T['net/headings'] = []
T['net/encoders'] = []
T['net/motors'] = []
T['net/ready'] = False


##############################################################
#
def vec(heading,encoder,motor,sample_frequency):
    velocity = encoder * _['vel-encoding coeficient']
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

def get_latest_network_2D_trajectory_predictions(headings,encoders,motors):
    assert len(headings) == len(encoders)
    assert len(headings) == len(motors) # this means motor predictions
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],_['net sample frequency'])
        xy += v
        xys.append(xy.copy())
    return xys
#
#############################################################################
#



if T['net/ready']:
    T['net/ready'] == False
    headings = T['net/headings']
    encoders = T['net/encoders']
    motors = T['net/motors']




d_heading = _['car/heading'] - _['car/heading_prev']
encoder = _['car/encoder']
velocity = encoder * _['vel-encoding coeficient']
trajectory_vector = na([0,1]) * velocity / sample_frequency

xys.append(trajectory_vector)
xys = rotatePolygon(xys,-d_heading)
axys = na(xys)
axys -= axys[-1]
xys = list(axys)

xys += get_latest_network_2D_trajectory_predictions(headings,encoders,motors)





#
##########################################################



















#EOF
