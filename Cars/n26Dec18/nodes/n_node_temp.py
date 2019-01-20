#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import camera
exec(identify_file_str)

if __name__ == '__main__':

    rospy.init_node('network_node',anonymous=True,disable_signals=True)
    
    Q_list = camera.Q_list
    
    
    hz = Timer(30)
    wait = Timer()
    wait2 = Timer(30)
    while not rospy.is_shutdown():
        if wait.time() > 10:
            if wait2.check():
                cr('wait.time() =',int(wait.time()))
                wait2.reset()
        try:
            if len(Q_list) > 0:
                if Q_list[-1].ready:
                    Q_list[-1].ready = False
                    Q_list[-1].display(1,1,4)
                    hz.freq(' (main) ')
                    wait.reset()
                    continue
            time.sleep(1./10000.)
    
        except KeyboardInterrupt:
            QUIT = True
            cr('\n\n*** KeyboardInterrupt ***\n')
            time.sleep(1)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            #QUIT = True
            #cr('\n\n*** Exception ***\n')
            #time.sleep(1)

#EOF

    