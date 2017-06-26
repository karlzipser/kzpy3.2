from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch1'])



def Rate_Counter():
    D = {}
    D['type'] = 'Rate_Counter'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Network rate object')
    D['rate_ctr'] = 0
    D['rate_timer_interval'] = 10.0
    D['rate_timer'] = Timer(D['rate_timer_interval'])
    def _step(d):
        batch_size = d['batch_size']

        D['rate_ctr'] += 1
        if D['rate_timer'].check():
            print(d2s('rate =',dp(batch_size*D['rate_ctr']/D['rate_timer_interval'],2),'Hz'))
            D['rate_timer'].reset()
            D['rate_ctr'] = 0
    D['step'] = _step
    return D   
