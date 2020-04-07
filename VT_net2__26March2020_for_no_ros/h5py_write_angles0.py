from kzpy3.vis3 import *
#Arguments['run_name'] = 'tegra-ubuntu_31Oct18_16h06m32s'
assert 'run_name' in Arguments
Defaults = {
    'show':False,
    'show2':False,
    'backward':50,
    'forward':250,
    'save':False,
    'start':0,
    'halve':True,
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
save_path = opjD('Data','pts2D_multi_step','h5py_angles0',Arguments['run_name']+'.h5py')


if Arguments['show2']:
    F = h5r(save_path)
    a0,O,a1 = open_run2(Arguments['run_name'])
    indicies = F['index'][:]
    for i in rlen(indicies):
        mci(O['left_image']['vals'][indicies[i]],title='a',scale=3.)
        mci(F['images'][i],title='b',scale=3.,delay=1)
    raw_enter('Hit return to exit.')
    exit()

if Arguments['save']:
    if os.path.exists(save_path):
        clp('!!!',save_path,'exists!!!','`wrb')
        exit()

Colors = {'direct':'b','left':'r','right':'g'}
P = {}
P['behavioral_mode_list'] = ['left','direct','right']

Angles = lo(opjD('Data','pts2D_multi_step','pkl_angles0',Arguments['run_name']))
lst = lo(opjD('Data','pts2D_multi_step','pkl',Arguments['run_name']))


if Arguments['save']:
    make_path_and_touch_file(save_path)

Prediction2D_plot = CV2Plot(height_in_pixels=94,width_in_pixels=168,pixels_per_unit=7,y_origin_in_pixels=80)

Prediction2D_plot['verbose'] = False

indicies = []
images = []
freq = Timer(10)


def angle_color(a):
    if a < 0:
        r = -max(-90,a)
        g = 0
        b = 90 - r
    else:
        g = min(90,a)
        r = 0
        b = 90 - g
    return z55((r,g,b))


for n in range(Arguments['start'],len(lst)-1,1):
    try:
        indicies.append(lst[n]['index'])
        heading = -lst[n]['HEADING']
        Prediction2D_plot['clear']()
        a,b,c = max(0,n - Arguments['backward']), min(len(lst),n + Arguments['forward']), 1
        for i in range(a,b,c):
            if np.abs(lst[i]['steer'] - 49) < 100:
                for b in ['direct','left','right',]:
                    pts = rotatePolygon(
                        lst[i][b]-na([[lst[n]['x'],lst[n]['y']]]),
                        heading
                    )
                    if i == n:
                        sym = '.'
                    else:
                        sym = ','
                    if False:
                        figure(1);clf();plt_square()
                        pts_plot(pts,color=Colors[b],sym=sym) ###
                    #print pts
                    #print pts[-1]
                    if b == 'direct':
                        q = -1
                        c = Colors[b]
                        Prediction2D_plot['pts_plot'](na([pts[q]]),c,add_mode=False)
                    else:
                        q = -1
                        
                        if Angles[b][i] > 30:
                            c = Colors['right']
                        elif Angles[b][i] < -30:
                            c = Colors['left']
                        else:
                            c = Colors['direct']
                        
                        #c = angle_color(Angles[b][i])
                        #print len(pts)
                        Prediction2D_plot['pts_plot'](pts,c,add_mode=False)

        
        img = Prediction2D_plot['show'](autocontrast2=True,scale=3.0,threshold=10,return_img=True)

        if Arguments['halve']:
            img = img[47-18:94-18,42:42+168/2,:]
            assert shape(img) == (47, 84, 3)
            img = cv2.resize(img,(0,0),fx=2.0,fy=2.0)
            assert shape(img) == (94, 168, 3)

        if Arguments['show']:
            mci(img,scale=3.0)

        images.append(img)

        freq.freq(d2n(int(100 * n/len(lst)),'% '))
    
    except KeyboardInterrupt:
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        print n
        break
    
if Arguments['save']:
    F = h5w(save_path)
    F.create_dataset('index',data=na(indicies))
    F.create_dataset('images',data=na(images),dtype='uint8')          
    F.close()




#EOF
