#!/usr/bin/env python

from kzpy3.utils3 import *

import kzpy3.scratch.Template.default_values as default_values

P = default_values.P
P['ABORT'] = False

def topic_warning(t):
    cr("Warning!!!!!!!\n","topic",t,"in both Topics['To Expose'][] and in Arguments")

try:
    param = Arguments['param']
except:
    param = 'default value'

for a in Arguments:
    if a in P['To Expose']['template']:
       topic_warning(t) 
    P[a] = Arguments[a]

duration_timer = Timer()
freq_timer = Timer(1)
waiting_timer = Timer(1)







if __name__ == '__main__':

    print 'main loop'
    
    import kzpy3.Menu_app.menu2 as menu2

    parameter_file_load_timer = Timer(0.5)

    while P['ABORT'] == False:

        try:
            time.sleep(1)

            if parameter_file_load_timer.check():
                Topics = menu2.load_Topics(opjk("scratch/Template/default_values.py"),first_load=False,customer='template')
            print Topics
            if type(Topics) == dict:
                for t in Topics['To Expose']['template']:
                    if t in Arguments:
                        topic_warning(t)
                    if '!' in t:
                        pass
                    else:
                        P[t] = Topics[t]
            parameter_file_load_timer.reset()

            #for t in P:
            #    print P[t]
            #except:
            #    pass





            #if 'SOUND' in P['Arduinos']:
            #    pass #P['Arduinos']['SOUND'].write("(22)")

            #Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)

        except Exception as e:
            CS_(d2s('Main loop exception',e))
            #Default_values.arduino.default_values.EXIT(restart=False,shutdown=False,kill_ros=True,_file_=__file__)


#EOF
