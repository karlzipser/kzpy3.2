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
Syms = {'direct':'o','left':'.','right':'.'}
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

        # a,d,c = max(0,n - Arguments['backward']), min(len(lst),n + Arguments['forward']), 1


        for b in ['left','right','direct']:
            Pts[b] = []

        # for i in range(a,d,c):
        for j in range(-60,30):#(-Arguments['backward'],Arguments['forward']):
            i = j + n
            if i < 0:
                continue
            if i >= len(lst)-1:
                continue

            if np.abs(lst[i]['steer'] - 49) < 100:
                for b in ['left','right','direct']:
                    
                    if b != 'direct':
                        if j > -30:
                            continue
                    else:
                        if j != 0:
                            continue
                    v = lst[i][b]-na([[lst[n]['x'],lst[n]['y']]])
                    #v = lst[n][b]-na([[lst[n]['x'],lst[n]['y']]])
                    if b in ['left','right']:
                        #print len(v)
                        v = v[-3:]
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

                    
                    Pts[b].append(pts[0])

                    #if True:
                    #    pts_plot(pts,color=Colors[b],sym=sym) ###
                    #Prediction2D_plot['pts_plot'](pts,Colors[b],add_mode=False)

        for b in ['left','right','direct']:
            print shape(Pts[b]),b
            pts_plot(Pts[b],Colors[b],sym=',')
            plot(na(Pts[b])[:,0].mean(),na(Pts[b])[:,1].mean(),Colors[b]+'o')
            #Prediction2D_plot['pts_plot'](na(Pts[b]),Colors[b],add_mode=False)
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

#,a
Colors = {'direct':'b','left':'r','right':'g'}

Pts = {
    'left':{},
    'right':{},
    'direct':{},
}
for k in Pts:
    for i in range(10):
        Pts[k][i] = []
Pts['xy'] = []
if 'lst' not in locals():
    lst = lo('/Users/karlzipser/Desktop/Data/pts2D_multi_step/pkl/tegra-ubuntu_31Oct18_16h06m32s.pkl')
#figure(1);clf();plt_square()
for i in range(len(lst)-10):
    N = lst[i]
    Pts['xy'].append(na([N['x'],N['y']]))
    for b in ['left','right','direct']:
        for j in rlen(N[b]):
            Pts[b][j].append(N[b][j])

ll = []
rl = []
l = Pts['left']
r = Pts['right']

p = Pts['xy'][8000]

def pts_dist(a,b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

for i in rlen(Pts['left'][9]):
    if pts_dist(p,l[9][i]) < 4:
        ll.append(l[9][i])
    if pts_dist(p,r[9][i]) < 4:
        rl.append(r[9][i])

figure(1);clf();plt_square()
pts_plot(ll,'r')
pts_plot(rl,'g')
pts_plot([p],'b',sym='o')
spause()

        #p = N[b][-1]
        #plot(p[0],p[1],Colors[b]+'.')
#spause()
#,b


o = lo('/Users/karlzipser/Desktop/Data/pts2D_multi_step/pkl_angles0/tegra-ubuntu_31Oct18_16h06m32s.pkl')
c = o['left']
d = o['right']

n = 5
a = Pts['left'][9]
b = Pts['right'][9]
ax = meo(na(a)[:,0],n)
ay = meo(na(a)[:,1],n)
bx = meo(na(b)[:,0],n)
by = meo(na(b)[:,1],n)
figure(1);clf();plt_square()
plot(ax,ay,'r')
plot(bx,by,'g')
for i in rlen(ax):
    #if c[i] < -30:
    #    plot(ax[i],ay[i],'r.')
    if d[i] > 30:
        plot(bx[i],by[i],'g.')



s = 0.75
sn = np.sin(arange(0,30,0.1))
sn += 0.2*rndn(len(sn))
tn = [0]
for i in range(1,len(sn)):
    b = s * tn[i-1] + (1-s) * sn[i]
    tn.append( b )
tn = na(tn)
clf()
plot(sn)
plot(tn[:-2])
plot(meo(sn,5))

#EOF
