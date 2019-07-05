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

def shift(big,small,top,bottom):
    big[top:bottom,0:-1,:] = big[top:bottom,1:,:]
    big[top:bottom,-1:,:] = small[top:bottom,:,:]

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

    show_timer = Timer(T['times']['show'])
    shift_timer = Timer(T['times']['shift'])
    baseline_timer = Timer(T['times']['baseline_ticks'])
    #second_timer = Timer(1)

    new_images(T)

    while True:

        time.sleep(T['times']['thread_delay'])

        if T['ABORT']:
            break

        Q['load']()

        if shift_timer.check():
            if shift_timer.time_s != T['times']['shift']:
                shift_timer = Timer(T['times']['shift'])
            if show_timer.time_s != T['times']['show']:
                show_timer = Timer(T['times']['show'])
            if baseline_timer.time_s != T['times']['baseline_ticks']:
                baseline_timer = Timer(T['times']['baseline_ticks'])
            shift_timer.reset()

            if shape(P['images']['big']) != (T['window']['height'],T['window']['width'],3):
                print 'need to reset window'
                new_images(T)

            P['images']['small'] *= 0

            for k in T['data'].keys():

                if k[:2] == '--':
                    continue

                if T['data'][k]['value'] == None:
                    continue

                y = value_to_y(
                    T['data'][k]['value'],
                    -T['data'][k]['scale'],
                    T['data'][k]['offset'],
                    T['window']['height'],
                )

                if y >= 0 and y < T['window']['height']:
                    try:
                        P['images']['small'][y,0,:] = T['data'][k]['color']

                        if baseline_timer.check():
                            y = value_to_y(
                                T['data'][k]['baseline'],
                                -T['data'][k]['scale'],
                                T['data'][k]['offset'],
                                T['window']['height'],
                            )

                            if False:#second_timer.check():
                                d = 1
                            else:
                                d = 0
                            P['images']['small'][y-d:y+d+1,0,:] = T['data'][k]['color']

                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        CS_('Exception!',emphasis=True)
                        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
                        cr(0)

            if baseline_timer.check():
                baseline_timer.reset()

            shift(
                P['images']['big'],
                P['images']['small'],
                T['window']['shift_top'],
                T['window']['shift_bottom'],
            )

        for img in T['image_topics']:
            shp = shape(T['images'][img]['value'])

            if len(shp) == 3:
                a = 0
                b = shp[0]
                c = 0
                d = shp[1]
                if T['images'][img]['x_align'] == 'right':
                    c = T['window']['width'] - shp[1]
                    d = T['window']['width']
                if T['images'][img]['y_align'] == 'bottom':
                    a = T['window']['height'] - shp[0]
                    b = T['window']['height']
                
                a += T['images'][img]['y_offset']
                b += T['images'][img]['y_offset']
                c += T['images'][img]['x_offset']
                d += T['images'][img]['x_offset']

                P['images']['big'][a:b,c:d,:] = T['images'][img]['value']


    cg('grapher() thread done.')
###
###########################################################################




if __name__ == '__main__':
    
    threading.Thread(target=grapher,args=[]).start()
    prnt = Timer(1)
    show_timer = Timer(T['times']['show'])
    while True:
        time.sleep(T['times']['thread_delay'])
        T['data']['a']['value'] = np.sin(5*time.time())
        T['data']['b']['value'] = np.sin(2*time.time())
        T['data']['c']['value'] = np.sin(10*time.time())

        if show_timer.check():
            if T['CLEAR']:
                T['CLEAR'] = False
                P['images']['big'] *= 0
            show_timer.reset()
            k = mci(P['images']['big'],delay=1,scale=1)
            if k == ord('q'):
                CA()
                T['ABORT'] = True
                break
        if T['ABORT']:
            break

    cb('main() done.')


#EOF