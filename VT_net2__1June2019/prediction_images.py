from kzpy3.vis3 import *

import kzpy3.misc.fit3d as fit3d#_torch as fit3d

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
def vec(heading,encoder,motor,sample_frequency,P):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)



def get_predictions2D(headings,encoders,motors,sample_frequency,P):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],P['vec sample frequency'],P) #3.33)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step




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





def point_in_3D_to_point_in_2D(a,backup_parameter=1.):
    if a[1]<0:
        return False,False

    b = fit3d.Point3(a[0], 0, a[1]-backup_parameter)
    c = fit3d.project(b, fit3d.mat)

    if c.x < 0 or c.x >= 168:
        return False,False

    elif c.y < 0 or c.y >= 94:
        return False,False

    return c.x,c.y

##############################################################
###



def non_linear_fit(vel):
    q = 4.078*vel + 2.978
    if q > 5.75:
        return 5.75
    elif q < 0.25:
        return 0.25
    else:
        return q
def non_linear_correction(vel):
    return 5.75/non_linear_fit(vel)


def get__path_pts2D(
    d_heading,
    encoder,
    sample_frequency,
    direction,
    value,
    Path_pts2D,
    P
):
    # 226.5 inches = 5.75 meters, .338 meters per tile
    velocity = encoder * P['vel-encoding coeficient'] * direction
    velocity = non_linear_correction(velocity)

    P['velocity'] = velocity

    magnitude = velocity / sample_frequency

    trajectory_vector = na([0,1]) * magnitude

    P['distance'] += magnitude# / sample_frequency

    try:
        Path_pts2D['rotate'](-d_heading / sample_frequency * P['d_heading_multiplier'])
    except:
        pass

    Path_pts2D['append'](trajectory_vector,value,{'velocity':velocity})

    Path_pts2D['zero']()

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

#EOF
