from kzpy3.vis3 import *
#
#,a

Arguments = {
    'run_name':'tegra-ubuntu_31Oct18_16h06m32s',
}

def plot_line(A,B,c='r'):
    plot([A[0],B[0]],[A[1],B[1]],c)

def pts_dist(A,B):
    return np.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

Colors = {'direct':'b','left':'r','right':'g'}

if True:

    if 'lst' not in locals():
        lst = lo('/Users/karlzipser/Desktop/Data/pts2D_multi_step/pkl/'+Arguments['run_name']+'.pkl')

    if 'Pts' not in locals():
        Pts = {
            'left':{},
            'right':{},
            'direct':{},
        }
        for k in Pts:
            for i in range(10):
                Pts[k][i] = []
        Pts['xy'] = []

        for i in range(len(lst)-10):
            N = lst[i]
            Pts['xy'].append(na([N['x'],N['y']]))
            for b in ['left','right','direct']:
                for j in rlen(N[b]):
                    Pts[b][j].append(N[b][j])

    if 'angles' not in Pts:
        Pts['angles'] = {}
        o = lo('/Users/karlzipser/Desktop/Data/pts2D_multi_step/pkl_angles0/'+Arguments['run_name']+'.pkl')
        Pts['angles']['left'] = o['left']
        Pts['angles']['right'] = o['right']

    if 'angles_meo' not in Pts:
        Pts['angles_meo'] = {}
        Pts['angles_meo']['left'] = meo(Pts['angles']['left'],10)
        Pts['angles_meo']['right'] = meo(Pts['angles']['right'],10)

    if 'direct_meo' not in Pts:
        n = 90#33
        Pts['left_meo'] = {}
        Pts['right_meo'] = {}
        Pts['direct_meo'] = {}
        for q in range(10):
            cg('meo',q)
            a = Pts['left'][q]
            ax = meo(na(a)[:,0],n)
            ay = meo(na(a)[:,1],n)
            Pts['left_meo'][q] = na([ax,ay]).transpose()
            a = Pts['right'][q]
            ax = meo(na(a)[:,0],n)
            ay = meo(na(a)[:,1],n)
            Pts['right_meo'][q] = na([ax,ay]).transpose()
            a = Pts['direct'][q]
            ax = meo(na(a)[:,0],n)
            ay = meo(na(a)[:,1],n)
            Pts['direct_meo'][q] = na([ax,ay]).transpose()

    if 'O' not in locals():
        a0,O,a1 = open_run2(Arguments['run_name'])



def f___(x,A,B):
    return A*x+B
    #xy = Pts['direct9_meo'][i+start:i+start + 3*30:step]
    #h = normalized_vector_from_pts(xy)
    #m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
    #xs = na([XY[0]-20,XY[0]+20])
    #ys = m * xs + b
    #plot(xs,ys,'c')
    #plot([XY[0],XY[0]+ 10*h[0]],[XY[1],XY[1]+ 10*h[1]],'c')
    #plot([XY[0],XY[0]+ m*h[0]],[XY[1],XY[1]+ 10*h[1]],'b')
#EOF
