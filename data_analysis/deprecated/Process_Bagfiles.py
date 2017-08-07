'''
Created on May 5, 2017

@author: picard
'''

import sys
import os
from Angle_Dict_Creator import Angle_Dict_Creator

if __name__ == '__main__':
    
    bagfile_folder = sys.argv[1]
    show_video = sys.argv[2]

    for file in os.listdir(bagfile_folder):
        if file.endswith(".bag"):
            
            bagfile_name = os.path.join(bagfile_folder, file)
            
            angle_dict_creator = Angle_Dict_Creator((None,bagfile_name, show_video))
            
            dictionary = angle_dict_creator.get_dict()
            print(dictionary)
            
            