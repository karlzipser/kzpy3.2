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
#CA()



D = {}
D['marker_size'] = {}
D['marker_size']['left'] = []
D['marker_size']['right'] = []
D['outor_contours'] = {}
D['outer_countours_rotated'] = {}
D['angles'] = {}

lenL = len(L['motor'])

M = {
    'valid' : zeros(lenL),
    'angles_left' : zeros((lenL,42)),
    'outer_countours_rotated_left': zeros((lenL,42,2)),
    'angles_right' : zeros((lenL,42)),
    'outer_countours_rotated_right': zeros((lenL,42,2)),
}

e = 16

timer = Timer(10)
timer.trigger()

data = list(zeros(len(L['steer'])))

for i in rlen(L['steer']):#range(6500,11000,1):#200000+6500,1):

    timer.freq(str(i))
    #cm(i)

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        #cm(i,'motor/encoder')
        #data.append(None)
        continue


    if 'find i_back':
        A = Pts['direct9_meo'][i-90]
        i_back = i-1-90
        while True:
            B = Pts['direct9_meo'][i_back]
            pd = pts_dist(A,B)
            if pd > 0.5:
                break
            else:
                i_back -= 1

        if i - i_back > 200:
            #cm(i,'i_back')
            continue



    XY = Pts['xy'][i]

    
    if not 'Pts[xy]':
        xy = na(Pts['xy'][i-15:i+1])
        plot(xy[:,0],xy[:,1],'k')



    if 'outer countors':
        
        for k in ['left','right']:

            D['outor_contours'][k] = Pts[k+'9_meo'][i+start:i+end:step]


    if 'markers':

        for k in ['left','right']:

            D['marker_size'][k] = Pts['angles_meo'][k][i+start:i+end:step]
            for l in rlen(D['marker_size'][k]):
                a = min(np.abs(D['marker_size'][k][l]),80)
                marker_size = int(a/marker_size_divisor)
                D['marker_size'][k][l] = marker_size

            D['angles'][k] = na(Pts['angles_meo'][k][i+start:i+end:step])



    if 'find turns':

        aa = L['gyro_heading_x_meo'][i+start:i+end:step]
        bb = L['gyro_heading_x_meo'][i+start-step:i+end-step:step]
        cc = aa - bb
        dd = L['behavioral_mode'][i+start:i+end:step]
        ee = 0 * dd
        ee[ cc > 5 ] = 3 - 2
        ee[ cc < -5] = 1 - 2
        ff = 0 * dd
        ff[dd == 1] = 1
        ff[dd == 3] = 1
        gg = ee * ff + 2


        D['turns'] = gg

                
    if 'make rotated':

        if 'get slope, alpha':
            xy = na(Pts['xy'][i_back+90:i+1:1])
            D["Pts['xy'] to fit"] = xy
            
            m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
            xs = na([XY[0]-20,XY[0]+20])
            ys = m * xs + b
            D["xs_fit_line"] = xs
            D["ys_fit_line"] = ys
            
            alpha = corrected_angle(m,xy[-1,:],xy[0,:])

        for k in ['left','right']:
            D['outer_countours_rotated'][k] = \
                rotatePolygon( D['outor_contours'][k] - A, 90-alpha)



    if not 'plot':


        if 'plot non-rotated plot':

            if 'meter scale bar':
                x = XY[0]; y = XY[1]
                figure(1)
                clf()
                xylim(x-e,x+e,y-e,y+e);plt_square();


            for k in ['left','right']:
                xy = D['outor_contours'][k]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=1)
                for l in rlen(D['marker_size'][k]):
                    pts_plot(D['outor_contours'][k][l],Colors[k],sym='.',ms = D['marker_size'][k][l])

        if 'plot fit':
            plot(D["Pts['xy'] to fit"][:,0],D["Pts['xy'] to fit"][:,1],'kx')
            plot(D["xs_fit_line"],D["ys_fit_line"],'k:')



        if 'plot rotated' and 'outer_countours_rotated' in D:
            
            figure(2);clf();plt_square(); xylim(-e,e,-e/4,2*e)
            for k in ['left','right']:
                xy = D['outer_countours_rotated'][k]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=1)
                for r in rlen(D['outer_countours_rotated'][k]):
                    pts_plot(D['outer_countours_rotated'][k][r],Colors[k],sym='.',ms = D['marker_size'][k][r])



        if '1-d plot':
            figure(3);clf()
            for k in ['left','right']:
                x = D['outer_countours_rotated'][k][:,0]
                plot(x,Colors[k]+'x-')
                y = D['outer_countours_rotated'][k][:,1]
                plot(y,Colors[k]+'.-')
                plot(D['angles'][k]/10.,Colors[k]+'-')

            plot(D['turns'],'c.-')



        if 'show camera image':
            img = O['left_image']['vals'][i]
            img = cv2.resize(img,(168*2,94*2))
            if False: img[:,168,:] = int((127+255)/2)
            mci(img,title='left_image',scale=1.)



    if not 'plot':
        spause()

    data[i] = {
        'outer_countours_rotated' : D['outer_countours_rotated'],
        'angles' : D['angles'],
        'turns' : D['turns'],
        'angles' : D['angles'],
        'index' : i,
        }
    
    M['valid'][i] = 1
    for k in ['left','right']:
        M['angles_'+k][i] = D['angles'][k].copy()
        M['outer_countours_rotated_'+k][i] = D['outer_countours_rotated'][k].copy()













if False:

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



    spause()
#,b

#EOF
