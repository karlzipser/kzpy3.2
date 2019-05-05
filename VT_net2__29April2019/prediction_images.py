from kzpy3.vis3 import *

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
def vec(heading,encoder,motor,sample_frequency,_):
    velocity = encoder * _['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)


def f(x,A,B):
    return A*x + B


def get_predictions2D(headings,encoders,motors,sample_frequency,_):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],_['vec sample frequency'],_) #3.33)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step




zeros_23_41_3 = np.zeros((23,41,3))


def get_prediction_images_3D(pts2D_1step_list,img,_):
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
                if _['graphics 3']:
                    try:
                        r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
                    except:
                        r = 1
        
                b = fit3d.Point3(a[0], 0, a[1]-_['backup parameter'])
                c = fit3d.project(b, fit3d.mat)

                try:

                    good = True

                    if c.x < 0 or c.x >= 168:
                        good = False
                    elif c.y < 0 or c.y >= 94:
                        good = False

                    if good and _['graphics 3']:             
                        if r < rmax:
                            cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])

                    if _['graphics 2']:
                        good = True
                        cx = intr(c.x * 0.245)
                        cy = intr(c.y * 0.245)
                        if cx < 0 or cx >= 41:
                            good = False
                        elif cy < 0 or cy >= 23:
                            good = False
                        if good:               
                            img2[cy,cx,Color_index[behavioral_mode]] += q**2/(_['num timesteps']**2.0)

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                    cr(r)

    if _['graphics 3']:
        img = cv2.resize(img,(168*2,94*2))
        if _['use center line']:
            img[:,168,:] = int((127+255)/2)
        left_camera_3D_img = img
    else:
        left_camera_3D_img = False

    if _['graphics 2']:
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
def get__pts2D_multi_step(d_heading,encoder,sample_frequency,headings,encoders,motors,pts2D_multi_step,_):

    Pts2D_1step = {}

    for behavioral_mode in _['behavioral_mode_list']:

        Pts2D_1step[behavioral_mode] = \
            get_predictions2D(
                headings[behavioral_mode],
                encoders[behavioral_mode],
                motors[behavioral_mode],
                sample_frequency,
                _)
    
    pts2D_multi_step.append({})

    for behavioral_mode in _['behavioral_mode_list']:
        
        if len(pts2D_multi_step) > _['num timesteps']:
            pts2D_multi_step = pts2D_multi_step[-_['num timesteps']:]

        pts2D_multi_step[-1][behavioral_mode] = Pts2D_1step[behavioral_mode] #list(Pts2D_1step[behavioral_mode])

    velocity = encoder * _['vel-encoding coeficient']

    trajectory_vector = na([0,1]) * velocity / sample_frequency

    for behavioral_mode in _['behavioral_mode_list']:

        for i in rlen(pts2D_multi_step):
            pts2D_multi_step[i][behavioral_mode] = rotatePolygon(pts2D_multi_step[i][behavioral_mode],-d_heading*_['d_heading_multiplier'])

        pts2D_multi_step[-1][behavioral_mode].append(trajectory_vector)

        for i in rlen(pts2D_multi_step):

            pts2D_multi_step[i][behavioral_mode] = pts2D_multi_step[i][behavioral_mode] - pts2D_multi_step[-1][behavioral_mode][-1]

    return pts2D_multi_step
###
##############################################################

#rotate





def Array(max_len,n_dims):#,n_code_dims=0):
    D = {}
    D['max_len'] = max_len
    D['n_dims'] = n_dims
    #D['n_code_dims'] = n_code_dims
    D['data'] = zeros((2*max_len,n_dims+1+1))#+n_code_dims))
    D['array'] = D['data'][:,:n_dims]
    D['keys'] = D['data'][:,-1]
    D['code'] = D['data'][:,n_dims]#:n_dims+n_code_dims]
    D['ctr'] = 0
    D['key_ctr'] = 0
    D['Dic'] = {}

    def function_check_len():
        ctr = D['ctr']
        max_len = D['max_len']
        #cm(max_len,ctr-max_len,ctr)
        if ctr > 1.5*max_len:
            cm(max_len,ctr-max_len,ctr)
            D['data'][:max_len,:] = D['data'][ctr-max_len:ctr,:]
            D['data'][-max_len:,:] = 0
            D['ctr'] = max_len
            cy(ctr)
            kys = list(D['keys'])
            for k in D['Dic'].keys():
                if k not in kys:
                    del D['Dic'][k]

    #zero_code_array = zeros(n_code_dims)

    def function_append(a,code,dic_info=None):#,code_array=zero_code_array,dic_info=None):
        function_check_len()
        ctr = D['ctr']
        D['array'][ctr,:] = a
        D['keys'][ctr] = D['key_ctr']
        D['code'][ctr] = code #code_array
        D['Dic'][D['key_ctr']] = dic_info
        D['ctr'] += 1
        D['key_ctr'] += 1

    def function_rotate(deg):
        rotatePolygon__array_version(D['array'],deg)

    def function_zero():
        D['array'][:D['ctr'],:] -= D['array'][D['ctr']-1] #path_pts2D[-1]

    D['append'] = function_append
    D['rotate'] = function_rotate
    D['zero'] = function_zero

    return D

