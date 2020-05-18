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
end = start + 1*60*30
step = 30/3
d = 50
marker_size = 40

CA()


fig = 4

for i in range(6500,7000):#200000+6500,1):

    if True:
        XY = Pts['xy'][i]
        figure(1,figsize=(16,16));clf();
        plot((-41,-40),(3,3),'k',linewidth=1)
        #plt.text(5-1,-2,'10 m')
    
    if False:
        xy = na(Pts['xy'][i-15:i+1])
        plot(xy[:,0],xy[:,1],'k')

    if fig in [3,4]:
        for k in Colors.keys():
            xy = Pts[k+'9_meo'][i+start:i+end:step]
            plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=3)




    cy(i)

    for j in range(i+start,i+end,1):#step):


        cg(i,j)

        if fig in [0,1,2]:
            xy = na([Pts['direct0_meo'][j]])
            plot(xy[:,0],xy[:,1],'k.')

        if j % step != 0:
            continue
        
        if fig in [1,2,3]: # trajectories
            for k in Colors:
                m = []
                for l in range(10):
                    xy = Pts[k+str(l)+'_meo'][j+l]
                    m.append(xy)
                    #cm(i,l,xy)
                pts_plot(m,Colors[k],sym='-')

        if False:
            if Pts['angles_meo']['left'][j] < -40:
                pts_plot(Pts['left9_meo'][j],'r',sym='.',ms=marker_size)
            elif Pts['angles_meo']['left'][j] < -20:
                pts_plot(Pts['left9_meo'][j],'r',sym='.',ms=int(marker_size/2))

            if Pts['angles_meo']['right'][j] > 40:
                pts_plot(Pts['right9_meo'][j],'g',sym='.',ms=marker_size)
            elif Pts['angles_meo']['right'][j] > 20:
                pts_plot(Pts['right9_meo'][j],'g',sym='.',ms=int(marker_size/2))

        if fig in [2,3,4]: # markers
            for k in ['left','right']:
                a = min(np.abs(Pts['angles_meo'][k][j]),40)
                marker_size = int(a/2.)
                pts_plot(Pts[k+'9_meo'][j],Colors[k],sym='.',ms=marker_size)

        if False:
            E = Pts['left9_meo'][j]#+step]
            R = Pts['right9_meo'][j]#+step]
            D = Pts['direct9_meo'][j]
            plot_line(R,D,'g:')
            plot_line(E,D,'r:')


        if False:
            pts_plot(Pts['xy'][j],'k')
    
    plt_square(); #xylim(XY[0]-d,XY[0]+d,XY[1]-d,XY[1]+d)

    spause()

    if False:
        e = 15
        figure(2);clf();plt_square(); xylim(-e,e,-e/4,2*e)
        A = Pts['direct9_meo'][i+start] - Pts['direct9_meo'][i+start-2]
        alpha = angle_clockwise((0,1),A)
        for k in Colors:
            pts_plot(
                rotatePolygon(
                    Pts[k+'9_meo'][i+start:i+end:step] -Pts['direct9_meo'][i+start-1],alpha),
                Colors[k],sym='.-')

    if False:
        img = O['left_image']['vals'][i]
        img = cv2.resize(img,(168*2,94*2))
        if False: img[:,168,:] = int((127+255)/2)
        mci(img,title='left_image',scale=1.)

    break #clp('',r=1)

xylim(-47,-37,0,9)
    
if False:
    plt.savefig(opjD('a'),format='pdf')

# width of path
# angles over various distances
# input future navigation commands


def nearest_xy_index(xy):
    XY = (-999,-999)
    indx = -999
    dmin = 9999
    for i in rlen(Pts['xy']):
        d = pts_dist(xy,Pts['xy'][i])
        if d < dmin:
            dmin = d
            XY = Pts['xy'][i]
            indx = i
            #print i,d,indx
    assert indx != -999
    return indx


if False:
    Cdat = Click_Data(FIG=figure(1))
    path = opjD(d2p('click',time_str()))
    os.system('mkdir -p ' + path)
    for i in range(30):
        xy_list = Cdat['CLICK'](NUM_PTS=1)
        plt.text(xy_list[0][0],xy_list[0][1],str(i))
        indx = nearest_xy_index(xy_list[0])
        img = O['left_image']['vals'][indx]
        #img = cv2.resize(img,(168*2,94*2))
        #if False: img[:,168,:] = int((127+255)/2)
        mci(img,title='left',scale=2.)
        imsave(opj(path,d2n(i,'_',dp(xy_list[0][0]),'_',dp(xy_list[0][1]),'.png')),img,format='png')
    plt.savefig(opj(path,'map.pdf'),format='pdf')



#,b

#EOF
