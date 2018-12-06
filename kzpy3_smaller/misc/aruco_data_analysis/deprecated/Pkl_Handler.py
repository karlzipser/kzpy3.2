'''
Created on May 18, 2017

@author: Sascha Hornauer
'''
import os 
import cPickle as pickle
import random
from timeit import default_timer as timer
import sys

class Pkl_Handler(object):
    '''
    classdocs
    '''

    home = os.path.expanduser("~")
    test_trajectory_path = home + '/2ndDisk/N.pkl'
    
    run_names = []
    trajectory_list = {}
    
    def __init__(self):
        '''
        Constructor
        '''
        
        start = timer()
        traj_pkl_file = pickle.load(open(self.test_trajectory_path, "rb"))
        end = timer()
        print end-start
        
#         print traj_pkl_file['Mr_Yellow'].keys()
        
        for car_name in traj_pkl_file:                
            for run_name in traj_pkl_file[car_name]:
                for own_trajectory in traj_pkl_file[car_name][run_name]['self_trajectory']:
                    print type(own_trajectory)
                                                             
                sys.exit(0)
                    
            #    traj_lst.append( traj_pkl_file[car_name][run_name]['self_trajectory'] )
            #    print(car_name,run_name)
            
            
        
if __name__ == '__main__':    
    
    test_run = Pkl_Handler()