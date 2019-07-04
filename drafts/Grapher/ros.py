from kzpy3.vis3 import *
import Menu.main
import kzpy3.drafts.Grapher.main as main

Q = Menu.main.start_Dic(
    dic_project_path=opjk('drafts/Grapher'),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
T = Q['Q']

import kzpy3.drafts.Grapher.defaults as defaults
P = defaults.P

if __name__ == '__main__':
    
    threading.Thread(target=main.grapher,args=[]).start()
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