from kzpy3.vis3 import *

assert 'run_name' in Arguments
Defaults = {
    'show':False,
    'start':9000,
    'show2':False,
    'backward':15, # positive number
    'forward':15,
    'save':False,
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
save_path = opjD('Data','pts2D_multi_step','h5py',Arguments['run_name']+'.h5py')


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
    make_path_and_touch_file(save_path)

Colors = {'direct':'b','left':'r','right':'g'}
P = {}
P['behavioral_mode_list'] = ['left','direct','right']
#lst=lo('/Users/karlzipser/Desktop/pts2D_multi_step.pkl')
lst = lo(opjD('Data','pts2D_multi_step','pkl',Arguments['run_name']))






Prediction2D_plot = CV2Plot(height_in_pixels=94,width_in_pixels=168,pixels_per_unit=7,y_origin_in_pixels=80)

Prediction2D_plot['verbose'] = False

indicies = []
images = []
freq = Timer(10)

Pts = {}

for n in range(Arguments['start'],len(lst),1):
    figure(1);clf();plt_square(5)
    if True:#try:
        indicies.append(lst[n]['index'])
        heading = -lst[n]['HEADING']
        Prediction2D_plot['clear']()
        a,d,c = max(0,n - Arguments['backward']), min(len(lst),n + Arguments['forward']), 1


        for b in ['left','right','direct']:
            Pts[b] = []

        for i in range(a,d,c):

            if np.abs(lst[i]['steer'] - 49) < 100:
                for b in ['left','right','direct']:
                    j = i
                    #if b != 'direct':
                    #    j = i - 90
                    v = lst[i][b]-na([[lst[n]['x'],lst[n]['y']]])
                    #v = lst[n][b]-na([[lst[n]['x'],lst[n]['y']]])
                    if b in ['left','right']:
                        #print len(v)
                        v = v[-2:]
                    else:
                        v = [[lst[i]['x'],lst[i]['y']]]-na([[lst[n]['x'],lst[n]['y']]])
                        #v = [v[0]]
                    pts = rotatePolygon(
                        v,
                        heading
                    )
                    if False: #i == n:
                        sym = 'o'
                    else:
                        sym = '.'

                    #print shape(pts)
                    Pts[b].append(pts[0])

                    #if True:
                    #    pts_plot(pts,color=Colors[b],sym=sym) ###
                    #Prediction2D_plot['pts_plot'](pts,Colors[b],add_mode=False)

        for b in ['left','right','direct']:
            pts_plot(Pts[b],Colors[b])
            Prediction2D_plot['pts_plot'](na(Pts[b]),Colors[b],add_mode=False)
        #raw_enter()


        
        img = Prediction2D_plot['show'](autocontrast2=True,scale=3.0,threshold=10,return_img=True)

        if Arguments['show']:
            mci(img,scale=3.0)

        images.append(img)
        freq.freq(d2n(int(100 * n/len(lst)),'% '))
    """
    except KeyboardInterrupt:
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        break
    """

"""
F = h5w(save_path)
F.create_dataset('index',data=na(indicies))
F.create_dataset('images',data=na(images),dtype='uint8')          
F.close()
"""



#EOF
