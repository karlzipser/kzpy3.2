from kzpy3.vis3 import *
from Trajectories import *



###################
#
if 'O' not in locals():
    O = h5r(opjD('Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_30Oct18_15h58m09s/original_timestamp_data.h5py'))

if 'N' not in locals():
    N = lo(opjD('Data/Network_Predictions',('tegra-ubuntu_30Oct18_15h58m09s.net_predictions.pkl')))
#
###################




    
for i in range(20000+rndint(5000),30000,10):

    
    T = Trajectories(N,0.35,i)
    
    if not T['no_drections_blocked']():
        if not T['all_drections_blocked']():
            for t in T['trajectory_names']:
                closest = T['closest_non_blocked_trajectories'](t)
                if closest == t:
                    clp(t,'`--r','is not blocked')
                else:
                    clp(t,'`--r','is blocked, is closest to','`y',closest,'`--u')

                    for p in arange(0.1,1.04,0.05):
                        T['make_hybrid'](closest,p,t)
                        if not T['trajectories'][t+'_hybrid']['is_blocked'](
                            T['trajectories'][T['obstacle_tracjectory_name']]['pts'][T['obstacle_point_index']],
                            T['obstacle_radius']
                            ):
                            T['trajectories'][t+'_hybrid']['p'] = p
                            break
                    clp('p =',p,'`b')
        else:
            for t in T['trajectory_names']:
                T['trajectories'][t]['truncate_blocked']()



    T['plot'](O)

    kprint(T['trajectories'],ignore_types=function_types,ignore_keys=['pts'])
    

    a = raw_enter()

    if a == 'q':
        O.close()
        break

        
    print('\n\n\n\n\n')





#EOF
