#!/usr/bin/env python

############################################
"""
python kzpy3/Data_app/lidar/Offline_lidar_processing/Main.py autostart 1
"""
############################################



############################################
# setup and menu start
from kzpy3.vis3 import *
duration_timer = Timer()
import kzpy3.Data_app.lidar.Offline_lidar_processing.default_values as default_values
P = default_values.P
P['ABORT'] = False
try:
    if Arguments['autostart'] in [1,'y','Y','yes']:
        os.system(d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ","kzpy3/Data_app/lidar/Offline_lidar_processing"," dic P"))
        # Leading '/' in path messes up menu2.py; until fixed, using opjk() won't work.
except:
    pass
#
############################################


if __name__ == '__main__':
    """
    print 'main loop'
    import kzpy3.Menu_app.menu2 as menu2
    parameter_file_load_timer = Timer(0.5)
    while P['ABORT'] == False:
        try:
            time.sleep(1)

            if parameter_file_load_timer.check():
                Topics = menu2.load_Topics("kzpy3/Data_app/lidar/Offline_lidar_processing",first_load=False,customer='Main')
            if type(Topics) == dict:
                for t in Topics['To Expose']['Main']:
                    if t in Arguments:
                        topic_warning(t)
                    if '!' in t:
                        pass
                    else:
                        P[t] = Topics[t]
            parameter_file_load_timer.reset()

        except Exception as e:
            CS_(d2s('Main loop exception',e))
    """


    experiments = []
    locations = []
    behavioral_mode = []
    h5py = []
    runs = []

    experiments_ = sggo(P['experiments'],'*')
    for e in experiments_:
        if fname(e)[0] == '_' or '+' in e:
            cr('skipping',e)
        else:
            experiments.append(e)
            cb('using', e)

    for e in experiments:
        locations = sggo(e,'locations/*')
        for l in locations:
            behavioral_modes = sggo(l,'*')
            for b in behavioral_modes:
                runs_ = sggo(b,'h5py','*')
            for r in runs_:
                if 'Mr_Black' in r or fname(r)[0] == '_':
                    cr('skipping',fname(r))
                else:
                    runs.append(r)
                    cb('using', fname(r))
        


    os.system(d2s("mkdir -p",P['dst folder']))
    os.system(d2s("mkdir -p",P['dst folder working'))



#####################################
#
width = P['width']
Y = {}
mx = 2*np.pi*1000.0*10
extra = 10000
for d in range(0,int(mx+extra)):
    v = int( width*d / (1.0*mx) )
    if v > (width-1):
        v = (width-1)
    Y[d] = v

j = 0
for i in range(sorted(Y.keys())[-1]):
    if i in Y:
        j = Y[i]
    Y[i] = j

Y[np.nan] = 0
#
######################################



show_timer = Timer(P['show time 1'])
CA()
for i in [4000]:#range(4000,8000):#rlen(q):
    #i = 2000
    q = p[i,:,:]
    x = q[:,0]
    y = q[:,1]
    x = x.reshape(P['width'],P['height'])
    y = y.reshape(P['width'],P['height'])

    d = 0#P['height']/2

    angles = []
    for j in range(len(y[:,0])):
        a = x[j,d]
        b = y[j,d]
        n = angle_between((1,0), (a,b))

        if not n >= 0:
            if not n < 0:
            #    print (a,b),n
                n = 0
        if b > 0:
            n*=-1

        angles.append(np.pi+n)

    if show_timer.check():
        plot(angles,',')
        spause()
        show_timer = Timer(P['show time 1'])

    angles = na(angles)
    indicies = [Y[v] for v in (10000*na(angles)).astype(int)]

    angles2 = 0.0 * angles
    angles2[indicies] = angles



    img = np.sqrt(x**2+y**2)
    img2 = 0.0 * img
    img2[indicies,:] = img

    mi( (z2o(img2)*255).astype(np.uint8))
    spause()



















    cg("P['ABORT'] =",P['ABORT'],"\nRun duration =",dp(duration_timer.time()),"seconds.\nDone.\n")

#EOF
