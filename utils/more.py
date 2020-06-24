from kzpy3.utils.common import *
from utils.times import *
from utils.files import *
from utils.strings import *
from utils.array_stuff import *
from utils.clipcode import *
from utils.connect import *



def gpu_stats(num=500):
    clp('Getting GPU stats...','`rwb')
    Pa = Progress_animator(num,update_Hz=10,message='')
    GPUs_avg = {}
    for i in range(num):
        GPUs_avg[i] = {}

    nvidia_smi_str_lst = unix('nvidia-smi')
    GPUs = {}

    for i in range(num):
        ctr = 0
        
        for n in nvidia_smi_str_lst:
            if 'C' in n and 'W' in n and '%' in n:
                if ctr not in GPUs.keys():
                            GPUs[ctr] = {}
                GPUs[ctr]['line'] = n
                a = n.split('%')
                if 'fan' not in GPUs[ctr]:
                    #cm(0)
                    GPUs[ctr]['fan'] = 0
                if 'util' not in GPUs[ctr]:
                    GPUs[ctr]['util'] = 0
                    #cm(0)
                GPUs[ctr]['fan'] += int(a[0].split(' ')[-1])
                GPUs[ctr]['util'] += int(a[1].split(' ')[-1])
                ctr += 1
                #print i,ctr
        Pa['update'](i)
        time.sleep(0.01)
    Pa['update'](num)

    GPUs['most_free'] = 0
    GPUs['most_free_util'] = 100
    for i in range(ctr):
        GPUs[i]['fan'] /= 1.0*num
        GPUs[i]['util'] /= 1.0*num
        if GPUs[i]['util'] < GPUs['most_free_util']:
            GPUs['most_free_util'] = GPUs[i]['util']
            GPUs['most_free'] = i
    kprint(GPUs)
    return GPUs






def Toggler(t=5):
    D = {}
    D['timer'] = Timer()
    def function_test(s):
        if 'toggle_value' not in D:
            D['toggle_value'] = s            
        if D['timer'].time() < t:
            #print 'no toggle'
            return False
        D['toggle_value_prev'] = D['toggle_value']
        D['toggle_value'] = s
        #kprint(s,'s')
        #print D['toggle_value'],D['toggle_value_prev']
        if D['toggle_value'] != D['toggle_value_prev']:
            return True
        return False
    D['test'] = function_test
    return D








#exec(identify_file_str)

#EOF