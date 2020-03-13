from kzpy3.vis3 import *

if False:
    import fit3d#_torch as fit3d

    ##############################################################
    ##############################################################
    ##
    Colors = {'direct':'b','left':'r','right':'g'}
    RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}
    Color_index = {'direct':2,'right':1,'left':0}
    ##
    ##############################################################
    ##############################################################


    ##############################################################
    ##############################################################
    ###


#,a

P = {
    'vel-encoding coeficient':  1.0/2.3,
    'vec sample frequency': 30,#3.33,
}


def vec(heading,encoder,motor,sample_frequency,P):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)


def f(x,A,B):
    return A*x + B


def get_predictions2D(headings,encoders,motors,sample_frequency,P):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],P['vec sample frequency'],P) #3.33)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step

run_path = opjh('Desktops_older',
        'Desktop_19Feb19_08h49m53s',
        'model_car_data_July2018_lrc',
        'locations/local/left_right_center/h5py',
        'Mr_Black_24Jul18_20h04m17s_local_lrc',
        )

if 'L' not in locals():
    L = h5r(opj(
        run_path,
        'left_timestamp_metadata_right_ts.h5py'
    ))
if 'O' not in locals():
    O = h5r(opj(
        run_path,
        'original_timestamp_data.h5py'
        ))

h = L['gyro_heading_x'][:]
e = L['encoder'][:]
em = L['encoder_meo'][:]
m = L['motor'][:]

pts = get_predictions2D(h,e,m,30,P)
slow_pts = []
for i in rlen(pts):
    if em[i] < 0.25:
        slow_pts.append(pts[i]) 


def get_index_of_nearest_point(pts,p):
    min_dist = 10**30
    min_indx = -999
    def dist(a,b):
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    for i in rlen(pts):    
        d = dist(pts[i,:],p)
        if d < min_dist:
            min_indx = i
            min_dist = d
    assert(i >= 0 and i < len(pts))
    return min_indx

    


n = 30*30
m = 50
CA()
for i in range(50): 
    clf()
    fig = figure(1)
    pts_plot(pts,sym=',',color='b')
    pts_plot(slow_pts,sym=',',color='r')
    plot(pts[0,0],pts[0,1],'og')
    plot(pts[-1,0],pts[-1,1],'or')
    plt_square()
    xylim(min(pts[:,0])-m,max(pts[:,0])+m,min(pts[:,1])-m,max(pts[:,1])+m)
    Cdat = Click_Data(FIG=fig,NO_SHOW=True)
    xy_list = Cdat['CLICK'](NUM_PTS=1)
    if None in xy_list[0]:
        print('done.')
        break
    indx = get_index_of_nearest_point(pts,xy_list[0])
    pts_plot([pts[indx,:]],sym='.',color='g')
    spause()
    xy_list = Cdat['CLICK'](NUM_PTS=1)
    if None in xy_list[0]:
        print('done.')
        break
    indx2 = get_index_of_nearest_point(pts,xy_list[0])
    pts_plot([pts[indx2,:]],sym='.',color='r')

    if indx > indx2:
        clp(' Warning, indicies reversed to have time direction correct ','`wrb')
        a = indx2
        indx2 = indx
        indx = a

    spause()
    r = raw_input('enter to continue, q to reclick => ')
    if r == 'q':
        continue
    
    xs = pts[indx:indx2,0]
    ys = pts[indx:indx2,1]
    
    
    xylim(min(xs)-10,max(xs)+10,min(ys)-10,max(ys)+10)
    pts_plot(slow_pts,sym='x',color='r')
    figure(2)
    clf()
    plot(h[indx:indx2],',')
    spause();
    figure(1)
    spause()
    try:
        for j in range(indx,indx2):
            if not np.mod(j,30*5):
                #print j
                plot(pts[j,0],pts[j,1],'.k')
                #pts_plot([pts[j,:]],sym='.',color='k')
                spause()
            mci(O['left_image']['vals'][j],delay=33)
        raw_enter()
    except:
        print('exception')


        
#,b
if False:
    for i in range(1000,len(a),1000):
        plot(a[i-1000,0],a[i-1000,1],'r.')
        plot(a[i,0],a[i,1],'k.')
        spause()
raw_enter()

