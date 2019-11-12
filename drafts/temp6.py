#,a

from kzpy3.vis3 import *

TYPE = '-type-'
###################
#
if 'O' not in locals():
    O = h5r(opjD('Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_30Oct18_15h58m09s/original_timestamp_data.h5py'))

if 'N' not in locals():
    N = lo(opjD('Data/Network_Predictions',('tegra-ubuntu_30Oct18_15h58m09s.net_predictions.pkl')))
#
###################


###################
#
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
#
###################

def distance_between_points(pt0,pt1):
    x0 = pt0[1]
    y0 = pt0[0]   
    x1 = pt1[1]
    y1 = pt1[0]
    d = np.sqrt((x1-x0)**2+(y1-y0)**2)
    return d

###################
#
def Trajectory(name,pts):
    _ = {}
    _[TYPE] = "Trajectory(name,pts)"
    _['name'] = name
    _['pts'] = pts
    _['blocked_point_indicies'] = []
    def function_is_blocked(obstacle_pt,obstacle_radius):
        for j in rlen(_['pts']):
            if distance_between_points(obstacle_pt,_['pts'][j]) < obstacle_radius:
                _['blocked_point_indicies'].append(j)
        _['blocked_point_indicies'] = sorted(list(set(_['blocked_point_indicies'])))
        return not not _['blocked_point_indicies']
        #_['is_blocked'] = function_is_blocked
    _['is_blocked'] = function_is_blocked
    #kprint(_,'Trajectory')
    return _
#
###################


