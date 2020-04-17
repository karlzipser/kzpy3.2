from kzpy3.vis3 import *

def f___(x,A,B):
    return A*x+B
def normalized_vector_from_pts(pts):
    pts = array(pts)
    x = pts[:,0]
    y = pts[:,1]
    m,b = curve_fit(f___,x,y)[0]
    heading = normalized([1,m])[0]
    len_heading = length(heading)
    #print len_heading
    #if np.abs(len_heading-1.0)>0.1:
    #    print('here')
    #    print((heading,len_heading,pts))
    #    assert(False)
    return heading
#,a

def pts_dist(a,b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def plot_line(A,B,c='r'):
    plot([A[0],B[0]],[A[1],B[1]],c)

Colors = {'direct':'b','left':'r','right':'g'}

if 'lst' not in locals():
    lst = lo('/Users/karlzipser/Desktop/Data/pts2D_multi_step/pkl/tegra-ubuntu_31Oct18_16h06m32s.pkl')

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
    o = lo('/Users/karlzipser/Desktop/Data/pts2D_multi_step/pkl_angles0/tegra-ubuntu_31Oct18_16h06m32s.pkl')
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

start = -2*30
end = start + 10*30
step = 30/5
d = 20
for i in range(6500,200000+6500,5):
    XY = Pts['xy'][i]
    figure(1);clf();plt_square(); xylim(XY[0]-d,XY[0]+d,XY[1]-d,XY[1]+d)

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

    #xy = Pts['direct9_meo'][i+start:i+start + 3*30:step]
    #h = normalized_vector_from_pts(xy)
    #m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
    #xs = na([XY[0]-20,XY[0]+20])
    #ys = m * xs + b
    #plot(xs,ys,'c')
    #plot([XY[0],XY[0]+ 10*h[0]],[XY[1],XY[1]+ 10*h[1]],'c')
    #plot([XY[0],XY[0]+ m*h[0]],[XY[1],XY[1]+ 10*h[1]],'b')

# width of path
# angles over various distances
# input future navigation commands

    """
    for j in range(start,end,3):
        #plot_line(Pts['xy'][i],Pts['left9_meo'][i+j],'r')
        #plot_line(Pts['xy'][i+j-30],Pts['xy'][i+j],':c')
        pts_plot([Pts['left9_meo'][i+j]],'r')
        pts_plot([Pts['right9_meo'][i+j]],'g')
        pts_plot([Pts['direct9_meo'][i+j]],'b')
        #pts_plot(Pts['xy'][i],Pts['right9_meo'][i+j],'g')
    """
    spause()#raw_enter()
    #time.sleep(1/30.)    

#,b

#EOF
