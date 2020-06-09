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
        n = 33
        for side in ['left','direct','right']:
            for u in range(10):
                cm(side,u)
                a = Pts[side][u]
                ax = meo(na(a)[:,0],n)
                ay = meo(na(a)[:,1],n)
                Pts[side+str(u)+'_meo'] = na([ax,ay]).transpose()
        if False:
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
end = start + 2.5*minutes*30; end = int(end)
step = 30/3
d = 50
marker_size = 40

CA()


for fig in range(5):

    for i in range(6500,7000):#200000+6500,1):

        if True:
            XY = Pts['xy'][i]
            figure(1,figsize=(16,16));clf();
            plot((-41,-40),(3,3),'k',linewidth=1)
        

        if fig in [3,4]:
            for k in ['left','right']:
                xy = Pts[k+'9_meo'][i+start:i+end:step]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=3)




        cy(i)

        for j in range(i+start,i+end,1):


            cg(i,j)

            if fig in [0]:
                xy = na([Pts['direct0_meo'][j]])
                plot(xy[:,0],xy[:,1],'k.')

            if j % step != 0:
                continue
            
            if fig in [1,2,3]: # dead-reckoning trajectory
                for k in ['left','right']:
                    m = []
                    for l in range(10):
                        xy = Pts[k+str(l)+'_meo'][j+l]
                        m.append(xy)
                    pts_plot(m,Colors[k],sym='-')



            if fig in [2,3,4]: # markers
                for k in ['left','right']:
                    a = min(np.abs(Pts['angles_meo'][k][j]),40)
                    marker_size = int(a/2.)
                    pts_plot(Pts[k+'9_meo'][j],Colors[k],sym='.',ms=marker_size)


        
        plt_square()

        spause()





        break

    spause()
    plt.savefig(opjD('fig'+str(fig)+'a.pdf'),format='pdf')
    xylim(-47,-37,0,9)
    plt.savefig(opjD('fig'+str(fig)+'b.pdf'),format='pdf')
    








#,b

#EOF
