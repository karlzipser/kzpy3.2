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


#,
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




#,a
CA()

"""
time_width

y = mx + b

scale

offset
"""

def value_to_y(value,scale,offset):
    y = value * scale + offset
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



T = {
    'a':{
        'scale': 80.,
        'offset': height/2.,
        'color': [255,255,255],
        'value': 0,
    },
    'b':{
        'scale': 20.,
        'offset': height/4.,
        'color': [0,255,0],
        'value': 0,
    },
    'c':{
        'scale': 75.,
        'offset': 3.*height/4.,
        'color': [255,0,255],
        'value': 0,
    },    
}

while True:

    if shift_timer.check():

        shift_timer.reset()
        hz.freq()

        small *= 0

        T['a']['value'] = np.sin(5*time.time())
        T['b']['value'] = np.sin(2*time.time())
        T['c']['value'] = np.sin(20*time.time())

        for k in T.keys():
            y = value_to_y(
                T[k]['value'],
                T[k]['scale'],
                T[k]['offset']
            )
            if y >= 0 and y < height:
                small[y,0,:] = T[k]['color']

        shift(big,small)

        if False:
            small = 255*rnd((height,width_small,3))
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