if False:
    A = Array(7,2)#,2) 
    for i in range(50):
        A['append'](na([i,i]),np.random.randint(4),i*i)
        A['rotate'](1.)
        A['zero']()
        cg(A['data'],ra=1)




##############################################################
###
def _get__path_pts2D(d_heading,encoder,sample_frequency,direction,path_pts2D,_):

    #d_heading *= direction # test only

    velocity = encoder * _['vel-encoding coeficient'] * direction

    trajectory_vector = na([0,1]) * velocity / sample_frequency

    try:
        path_pts2D = rotatePolygon(path_pts2D,-d_heading*_['d_heading_multiplier'])
    except:
        pass
    path_pts2D.append(trajectory_vector)

    path_pts2D = na(path_pts2D)

    path_pts2D -= path_pts2D[-1]

    return list(path_pts2D)
###
##############################################################

##############################################################
###
def get__path_pts2D(d_heading,encoder,sample_frequency,direction,Path_pts2D,_):

    velocity = encoder * _['vel-encoding coeficient'] * direction

    trajectory_vector = na([0,1]) * velocity / sample_frequency

    try:
        Path_pts2D['rotate'](-d_heading*_['d_heading_multiplier'])
    except:
        pass
    #print direction,encoder
    if direction < 0 or encoder < 0.1:
        val = -1
    else:
        val = 1
    Path_pts2D['append'](trajectory_vector,val)

    Path_pts2D['zero']()

###
##############################################################

################################################################
################################################################
###
def prepare_2D_and_3D_images(Prediction2D_plot,pts2D_multi_step,d_heading,encoder,sample_frequency,headings,encoders,motors,img,_):

    pts2D_multi_step = get__pts2D_multi_step(d_heading,encoder,sample_frequency,headings,encoders,motors,pts2D_multi_step,_)

    if _['graphics 1']:
        Prediction2D_plot['clear']()

        for behavioral_mode in _['behavioral_mode_list']:

            for i in rlen(pts2D_multi_step):

                Prediction2D_plot['pts_plot'](na(pts2D_multi_step[i][behavioral_mode]),Colors[behavioral_mode],add_mode=_['add_mode'])



    left_camera_3D_img,metadata_3D_img = get_prediction_images_3D(pts2D_multi_step,img,_)

    return Prediction2D_plot,left_camera_3D_img,metadata_3D_img
###
################################################################
################################################################
###
def show_maybe_save_images(Prediction2D_plot,left_camera_3D_img,metadata_3D_img,_):

    if _['save metadata']:
        metadata_img_list[left_index] = metadata_3D_img

    if _['show timer'].check():
        _['show timer'] = Timer(_['show timer time'])
        if _['graphics 1']:
            img = Prediction2D_plot['image']
            img = z55(np.log10(1.0*img+1.0)*10.0)
            img = cv2.resize(img, (0,0), fx=4, fy=4, interpolation=0)
            img[4*41+1,:,:] = 128
            img[:,4*31+1,:] = 128
            mci(img,title='X',scale=1)

        if _['graphics 3']:
            mci(left_camera_3D_img,title='left_camera_3D_img',delay=_['cv2 delay'],scale=_['3d image scale'])
        if False:#_['graphics 2']: 
            mci(metadata_3D_img,title='metadata_3D_img',delay=_['cv2 delay'],scale=_['metadata_3D_img scale'])
###
################################################################
################################################################
################################################################
###
