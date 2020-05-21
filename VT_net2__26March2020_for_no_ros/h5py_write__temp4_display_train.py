from kzpy3.vis3 import *

#, a


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
        L,O,___ = open_run2(Arguments['run_name'])

frames_per_second = 30
start = -2*30
#end = start + 2.5*minutes*30; end = int(end)
end = start + 14 * seconds * frames_per_second; end = int(end)
step = 30/3
d = 50
marker_size_divisor = 4.0
marker_size = 80/marker_size_divisor
CA()


for fig in [4]:#range(5):

    for i in range(6500,11000,1):#200000+6500,1):

        if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
            cm(i,'motor/encoder')
            continue

        if 'find i_back':
            A = Pts['direct9_meo'][i-90]
            i_back = i-1-90
            while True:
                #B = Pts['xy'][i_back]
                B = Pts['direct9_meo'][i_back]
                pd = pts_dist(A,B)
                if pd > 0.5:
                    #print k,i,dp(pd)
                    break
                else:
                    i_back -= 1

            if i - i_back > 200:
                cm(i,'i_back')
                continue


        if 'meter scale bar':
            XY = Pts['xy'][i]
            figure(1,figsize=(16,16));clf();xylim(-100,100,-150,50);plt_square();
            plot((-41,-40),(3,3),'k',linewidth=1)
            #plt.text(5-1,-2,'10 m')
        
        if not 'Pts[xy]':
            xy = na(Pts['xy'][i-15:i+1])
            plot(xy[:,0],xy[:,1],'k')

        if fig in [3,4]:
            for k in ['left','right']:#Colors.keys():
                xy = Pts[k+'9_meo'][i+start:i+end:step]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=1)




        cy(i)

        for j in range(i+start,i+end,1):#step):


            cg(i,j)

            if fig in [0]:
                xy = na([Pts['direct0_meo'][j]])
                plot(xy[:,0],xy[:,1],'k.')

            if j % step != 0:
                continue
            
            if fig in [1,2,3]: # trajectories
                for k in ['left','right']:
                    m = []
                    for l in range(10):
                        xy = Pts[k+str(l)+'_meo'][j+l]
                        m.append(xy)
                        #cm(i,l,xy)
                    pts_plot(m,Colors[k],sym='-')



            if fig in [2,3,4]: # markers
                for k in ['left','right']:
                    a = min(np.abs(Pts['angles_meo'][k][j]),40)
                    marker_size = int(a/marker_size_divisor)
                    pts_plot(Pts[k+'9_meo'][j],Colors[k],sym='.',ms=marker_size)


        

        if 'show camera image':
            img = O['left_image']['vals'][i]
            img = cv2.resize(img,(168*2,94*2))
            if False: img[:,168,:] = int((127+255)/2)
            mci(img,title='left_image',scale=1.)



        if 'get slope, alpha':
            xy = na(Pts['xy'][i_back+90:i+1:1])
            plot(xy[:,0],xy[:,1],'kx')

            m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
            xs = na([XY[0]-20,XY[0]+20])
            ys = m * xs + b
            plot(xs,ys,'k:')

            #alpha_prev = alpha
            alpha = angle_clockwise((1,0),(1,m))

            if False:
                if np.abs(alpha - alpha_prev) > 5:
                    cs = '`wrb'
                    ra = True
                else:
                    cs = '`m'
                    ra = False





        spause()








        #break #clp('',r=1)

    spause()
    if False:
        plt.savefig(opjD('fig'+str(fig)+'a.pdf'),format='pdf')
        xylim(-47,-37,0,9)
        plt.savefig(opjD('fig'+str(fig)+'b.pdf'),format='pdf')
    
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



#,a
def corrected_angle(m,point,origin):

    alpha = angle_clockwise((1,0),(1,m))

    x = point[0]-origin[0]
    y = point[1]-origin[1]

    if x >= 0 and y >= 0:
        alpha = 360 - alpha
    elif x < 0 and y >= 0:
        alpha = 180 - alpha
    elif x < 0 and y < 0:
        alpha = 180+360 - alpha
    elif x >= 0 and y < 0:
        alpha = 90-alpha+270
    else:
        assert False

    return alpha



xsq = [ 1, 2, 3,  3, 3, 3,3,3,3, 2,1,0.01, -1,-2,-3, -3,-3, -3,  -3,-3,-3,  -2,-1, -0.01]
ysq = [-3,-3,-3, -2,-1, 0,1,2,3, 3,3,3,  3, 3, 3,  2, 1,  0,  -1,-2,-3,  -3,-3,-3]

ysq = 5.0*np.sin(arange(0,3*np.pi,0.03))
xsq = 5.0*np.cos(arange(0,3*np.pi,0.03))
ysq = ysq + 0.001*rndn(len(ysq))
xsq = xsq + 0.001*rndn(len(xsq))

for q in rlen(xsq):

    xy = [[0,0],[xsq[q],ysq[q]]]

    xy = na(xy)

    m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
    xs = na([-6,6])
    ys = m * xs + b

    clf();plt_square();xylim(-6,6,-6,6)
    plot(xsq,ysq,'b.')
    plot(xsq[q],ysq[q],'ro')
    plot(xs,ys,'k:')
    plot(0,0,'ko')
    
    spause()

    if False:
        #alpha_prev = alpha
        alpha = angle_clockwise((1,0),(1,m))
        cm([dp(xsq[q]),dp(ysq[q])],'m:',dp(m),'b:',dp(b),'alpha:',np.round(alpha),r=1)
        if xsq[q] >= 0 and ysq[q] >= 0:
            cy(int(360-alpha),sf=0)
        elif xsq[q] < 0 and ysq[q] >= 0:
            cg(int(180-alpha),sf=0)
        elif xsq[q] < 0 and ysq[q] < 0:
            cb(int(180+360-alpha),sf=0)
        elif xsq[q] >= 0 and ysq[q] < 0:
            cm(int(90-alpha+270),sf=0)
    print dp( corrected_angle(m, (xsq[q],ysq[q]), (0,0)) )

if np.abs(alpha - alpha_prev) > 5:
    cs = '`wrb'
    ra = True
else:
    cs = '`m'
    ra = False

spause()
#,b

#EOF
