from kzpy3.vis3 import *
import Menu.main
Q = Menu.main.start_Dic(
    dic_project_path=opjk('drafts'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)


width = 600
height = 200
width_small = 1

def shift(big,small):
    big[:,0:-width_small,:] = big[:,width_small:,:]
    big[:,-1:,:] = small

def value_to_y(value,scale,offset,height):
    y = value * scale + offset*height
    return intr(y)



mtime_prev = -1

def grapher(Q):

    big = np.zeros((height,width,3),np.uint8)
    small = np.zeros((height,width_small,3),np.uint8)
    show_timer = Timer(1/30.)
    shift_timer = Timer(1/180.)
    hz = Timer(1)
    change_timer = Timer(1)
    load_timer = Timer(0.5)
    while True:
        if load_timer.check():
            load_timer.reset()
            try:
                Q['load']()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
        if shift_timer.check():
            T = Q['Q']
            if shift_timer.time_s != T['timers']['shift']:
                shift_timer = Timer(T['timers']['shift'])
            if show_timer.time_s != T['timers']['show']:
                show_timer = Timer(T['timers']['show'])
            shift_timer.reset()
            if shape(big) != (T['window']['height'],T['window']['width'],3):
                #print 'need to reset',shape(big),(T['window']['height'],'to',T['window']['width'],3)
                big = np.zeros((T['window']['height'],T['window']['width'],3),np.uint8)
                small = np.zeros((T['window']['height'],1,3),np.uint8)
            small *= 0

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

threading.Thread(target=grapher,args=[Q]).start()

shift_timer2 = Timer(1/100.)
while True:
    if shift_timer2.check():
        shift_timer2.reset()
        T = Q['Q']
        T['data']['a']['value'] = np.sin(5*time.time())
        T['data']['b']['value'] = np.sin(2*time.time())
        T['data']['c']['value'] = np.sin(20*time.time())


#,b



#EOF