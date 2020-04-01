from kzpy3.vis3 import *

assert 'run_name' in Arguments
Defaults = {
    'show':False,
    'show2':False,
    'backward':50,
    'forward':250,
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

if os.path.exists(save_path):
    clp('!!!',save_path,'exists!!!','`wrb')
    exit()

Colors = {'direct':'b','left':'r','right':'g'}
P = {}
P['behavioral_mode_list'] = ['left','direct','right']
#lst=lo('/Users/karlzipser/Desktop/pts2D_multi_step.pkl')
lst = lo(opjD('Data','pts2D_multi_step','pkl',Arguments['run_name']))




make_path_and_touch_file(save_path)

Prediction2D_plot = CV2Plot(height_in_pixels=94,width_in_pixels=168,pixels_per_unit=7,y_origin_in_pixels=80)

Prediction2D_plot['verbose'] = False

indicies = []
images = []
freq = Timer(10)


for n in range(0,len(lst),1):
    indicies.append(lst[n]['index'])
    heading = -lst[n]['HEADING']
    Prediction2D_plot['clear']()
    a,b,c = max(0,n - Arguments['backward']), min(len(lst),n + Arguments['forward']), 1
    for i in range(a,b,c):
        if np.abs(lst[i]['steer'] - 49) < 100:
            for b in ['left','right','direct']:
                pts = rotatePolygon(
                    lst[i][b]-na([[lst[n]['x'],lst[n]['y']]]),
                    heading
                )
                if i == n:
                    sym = '.'
                else:
                    sym = ','
                if False:
                    pts_plot(pts,color=Colors[b],sym=sym) ###
                Prediction2D_plot['pts_plot'](pts,Colors[b],add_mode=True)

    
    img = Prediction2D_plot['show'](autocontrast2=True,scale=3.0,threshold=10,return_img=True)

    if Arguments['show']:
        mci(img,scale=3.0)

    images.append(img)
    freq.freq(d2n(int(100 * n/len(lst)),'% '))
    #raw_enter()

F = h5w(save_path)
F.create_dataset('index',data=na(indicies))
F.create_dataset('images',data=na(images),dtype='uint8')          
F.close()




#EOF
