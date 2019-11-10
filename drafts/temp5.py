from kzpy3.vis3 import *



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

if False:
    Pts = {}
    for i in range(20000+rndint(1000),30000,10):
        clf();plt_square();xylim(-2,2,0,5)
        for c,t in zip(['r','b','g'],['left','direct','right']):
            Q = N[t][i]
            Pts[t] = get_predictions2D(Q['heading'],Q['encoder'],Q['motor'],30,P)
            pts_plot(Pts[t],c,'.-')

        obstacle_trajectory = random.choice(['left','direct','right'])
        obstacle_point = random.choice(range(4,len(Pts['left'])))
        obstacle_radius = .15
        x0 = Pts[obstacle_trajectory][obstacle_point][1]
        y0 = Pts[obstacle_trajectory][obstacle_point][0]
        for t in ['left','direct','right']:
            for j in rlen(Pts[t]):
                x1 = Pts[t][j][1]
                y1 = Pts[t][j][0]
                if np.sqrt((x1-x0)**2+(y1-y0)**2) < obstacle_radius:
                    plot(y1,x1,'k.')
                #print x0,y0,x1,y1
        mci(O['left_image']['vals'][i],scale=3.)
        spause();time.sleep(1/60.)
        break


if False:
    Pts = {}
    for i in range(20000+rndint(1000),30000,10):
        clf();plt_square();xylim(-2,2,0,5)
        for c,t in zip(['r','b','g'],['left','direct','right']):
            Q = N[t][i]
            Pts[t] = get_predictions2D(Q['heading'],Q['encoder'],Q['motor'],30,P)
            pts_plot(Pts[t],c,'.-')

        obstacle_trajectory = random.choice(['left','direct','right'])
        obstacle_point = random.choice(range(4,len(Pts['left'])))
        obstacle_radius = .15
        x0 = Pts[obstacle_trajectory][obstacle_point][1]
        y0 = Pts[obstacle_trajectory][obstacle_point][0]
        for t in ['left','direct','right']:
            for j in rlen(Pts[t]):
                x1 = Pts[t][j][1]
                y1 = Pts[t][j][0]
                if np.sqrt((x1-x0)**2+(y1-y0)**2) < obstacle_radius:
                    plot(y1,x1,'k.')
                #print x0,y0,x1,y1
        mci(O['left_image']['vals'][i],scale=3.)
        spause();time.sleep(1/60.)
        break


def Traj():

    D = {}

    D['directions'] = ['left','direct','right',]
    D['adjacent_directions'] = {
        'left':['direct','right'],
        'direct':['left','right',],
        'right':['left','direct','right',],
    }

    colors = ['r','b','g',]

    for d,c in zip(D['directions'],colors):
        D[d] = {'color':c,'pts':None,'blocked':[]}


    def function_make_random_obstacle(obstacle_radius=0.45):
        obstacle_trajectory = random.choice(D['directions'])
        obstacle_point = random.choice(range(4,len(D['left']['pts'])))
        D[obstacle_trajectory]['blocked'].append(obstacle_point)
        x0 = D[obstacle_trajectory]['pts'][obstacle_point][1]
        y0 = D[obstacle_trajectory]['pts'][obstacle_point][0]
        for t in D['directions']:
            for j in rlen(D[t]['pts']):
                x1 = D[t]['pts'][j][1]
                y1 = D[t]['pts'][j][0]
                if np.sqrt((x1-x0)**2+(y1-y0)**2) < obstacle_radius:
                    D[t]['blocked'].append(j)
                    plot(y1,x1,'k.')
                #print x0,y0,x1,y1
        mci(O['left_image']['vals'][i],scale=3.)
        spause();time.sleep(1/60.)
    
    def function_adjust_trajectory(direction):

    
    D['make_random_obstacle'] = function_make_obstacle

    return D


for i in range(20000+rndint(1000),30000,10):
    clf();plt_square();xylim(-2,2,0,5)
    T = Traj()
    for t in T['directions']:
        Q = N[t][i]
        T[t]['pts'] = get_predictions2D(Q['heading'],Q['encoder'],Q['motor'],30,P)
        pts_plot(T[t]['pts'],T[t]['color'],'.-')
    T['make_obstacle']()








    """
    spause()
    raw_enter()

    obstacle_trajectory = random.choice(T['directions'])
    obstacle_point = random.choice(range(4,len(Pts['left'])))
    obstacle_radius = .15
    x0 = Pts[obstacle_trajectory][obstacle_point][1]
    y0 = Pts[obstacle_trajectory][obstacle_point][0]
    for t in T['directions']:
        for j in rlen(Pts[t]):
            x1 = Pts[t][j][1]
            y1 = Pts[t][j][0]
            if np.sqrt((x1-x0)**2+(y1-y0)**2) < obstacle_radius:
                plot(y1,x1,'k.')
            #print x0,y0,x1,y1
    mci(O['left_image']['vals'][i],scale=3.)
    spause();time.sleep(1/60.)
    break
    """


#EOF
