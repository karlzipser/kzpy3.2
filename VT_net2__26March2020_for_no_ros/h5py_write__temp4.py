from kzpy3.vis3 import *

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

    if 'direct9_meo' not in Pts:
        n = 90#33
        a = Pts['left'][9]
        ax = meo(na(a)[:,0],n)
        ay = meo(na(a)[:,1],n)
        Pts['left9_meo'] = na([ax,ay]).transpose()
        a = Pts['right'][9]
        ax = meo(na(a)[:,0],n)
        ay = meo(na(a)[:,1],n)
        Pts['right9_meo'] = na([ax,ay]).transpose()
        a = Pts['direct'][9]
        ax = meo(na(a)[:,0],n)
        ay = meo(na(a)[:,1],n)
        Pts['direct9_meo'] = na([ax,ay]).transpose()

    if 'O' not in locals():
        a0,O,a1 = open_run2(Arguments['run_name'])


start = -2*30
end = start + 10*30
step = 30/3
d = 20


for i in range(6500,200000+6500,1):

    if True:
        XY = Pts['xy'][i]
        figure(1);clf();plt_square(); xylim(XY[0]-d,XY[0]+d,XY[1]-d,XY[1]+d)

    
    if True:
        xy = na(Pts['xy'][i-15:i+1])
        plot(xy[:,0],xy[:,1],'k')

    for k in Colors.keys():
        xy = Pts[k+'9_meo'][i+start:i+end:step]
        plot(xy[:,0],xy[:,1],Colors[k]+'-')

    for j in range(i+start,i+end,step):

        if Pts['angles_meo']['left'][j] < -40:
            pts_plot(Pts['left9_meo'][j],'r',sym='o')
        elif Pts['angles_meo']['left'][j] < -20:
            pts_plot(Pts['left9_meo'][j],'r',sym='.')

        if Pts['angles_meo']['right'][j] > 40:
            pts_plot(Pts['right9_meo'][j],'g',sym='o')
        elif Pts['angles_meo']['right'][j] > 20:
            pts_plot(Pts['right9_meo'][j],'g',sym='.')

        E = Pts['left9_meo'][j]#+step]
        R = Pts['right9_meo'][j]#+step]
        D = Pts['direct9_meo'][j]
        plot_line(R,D,'g:')
        plot_line(E,D,'r:')

    
    
    spause()
    e = 15
    figure(2);clf();plt_square(); xylim(-e,e,-e/4,2*e)
    A = Pts['direct9_meo'][i+start] - Pts['direct9_meo'][i+start-2]
    alpha = angle_clockwise((0,1),A)
    for k in Colors:
        pts_plot(
            rotatePolygon(
                Pts[k+'9_meo'][i+start:i+end:step] -Pts['direct9_meo'][i+start-1],alpha),
            Colors[k],sym='.-')

    img = O['left_image']['vals'][i]
    img = cv2.resize(img,(168*2,94*2))
    img[:,168,:] = int((127+255)/2)
    mci(img,title='left_image',scale=1.)
    
# width of path
# angles over various distances
# input future navigation commands

    spause()    

#,b

#EOF
