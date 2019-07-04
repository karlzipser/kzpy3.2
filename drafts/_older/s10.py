if False:
    M = {
        'text':'Warning, meltdown in progress!',
        'period': 5,
        'till': 151239,
        'filename':'m293.py'
    }
    say(M['text'])

    Ms = {
        M['text']:M
    }


    def key_access(Dic,keys,start=True):
        if start:
            keys_copy = []
            for k in Dic['current_keys']:
                keys_copy.append(k)
            keys = keys_copy
        key = keys.pop(0)
        assert key in Dic.keys()
        if type(Dic[key]) == dict and len(keys) > 0:
            return key_access(Dic[key],keys,start=False)
        else:
            return Dic[key]



def key_get_set(D,key_list,value=None):
    key = key_list.pop(0)
    assert key in D.keys()
    if len(key_list) == 0:
        if value != None:
            D[key] = value
            return value
        else:
            return D[key]
    else:
        return key_get_set(D[key],key_list,value)
kg = key_get_set
if False:
    Q = {1:{2:{3:4}}}
    print Q
    print kg(Q,[1,2,3])
    print Q
    print kg(Q,[1,2,3],{5:6})
    print Q


#,
print 'hi there!'
#,


#,
from kzpy3.vis3 import *
import kzpy3.Array.Array
CA()
hz = Timer(1)
tt = Timer(1/30.)
U = kzpy3.Array.Array.Array(300,2)

U['setup_plot'](
    height_in_pixels=100,
    width_in_pixels=600,
    x_origin_in_pixels=300,
    pixels_per_unit=1,
)

for i in range(0,100000,5):
    while not tt.check():
        time.sleep(0.001)
    tt.reset()
    hz.freq()
    U['append'](
        na([i/5.,100/2.*np.sin(2*i/100.)]),
        None,
        {'time':time.time()},
    )

    #U['check_ts'](1)
    #print U['array'][U['ctr']-1,0]
    d = U['array'][U['ctr']-1,0]
    #print U['array'][U['ctr']-1,:]
    U['array'][:U['ctr'],0] -= d
    #if np.mod(i,15) == 0:
        
    k = U['show'](
        use_CV2_plot=True,
        use_maplotlib=False,
        do_print=False,
        clear=True,
        color=(255,255,0),
        code=None,
        show=True,
        grid=False,
        scale=1.0,
    )

    U['array'][:U['ctr'],0] += d
    #spause()
    #time.sleep(0.1)
    if k == ord('q'):
        CA()
        break
#,b



#,
from kzpy3.vis3 import *
import kzpy3.Array.Array
CA()
hz = Timer(5)
tt = Timer(1/30.)
U = kzpy3.Array.Array.Array(300,2)

U['setup_plot'](
    height_in_pixels=100,
    width_in_pixels=600,
    x_origin_in_pixels=600,
    pixels_per_unit=1,
)

ABORT = False
i = 0
while not ABORT:

    x = i
    y = 100/2.*np.sin(2*i/100.)

    U['append'](
        na([x,y]),
        None,
        {'time':time.time()},
    )

    if tt.check():
        tt.reset()
        hz.freq()
        #print time.time()
        d = U['array'][U['ctr']-1,0]

        U['array'][:U['ctr'],0] -= d
            
        k = U['show'](
            use_CV2_plot=True,
            use_maplotlib=False,
            do_print=False,
            clear=True,
            color=(255,255,0),
            code=None,
            show=True,
            grid=False,
            scale=1.0,
        )

        U['array'][:U['ctr'],0] += d


        if k == ord('q'):
            CA()
            ABORT = True
    i += 1
#,b


#,a
CA()
width = 600
height = 200
width_small = 1
big = np.zeros((height,width,3),np.uint8)
small = np.zeros((height,width_small,3),np.uint8)
show_timer = Timer(1/30.)
shift_timer = Timer(1/30.)
hz = Timer(1)

def shift(big,small):
    big[:,0:-width_small,:] = big[:,width_small:,:]
    big[:,-1:,:] = small

big = 255*rnd((height,width,3))
big = big.astype(np.uint8)

while True:
    if shift_timer.check():
        shift_timer.reset()
        hz.freq()
        small = 255*rnd((height,width_small,3))
        small = small.astype(np.uint8)
        shift(big,small)
        #mi(big);spause();
    if show_timer.check():
        show_timer.reset()
        k = mci(big,delay=1,scale=1)
        if k == ord('q'):
            CA()
            break
    #raw_enter()
#,b




#,




import Menu.main
CA()

def file_modified_test(path,mtime_prev):
    mtime = os.path.getmtime(path)
    if mtime > mtime_prev:
        return mtime
    else:
        return 0





def value_to_y(value,scale,offset,height):
    y = value * scale + offset*height
    return intr(y)



width = 600
height = 200
width_small = 1
big = np.zeros((height,width,3),np.uint8)
small = np.zeros((height,width_small,3),np.uint8)
show_timer = Timer(1/30.)
shift_timer = Timer(1/180.)
hz = Timer(1)


def shift(big,small):
    big[:,0:-width_small,:] = big[:,width_small:,:]
    big[:,-1:,:] = small

big = 255*rnd((height,width,3))
big = big.astype(np.uint8)

Q = Menu.main.start_Dic(
    dic_project_path=opjk('drafts'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)


T = Q['Q']

change_timer = Timer(1)
load_timer = Timer(0.5)

mtime_prev = -1

while True:
    if load_timer.check():
        load_timer.reset()
        try:
            t = file_modified_test(opjk('drafts/__local__/default_values.pkl'),mtime_prev)
            if t:
                mtime_prev = t
                Q['load']()
                T = Q['Q']
        except:
            cr(1)
    #print T
    if shift_timer.check():
        if shift_timer.time_s != T['timers']['shift']:
            shift_timer = Timer(T['timers']['shift'])
        if show_timer.time_s != T['timers']['show']:
            show_timer = Timer(T['timers']['show'])
        shift_timer.reset()
        hz.freq()
        if change_timer.check():
            change_timer.reset()
            #cg('T',T['window']['height'],T['window']['width'])
            """
            T['window']['height'] = rndint(100,300)
            T['window']['width'] = rndint(400,600)
            T['timers']['shift'] = 1/(1.0*rndint(60,300))
            T['timers']['show'] = 1/(1.0*rndint(10,60))
            """
        if shape(big) != (T['window']['height'],T['window']['width'],3):
            print 'need to reset',shape(big),(T['window']['height'],T['window']['width'],3)
            big = np.zeros((T['window']['height'],T['window']['width'],3),np.uint8)
            small = np.zeros((T['window']['height'],1,3),np.uint8)
        small *= 0

        T['data']['a']['value'] = np.sin(5*time.time())
        T['data']['b']['value'] = np.sin(2*time.time())
        T['data']['c']['value'] = np.sin(20*time.time())

        for k in T['data'].keys():
            if k[:2] == '--':
                continue
            y = value_to_y(
                T['data'][k]['value'],
                T['data'][k]['scale'],
                T['data'][k]['offset'],
                T['window']['height'],
            )
            if y >= 0 and y < T['window']['height']:
                try:
                    small[y,0,:] = T['data'][k]['color']
                except:
                    cr(0)

        shift(big,small)

        if False:
            small = 255*rnd((T['window']['height'],width_small,3))
            small = small.astype(np.uint8)
            shift(big,small)

    if show_timer.check():
        show_timer.reset()
        k = mci(big,delay=1,scale=1)
        if k == ord('q'):
            CA()
            break


#,b



#EOF