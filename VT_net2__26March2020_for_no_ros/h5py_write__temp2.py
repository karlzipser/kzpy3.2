from kzpy3.vis3 import *


#,a

def pts_dist(a,b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


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


if 'direct9_meo' not in Pts:
    n = 33
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

for i in range(6500,2000+6500,1):

    figure(1);clf();plt_square(); xylim(-50,-20,-10,10)

    pts_plot(Pts['xy'][i-200:i+200],'b')
    pts_plot(Pts['left9_meo'][i-200:i+200],'r')
    pts_plot(Pts['right9_meo'][i-200:i+200],'g')

    spause()#raw_enter()
    time.sleep(1/30.)    

#,b

#EOF
