from kzpy3.vis3 import *

#,a

if 'N' not in locals():
    N = lo(opjD('Data/Network_Predictions',('tegra-ubuntu_30Oct18_15h58m09s.net_predictions.pkl')))
if False:
    for i in range(10000,20000):
        clf()
        plt.xlim(-60,60)
        for c,t in zip(['r','b','g'],['left','direct','right']):
            plot(-N[t][i]['heading'],rlen(N[t][i]['heading']),c+'.-')
        a = N['left'][i]['heading']
        b = N['direct'][i]['heading']
        d = -(a+b)/2.
        plot(d,rlen(d),'k.-')    
        plt.title(d2s(i))
        spause()
        time.sleep(1/30.)


P = {}

P['ABORT'] = False
P['customers'] = ['VT menu']
P['To Expose'] = {}
#
###############################################3

# walking pace ~= 1.4 m/s
P['graphics 1'] = True ####TEMP_CHANGE False
P['graphics 2'] = True
P['graphics 3'] = True ####TEMP_CHANGE False
P['save metadata'] = False
P['step_size'] = 1
P['cmd/clear_screen'] = False
P['cv2 delay'] = 1
P['3d image scale'] = 2.0#1.0
P['metadata_3D_img scale'] = 8.3
P['Prediction2D_plot scale'] = 8.3
P['num timesteps'] = 2#8
P['load_timer_time'] = 2
P['U_heading_gain'] = 2.0
P['initial index'] = 0
P['backup parameter'] = 1.0
P['use center line'] = True
P['cmd/an impulse (click)'] = False
P['show timer time'] = 0
P['add_mode'] = True
P['skip_3D'] = False
P['d_heading_multiplier'] = 1.0
P['cmd_camera_to_camera_heading_cooeficient'] = 0.75
P['99 mov timer time'] = 1.0
P['To Expose']['VT menu'] = sorted(P.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
    P['To Expose']['VT menu'].remove(h)
for k in P.keys():
    if '!' in k:
        P['To Expose']['VT menu'].remove(k)
P['dst path'] = opjD('Data/Network_Predictions_projected_gain_2')
P['timer'] = Timer(5)
P['vec sample frequency'] = 3.33
P['start menu automatically'] = False
P['vel-encoding coeficient'] = (1.0/2.3)
P['show timer'] = Timer(P['show timer time'])
P['wait for start signal'] = False
P['index'] = P['initial index']
P['topic_suffix'] = ''
P['behavioral_mode_list'] = ['left','direct','right']


def vec(heading,encoder,motor,sample_frequency,_):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

def get_predictions2D(headings,encoders,motors,sample_frequency,_):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],P['vec sample frequency'],_) #3.33)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step

if 'O' not in locals():
    O = h5r(opjD('Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_30Oct18_15h58m09s/original_timestamp_data.h5py'))



