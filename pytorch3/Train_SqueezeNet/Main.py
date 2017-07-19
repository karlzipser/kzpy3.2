import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/pytorch3/Train_SqueezeNet','kzpy3/teg9'])

from Parameters import *
exec(identify_file_str)
import Data
import Batch

for a in Args.keys():
    P[a] = Args[a]

_ = dictionary_access

Training_data = Data.Training_Data()
Data_moment = _(Training_data,get_data)(run_code,1, seg_num,2, offset,3)
zdprint(dic,Data_moment)




#EOF