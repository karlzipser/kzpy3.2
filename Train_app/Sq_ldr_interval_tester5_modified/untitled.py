
from kzpy3.vis3 import *
from kzpy3.Train_app.Sq_ldr_interval_tester5_modified.Main import get_similarity

c = z55(rnd((23,41,3))) 
d = z55(rnd((23,41,3)))
v = get_similarity(c,d)

cg('v =',v,ra=1)