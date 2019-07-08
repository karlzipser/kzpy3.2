#!/usr/bin/env python
from kzpy3.utils3 import *
from filelock import Timeout, FileLock

setup_Default_Arguments(
    {
        'txt': 'a',
        't': 10,
    }
)
try:
    from filelock import Timeout, FileLock
    def soL(arg1,arg2,noisy=True):
        try:
            if type(arg1) == str and type(arg2) != str:
                name = arg1
                obj = arg2
            elif type(arg2) == str and type(arg1) != str:
                name = arg2
                obj = arg1
            elif type(arg2) == str and type(arg1) == str:
                pd2s('def so(arg1,arg2): both args cannot be strings')
                assert(False)
            else:
                assert(False)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

        lock_path = name + '.lock'
        lock = FileLock(lock_path, timeout=1)

        while True:
            try:
                lock.acquire()
                save_obj(obj,name,noisy)
                lock.release()
                break
            except Timeout:
                print("Another instance of this application currently holds the lock.")


    def loL(name,noisy=True):
        lock_path = name + '.lock'
        lock = FileLock(lock_path, timeout=1)
        while True:
            try:
                lock.acquire()
                o = load_obj(name,noisy)
                lock.release()
                return o
            except Timeout:
                print("Another instance of this application currently holds the lock.")


    def loState():
        return loL(opjk('__local__/State'))

    def soState(State):
        try:
            Original_state = lo(opjk('__local__/State'))
        except:
            Original_state = {}
        for k in State:
            Original_state[k] = State[k]
        os.system(d2s('mkdir -p',opjk('__local__')))
        os.system(d2s('touch',opjk('__local__/__init__.py')))
        soL(Original_state,opjk('__local__/State'))
except:
    print("unable to import filelock")


State = {'a':112}
State = loState()
pprint(State)
soState(State)


#EOF