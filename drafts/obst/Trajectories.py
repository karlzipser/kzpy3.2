from kzpy3.vis3 import *
from Trajectory import *





def Trajectories(N,obstacle_radius,index):
    _ = {}
    if 'info':
        _['-type-'] = "Trajectories(N,obstacle_radius,index)"
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
            'left':             {'color':'r','sym':'.','line':':'},
            'direct':           {'color':'b','sym':'.','line':':'},
            'right':            {'color':'g','sym':'.','line':':'},
            'left_hybrid':      {'color':'r','sym':'x','line':'-'},
            'direct_hybrid':    {'color':'b','sym':'x','line':'-'},
            'right_hybrid':     {'color':'g','sym':'x','line':'-'},
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


    def function_make_hybrid(closest,p,blocked_name):
        hybrid_name = blocked_name + '_hybrid'
        _['trajectories'][hybrid_name] = Trajectory(hybrid_name,None)
        _['trajectories'][hybrid_name]['blocked_point_indicies'] = []
        _['trajectories'][hybrid_name]['pts'] = \
            p*_['trajectories'][closest]['pts'] + \
            (1-p)*_['trajectories'][blocked_name]['pts']



    def function_plot(O):
        clf();plt_square();xylim(-2,2,0,5)
        blocked_pts = []
        
        for t in _['trajectories']:
            use_this_t = False
            for q in _['trajectory_names']:
                if q in t:
                    use_this_t = True
                    if use_this_t:

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




#EOF