if False:
    zeros_23_41_3 = np.zeros((23,41,3))


    def get_prediction_images_3D(pts2D_1step_list,img,P):
        rmax = 7
        metadata_version_list = []
        img2 = zeros_23_41_3.copy()

        for q in range(len(pts2D_1step_list)-1,-1,-1):
            Pts2D_1step = pts2D_1step_list[q]

            for behavioral_mode in Pts2D_1step.keys():
                pts2D_1step = Pts2D_1step[behavioral_mode]
                for i in rlen(pts2D_1step):
                    a = pts2D_1step[i,:]
                    if a[1]<0:
                        continue
                    if P['graphics 3']:
                        try:
                            r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
                        except:
                            r = 1
            
                    b = fit3d.Point3(a[0], 0, a[1]-P['backup parameter'])
                    c = fit3d.project(b, fit3d.mat)

                    try:

                        good = True

                        if c.x < 0 or c.x >= 168:
                            good = False
                        elif c.y < 0 or c.y >= 94:
                            good = False

                        if good and P['graphics 3']:             
                            if r < rmax:
                                cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])

                        if P['graphics 2']:
                            good = True
                            cx = intr(c.x * 0.245)
                            cy = intr(c.y * 0.245)
                            if cx < 0 or cx >= 41:
                                good = False
                            elif cy < 0 or cy >= 23:
                                good = False
                            if good:               
                                img2[cy,cx,Color_index[behavioral_mode]] += q**2/(P['num timesteps']**2.0)

                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        CS_('Exception!',emphasis=True)
                        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                        cr(r)

        if P['graphics 3']:
            img = cv2.resize(img,(168*2,94*2))
            if P['use center line']:
                img[:,168,:] = int((127+255)/2)
            left_camera_3D_img = img
        else:
            left_camera_3D_img = False

        if P['graphics 2']:
            for y in range(11,23):
                for c in range(3):
                    if img2[y,:,c].max() > 0:
                        img2[y,:,c] = z2o(img2[y,:,c])
            metadata_3D_img = z55(img2)
        else:
            metadata_3D_img = False

        return left_camera_3D_img,metadata_3D_img
    ##
    ##############################################################
    ##############################################################
    ###
    def get__pts2D_multi_step(d_heading,encoder,sample_frequency,headings,encoders,motors,pts2D_multi_step,P):

        Pts2D_1step = {}

        for behavioral_mode in P['behavioral_mode_list']:

            Pts2D_1step[behavioral_mode] = \
                get_predictions2D(
                    headings[behavioral_mode],
                    encoders[behavioral_mode],
                    motors[behavioral_mode],
                    sample_frequency,
                    P)
        
        pts2D_multi_step.append({})

        for behavioral_mode in P['behavioral_mode_list']:
            
            if len(pts2D_multi_step) > P['num timesteps']:
                pts2D_multi_step = pts2D_multi_step[-P['num timesteps']:]

            pts2D_multi_step[-1][behavioral_mode] = Pts2D_1step[behavioral_mode] #list(Pts2D_1step[behavioral_mode])

        velocity = encoder * P['vel-encoding coeficient']

        trajectory_vector = na([0,1]) * velocity / sample_frequency

        for behavioral_mode in P['behavioral_mode_list']:

            for i in rlen(pts2D_multi_step):
                pts2D_multi_step[i][behavioral_mode] = rotatePolygon(pts2D_multi_step[i][behavioral_mode],-d_heading*P['d_heading_multiplier'])

            pts2D_multi_step[-1][behavioral_mode].append(trajectory_vector)

            for i in rlen(pts2D_multi_step):

                pts2D_multi_step[i][behavioral_mode] = pts2D_multi_step[i][behavioral_mode] - pts2D_multi_step[-1][behavioral_mode][-1]

        return pts2D_multi_step
    ###
    ##############################################################




    ################################################################
    ################################################################
    ###
    def prepare_2D_and_3D_images(Prediction2D_plot,pts2D_multi_step,d_heading,encoder,sample_frequency,headings,encoders,motors,img,P):

        pts2D_multi_step = get__pts2D_multi_step(d_heading,encoder,sample_frequency,headings,encoders,motors,pts2D_multi_step,P)

        if P['graphics 1']:
            Prediction2D_plot['clear']()

            for behavioral_mode in P['behavioral_mode_list']:

                for i in rlen(pts2D_multi_step):

                    Prediction2D_plot['pts_plot'](na(pts2D_multi_step[i][behavioral_mode]),Colors[behavioral_mode],add_mode=P['add_mode'])



        left_camera_3D_img,metadata_3D_img = get_prediction_images_3D(pts2D_multi_step,img,P)

        return Prediction2D_plot,left_camera_3D_img,metadata_3D_img
    ###
    ################################################################
    ################################################################
    ###
    def show_maybe_save_images(Prediction2D_plot,left_camera_3D_img,metadata_3D_img,P):

        if P['save metadata']:
            metadata_img_list[left_index] = metadata_3D_img

        if P['show timer'].check():
            P['show timer'] = Timer(P['show timer time'])
            if P['graphics 1']:
                img = Prediction2D_plot['image']
                img = z55(np.log10(1.0*img+1.0)*10.0)
                img = cv2.resize(img, (0,0), fx=4, fy=4, interpolation=0)
                img[4*41+1,:,:] = 128
                img[:,4*31+1,:] = 128
                mci(img,title='X',scale=1)

            if P['graphics 3']:
                mci(left_camera_3D_img,title='left_camera_3D_img',delay=P['cv2 delay'],scale=P['3d image scale'])
            if False:#P['graphics 2']: 
                mci(metadata_3D_img,title='metadata_3D_img',delay=P['cv2 delay'],scale=P['metadata_3D_img scale'])
    ###
    ################################################################
    ################################################################
    ################################################################
    ###