def Traj(N,obstacle_radius,index):

    D = {}
    D['index'] = index
    D['trajectories'] = ['left','direct','right',]
    D['adjacent_trajectories'] = {
        'left':['direct','right'],
        'direct':['left','right',],
        'right':['direct','left',],
    }

    D['display'] = {
        'left':     {'color':'r','sym':'.','line':':'},
        'direct':   {'color':'b','sym':'.','line':':'},
        'right':    {'color':'g','sym':'.','line':':'},
        'left_hybrid':     {'color':'r','sym':'.','line':'-'},
        'direct_hybrid':   {'color':'b','sym':'.','line':'-'},
        'right_hybrid':    {'color':'g','sym':'.','line':'-'},
    }

    for d in D['trajectories']:
        D[d] = {'pts':None,'blocked':[]}
        Q = N[d][i]
        D[d]['pts'] = get_predictions2D(Q['heading'],Q['encoder'],Q['motor'],30,P)

    D['obstacle_radius'] = obstacle_radius
    D['obstacle_tracjectory'] = random.choice(D['trajectories'])
    D['obstacle_point'] = random.choice(range(4,len(D['left']['pts'])))

    D[D['obstacle_tracjectory']]['blocked'].append(D['obstacle_point'])

    def function_trajectory_is_blocked(other_trajectory):

        for j in rlen(D[other_trajectory]['pts']):

            if distance_between_points(D['obstacle_tracjectory'],D['obstacle_point'],other_trajectory,j) < D['obstacle_radius']:

                D[other_trajectory]['blocked'].append(j)

        D[other_trajectory]['blocked'] = sorted(list(set(D[other_trajectory]['blocked'])))

        return not not D[other_trajectory]['blocked']

    def function_no_drections_blocked():
        for t in D['trajectories']:
            if D[t]['blocked']:
                return False
        print 'no_trajectories_blocked'
        return True

    def function_all_drections_blocked():
        assert not function_no_drections_blocked()
        for t in D['trajectories']:
            if not D[t]['blocked']:
                return False
        print 'all_trajectories_blocked'
        return True

    def function_closest_non_blocked_trajectories(direction):
        assert not function_all_drections_blocked()
        if not D[direction]['blocked']:
            return direction
        a = D['adjacent_trajectories'][direction][0]
        b = D['adjacent_trajectories'][direction][1]

        if D[a]['blocked']:
             return b

        elif D[b]['blocked']:
             return a

        #print 'neither direction blocked, need to measure distance'

        if average_distance_between_trajectories(direction,a) > average_distance_between_trajectories(direction,b):
            return b
        else:
            return a

    def distance_between_points(dir0,i,dir1,j):
        x0 = D[dir0]['pts'][i][1]
        y0 = D[dir0]['pts'][i][0]   
        x1 = D[dir1]['pts'][j][1]
        y1 = D[dir1]['pts'][j][0]
        d = np.sqrt((x1-x0)**2+(y1-y0)**2)
        #print x0,y0,x1,y1,d
        return d
        
    def function_make_hybrid(direction,p):
        #o = D['obstacle_tracjectory']
        o = direction
        D[o+'_hybrid'] = {}
        D[o+'_hybrid']['blocked'] = []
        D[o+'_hybrid']['pts'] = p*D[direction]['pts'] + (1-p)*D[o]['pts']


    def average_distance_between_trajectories(dir0,dir1):
        dist = 0.
        for j in rlen(D[dir0]['pts']):
            d = distance_between_points(dir0,j,dir1,j)
            dist += d
            #kprint([d,dist],'d')
        r = dist/(1.0*len(D[dir0]['pts']))
        #kprint(r,'r')
        return r

    def function_plot():
        clf();plt_square();xylim(-2,2,0,5)
        blocked_pts = []
        
        for t in D.keys():
            use_this_t = False
            for q in D['trajectories']:
                if q in t:
                    use_this_t = True
                    if use_this_t:
                        #print t
                        #print D[t]
                        #kprint(D[t].keys(),t)
                        pts_plot(
                            D[t]['pts'],
                            D['display'][t]['color'],
                            D['display'][t]['sym']+D['display'][t]['line']
                        )
                        for i in D[t]['blocked']:
                            blocked_pts.append(D[t]['pts'][i])
        pts_plot(blocked_pts,'k',sym='s')
        mci(O['left_image']['vals'][D['index']],scale=3.)
        spause();time.sleep(1/60.)

    for t in D['trajectories']:
        function_trajectory_is_blocked(t)

    D['no_drections_blocked'] = function_no_drections_blocked
    D['all_drections_blocked'] = function_all_drections_blocked
    D['closest_non_blocked_trajectories'] = function_closest_non_blocked_trajectories
    D['plot'] = function_plot
    D['trajectory_is_blocked'] = function_trajectory_is_blocked
    D['make_hybrid'] = function_make_hybrid
    return D


for i in range(20000+rndint(1000),30000,10):
    print('\n\n\n\n\n')
    
    T = Traj(N,0.25,i)

    if not T['no_drections_blocked']():
        if not T['all_drections_blocked']():
            for t in T['trajectories']:
                closest = T['closest_non_blocked_trajectories'](t)
                if closest == t:
                    clp(t,'is not blocked')
                else:
                    clp(t,'is blocked, is closest to','`y',closest,'`')

                    for p in arange(0.1,1.04,0.05):
                        #print p
                        T['make_hybrid'](closest,p)
                        #print T['trajectory_is_blocked'](closest)
                        if not T['trajectory_is_blocked'](closest+'_hybrid'):
                            kprint(T[closest+'_hybrid'],closest+'_hybrid',ignore_keys=['pts'])
                            break
                    clp('p =',p,'`b')
    T['plot']()
    print('\n\n\n\n\n')
    raw_enter()




#,b
#EOF
