from kzpy3.vis3 import *

#,a

if not 'from command line': #sys.stdin.isatty():# 
    Arguments = {
        'run_name':'tegra-ubuntu_31Oct18_16h06m32s',
    }
    Defaults = {
        'show':False,
        'show2':False,
        #'backward':50,
        #'forward':250,
        'save':True,
        'start':0,
        'end':-1,
        'istep':1,
        #'halve':True,
    }
else:
    Defaults = {
        'show':False,
        'show2':False,
        #'backward':50,
        #'forward':250,
        'save':True,
        'start':0,
        'end':-1,
        'istep':1,
        #'halve':True,
    }

assert 'run_name' in Arguments
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
save_path = opjD('Data','outer_contours','rotated1',Arguments['run_name']+'.h5py')

if Arguments['save']:
    if os.path.exists(save_path):
        clp('!!!',save_path,'exists!!!','`wrb')
        exit()
if Arguments['save']:
    make_path_and_touch_file(save_path)

def plot_line(A,B,c='r'):
    plot([A[0],B[0]],[A[1],B[1]],c)

def pts_dist(A,B):
    return np.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

Colors = {'direct':'b','left':'r','right':'g'}




if not Arguments['show2']:

    if 'lst' not in locals():
        path = opjD('Data/pts2D_multi_step/pkl/'+Arguments['run_name']+'.pkl')
        #cb(path,ra=1)
        lst = lo(path)

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
        o = loD('Data/pts2D_multi_step/pkl_angles0/'+Arguments['run_name']+'.pkl')
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

marker_size_divisor = 4.0
marker_size = 80/marker_size_divisor


D = {}
D['marker_size'] = {}
D['marker_size']['left'] = []
D['marker_size']['right'] = []
D['outor_contours'] = {}
D['outer_countours_rotated'] = {}
D['angles'] = {}
e = 16

if Arguments['save']:
    frames_per_second = 30
    start = -10*30
    #end = start + 2.5*minutes*30; end = int(end)
    end = start + (14+8) * seconds * frames_per_second; end = int(end)
    step = 30/3
    d = 50
    length = len(range(start,end,step))
    #cm((end-start)/step,ra=1)
    
    
    #CA()




    lenL = len(L['motor'])
    if Arguments['end'] == -1:
        Arguments['end'] = lenL

    M = {
        'valid' : zeros(lenL),
        'angles_left' : zeros((lenL,length)),
        'outer_countours_rotated_left' : zeros((lenL,length,2)),
        'angles_right' : zeros((lenL,length)),
        'outer_countours_rotated_right' : zeros((lenL,length,2)),
        'turns' : zeros((lenL,length)),
    }

    

    timer = Timer(10)
    timer.trigger()

    data = list(zeros(len(L['steer'])))

if not Arguments['show2']:
    for i in range(Arguments['start'],Arguments['end'],Arguments['istep']):#rlen(L['steer']):#range(6500,11000,1):#200000+6500,1):

        if True:#try:

            timer.freq(str(i))

            if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
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



            if Arguments['show']:#not 'plot':


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



            if Arguments['show']:#not 'plot':
                spause()

            
            M['valid'][i] = 1
            for k in ['left','right']:
                M['angles_'+k][i] = D['angles'][k].copy()
                M['outer_countours_rotated_'+k][i] = D['outer_countours_rotated'][k].copy()
                #clp(shape(D['turns']),shape(M['turns'][i]))
                M['turns'][i] = D['turns']

        """
        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        
        except:
            clp(i,'failed','`wrb')
        """
        


    if Arguments['save']:
        save_as_h5py(save_path,M,'float32')



elif Arguments['show2']:

    if 'O' not in locals():
        L,O,___ = open_run2(Arguments['run_name'])

    M = h5r(save_path)

    if Arguments['end'] == -1:
        Arguments['end'] = len(M['outer_countours_rotated_left'])

    for i in range(Arguments['start'],Arguments['end'],Arguments['istep']):

        if not M['valid'][i]:
            continue


        D = {
                'angles' : {
                    'left' :     M['angles_left'][i].copy(),
                    'right' :    M['angles_right'][i].copy(),
                },
                'outer_countours_rotated' : {
                    'left' :     M['outer_countours_rotated_left'][i].copy(),
                    'right' :    M['outer_countours_rotated_right'][i].copy(),
                },
                'marker_size' : {
                    'left' :     M['angles_left'][i].copy(),
                    'right' :    M['angles_right'][i].copy(),
                },
                'turns' : M['turns'][i].copy(),
        }
        #kprint(D,r=1)

        
        for k in ['left','right']:
            for l in rlen(D['marker_size'][k]):
                a = min(np.abs(D['marker_size'][k][l]),80)
                marker_size = int(a/marker_size_divisor)
                D['marker_size'][k][l] = marker_size
     

        if not 'plot non-rotated plot':

            if not 'meter scale bar':
                x = XY[0]; y = XY[1]
                figure(1)
                clf()
                xylim(x-e,x+e,y-e,y+e);plt_square();


            for k in ['left','right']:
                xy = D['outor_contours'][k]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=1)
                for l in rlen(D['marker_size'][k]):
                    pts_plot(D['outor_contours'][k][l],Colors[k],sym='.',ms = D['marker_size'][k][l])


        if not 'plot fit':
            plot(D["Pts['xy'] to fit"][:,0],D["Pts['xy'] to fit"][:,1],'kx')
            plot(D["xs_fit_line"],D["ys_fit_line"],'k:')



        if 'plot rotated' and 'outer_countours_rotated' in D:
            
            figure(2);clf();plt_square(); xylim(-e,e,-e/4,2*e)
            for k in ['left','right']:
                xy = D['outer_countours_rotated'][k]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=1)
                for r in rlen(D['outer_countours_rotated'][k]):
                    pts_plot(D['outer_countours_rotated'][k][r],Colors[k],sym='.',ms = D['marker_size'][k][r])



        if  '1-d plot':
            figure(3);clf()
            for k in ['left','right']:
                x = D['outer_countours_rotated'][k][:,0]
                plot(x,Colors[k]+'x-')
                y = D['outer_countours_rotated'][k][:,1]
                plot(y,Colors[k]+'.-')
                plot(D['angles'][k]/10.,Colors[k]+'-')

            plot(D['turns'],'c.-')


        spause()
        

        if 'show camera image':
            img = O['left_image']['vals'][i]
            img = cv2.resize(img,(168*2,94*2))
            if False: img[:,168,:] = int((127+255)/2)
            mci(img,title='left_image',scale=1.)



#,b

#EOF
