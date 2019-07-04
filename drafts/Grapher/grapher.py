from kzpy3.vis3 import *
import Menu.main

Q = Menu.main.start_Dic(
    dic_project_path=opjk('drafts/Grapher'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
Q['load']()
T = Q['Q']

import kzpy3.drafts.Grapher.defaults as defaults
P = defaults.P

def shift(big,small):
    big[:,0:-1,:] = big[:,1:,:]
    big[:,-1:,:] = small

def value_to_y(value,scale,offset,height):
    y = value * scale + offset*height
    return intr(y)

def new_images(T):
    P['images']['big'] = 255*rnd((T['window']['height'],T['window']['width'],3))
    P['images']['big'] = P['images']['big'].astype(np.uint8)
    P['images']['small'] = np.zeros((T['window']['height'],1,3),np.uint8) 
###########################################################################
###
def grapher():

    T = Q['Q']
    show_timer = Timer(T['times']['show'])
    shift_timer = Timer(T['times']['shift'])

    new_images(T)

    while True:

        time.sleep(T['params']['thread_delay'])

        #if T['read_only']['ABORT']:
        #    break

        if T['params']['ABORT']:
            break

        Q['load']()

        if shift_timer.check():
            T = Q['Q']
            if shift_timer.time_s != T['times']['shift']:
                shift_timer = Timer(T['times']['shift'])
            if show_timer.time_s != T['times']['show']:
                show_timer = Timer(T['times']['show'])
            shift_timer.reset()

            if shape(P['images']['big']) != (T['window']['height'],T['window']['width'],3):
                #print 'need to reset',shape(big),(T['window']['height'],'to',T['window']['width'],3)
                #P['images']['big'] = np.zeros((T['window']['height'],T['window']['width'],3),np.uint8)
                #P['images']['small'] = np.zeros((T['window']['height'],1,3),np.uint8)
                new_images(T)

            P['images']['small'] *= 0

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
                        P['images']['small'][y,0,:] = T['data'][k]['color']
                    except:
                        cr(0)

            shift(P['images']['big'],P['images']['small'])

    cg('grapher() thread done.')
###
###########################################################################




if __name__ == '__main__':
    
    threading.Thread(target=grapher,args=[]).start()
    prnt = Timer(1)
    show_timer = Timer(T['times']['show'])
    while True:
        T = Q['Q']
        time.sleep(T['params']['thread_delay'])
        T['data']['a']['value'] = np.sin(5*time.time())
        T['data']['b']['value'] = np.sin(2*time.time())
        T['data']['c']['value'] = np.sin(20*time.time())
        #prnt.message(d2s(T['read_only']['ABORT']))
        if show_timer.check():
            show_timer.reset()
            k = mci(P['images']['big'],delay=1,scale=1)
            if k == ord('q'):
                CA()
                #T['read_only']['ABORT'] = True
                T['params']['ABORT'] = True
                break
        if T['params']['ABORT']:
            break
    cb('main() done.')


#EOF