###################
#
def Trajectories(N,obstacle_radius,index):
    _ = {}
    _[TYPE] = "Trajectories(N,obstacle_radius,index)"
    if True:
        _['vec sample frequency'] = 3.33
        _['vel-encoding coeficient'] = (1.0/2.3)
        _['index'] = index
        _['trajectory_names'] = ['left','direct','right',]
        _['adjacent_trajectory_names'] = {
            'left':['direct','right'],
            'direct':['left','right',],
            'right':['direct','left',],
        }
        _['display'] = {
            'left':     {'color':'r','sym':'.','line':':'},
            'direct':   {'color':'b','sym':'.','line':':'},
            'right':    {'color':'g','sym':'.','line':':'},
            'left_hybrid':     {'color':'r','sym':'x','line':'-'},
            'direct_hybrid':   {'color':'b','sym':'x','line':'-'},
            'right_hybrid':    {'color':'g','sym':'x','line':'-'},
        }
        _['obstacle_radius'] = obstacle_radius
        _['obstacle_tracjectory_name'] = random.choice(_['trajectory_names'])

    _['trajectories'] = {}
    for t in _['trajectory_names']:
        Q = N[t][index]
        pts = get_predictions2D(
            Q['heading'],
            Q['encoder'],
            Q['motor'],
            30,
            _['vec sample frequency'],
            _['vel-encoding coeficient'],
        )
        _['trajectories'][t] = Trajectory(t,pts)

    #kprint(_,'Trajectories')
    #raw_enter()
    _['obstacle_point_index'] = random.choice(range(4,len(_['trajectories']['left']['pts'])))
    _['trajectories'][_['obstacle_tracjectory_name']]['blocked_point_indicies'].append(_['obstacle_point_index'])



    def function_no_drections_blocked():
        for t in _['trajectory_names']:
            if _['trajectories'][t]['blocked_point_indicies']:
                return False
        print 'no trajectories are blocked'
        return True


    def function_all_drections_blocked():
        assert not function_no_drections_blocked()
        for t in _['trajectory_names']:
            if not _['trajectories'][t]['blocked_point_indicies']:
                return False
        print 'all trajectories are blocked'
        return True


    def function_closest_non_blocked_trajectories(name):
        assert not function_all_drections_blocked()
        if not _['trajectories'][name]['blocked_point_indicies']:
            return name
        a = _['adjacent_trajectory_names'][name][0]
        b = _['adjacent_trajectory_names'][name][1]

        #kprint(a)
        #kprint(b)

        if _['trajectories'][a]['blocked_point_indicies']:
             return b

        elif _['trajectories'][b]['blocked_point_indicies']:
             return a

        if average_distance_between_trajectories(name,a) > average_distance_between_trajectories(name,b):
            return b
        else:
            return a





    def average_distance_between_trajectories(name0,name1):
        dist = 0.
        for j in rlen(_['trajectories'][name0]['pts']):
            d = distance_between_points(
                _['trajectories'][name0]['pts'][j],
                _['trajectories'][name1]['pts'][j]
            )
            dist += d
        r = dist/(1.0*len(_['trajectories'][name0]['pts']))
        return r


    def function_make_hybrid(name,p,t):
        hname = t + '_hybrid'
        #hname = _['obstacle_tracjectory_name'] + '_hybrid'
        #o = _['obstacle_tracjectory_name']
        #o = direction
        #_['trajectories'][o+'_hybrid'] = Trajectory(o+'_hybrid',None)
        #_['trajectories'][o+'_hybrid']['blocked_point_indicies'] = []
        #_['trajectories'][o+'_hybrid']['pts'] = p*_['trajectories'][name]['pts'] + (1-p)*_['trajectories'][o]['pts']
        #o = _['obstacle_tracjectory_name']
        #o = direction
        _['trajectories'][hname] = Trajectory(hname,None)
        _['trajectories'][hname]['blocked_point_indicies'] = []
        _['trajectories'][hname]['pts'] = \
            p*_['trajectories'][name]['pts'] + \
            (1-p)*_['trajectories'][_['obstacle_tracjectory_name']]['pts']




    def function_plot():
        clf();plt_square();xylim(-2,2,0,5)
        blocked_pts = []
        
        for t in _['trajectories']:
            use_this_t = False
            for q in _['trajectory_names']:
                if q in t:
                    use_this_t = True
                    if use_this_t:
                        #print t
                        #print _[t]
                        #kprint(_[t].keys(),t)
                        pts_plot(
                            _['trajectories'][t]['pts'],
                            _['display'][t]['color'],
                            _['display'][t]['sym']+_['display'][t]['line']
                        )
                        for i in _['trajectories'][t]['blocked_point_indicies']:
                            blocked_pts.append(_['trajectories'][t]['pts'][i])
        pts_plot(blocked_pts,'k',sym='s')
        mci(O['left_image']['vals'][_['index']],scale=3.)
        spause();time.sleep(1/60.)

    for t in _['trajectory_names']:
        _['trajectories'][t]['is_blocked'](
            _['trajectories'][_['obstacle_tracjectory_name']]['pts'][_['obstacle_point_index']],
            _['obstacle_radius']
        )





    _['no_drections_blocked'] = function_no_drections_blocked
    _['all_drections_blocked'] = function_all_drections_blocked
    _['closest_non_blocked_trajectories'] = function_closest_non_blocked_trajectories
    _['plot'] = function_plot
    _['make_hybrid'] = function_make_hybrid
    return _
#
####################




if __name__ == '__main__':
    
    for i in range(20000+rndint(1000),30000,10):
        print('\n\n\n\n\n')
        
        E = {'Trajectories':Trajectories(N,0.25,i)}
        T = E['Trajectories']
        #

        if not T['no_drections_blocked']():
            if not T['all_drections_blocked']():
                for t in T['trajectory_names']:
                    closest = T['closest_non_blocked_trajectories'](t)
                    if closest == t:
                        clp(t,'is not blocked')
                    else:
                        clp(t,'is blocked, is closest to','`y',closest,'`')

                        for p in arange(0.1,1.04,0.05):
                            #print p
                            T['make_hybrid'](closest,p,t)
                            #print T['trajectory_is_blocked'](closest)
                            #print T['trajectories'][T['obstacle_tracjectory_name']]['pts'][T['obstacle_point_index']],T['obstacle_radius']
                            if not T['trajectories'][t+'_hybrid']['is_blocked'](
                                T['trajectories'][T['obstacle_tracjectory_name']]['pts'][T['obstacle_point_index']],
                                T['obstacle_radius']
                                ):
                                #kprint(T[closest+'_hybrid'],closest+'_hybrid',ignore_keys=['pts'])
                                break
                        clp('p =',p,'`b')
        T['plot']()
        kprint(E,ignore_keys=['pts'])
        
        raw_enter()
        print('\n\n\n\n\n')




#,b
#EOF
