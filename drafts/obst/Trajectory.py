from kzpy3.vis3 import *
from traj_utils import *


def Trajectory(name,pts):

    _ = {}
    _['-type-'] = "Trajectory(name,pts)"
    _['name'] = name
    _['pts'] = pts
    _['blocked_point_indicies'] = []


    def function_is_blocked(obstacle_pt,obstacle_radius):
        for j in rlen(_['pts']):
            if distance_between_points(obstacle_pt,_['pts'][j]) < obstacle_radius:
                _['blocked_point_indicies'].append(j)
        _['blocked_point_indicies'] = sorted(list(set(_['blocked_point_indicies'])))
        return not not _['blocked_point_indicies']


    def function_truncate_blocked():
        first_blocked = _['blocked_point_indicies'][0]
        for j in rlen(_['pts']):
            if j >= first_blocked:
                _['pts'][j] = _['pts'][first_blocked]


    _['is_blocked'] = function_is_blocked

    _['truncate_blocked'] = function_truncate_blocked


    return _


#EOF
