
from kzpy3.utils3 import *


Driving_direction_model = markov.Net(Compact_notation,still)




if __name__ == '__main__':
    
    def environment():
        return {
            'encoder': max(0,0.1+0.1*rndn()),
            'motor': int(max(0,49+10*rndn())),
        }

    while True:
        Driving_direction_model['step'](environment())
        raw_enter()




#EOF
