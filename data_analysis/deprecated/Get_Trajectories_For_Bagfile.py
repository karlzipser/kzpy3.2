'''
Created on May 10, 2017

@author: picard
'''
import sys
from data_parsing.Bagfile_Handler import Bagfile_Handler

if __name__ == '__main__':
    # Load bagfile
    bagfile_path = sys.argv[1]
    
    # Load Bagfile Parser
    bagfile_handler = Bagfile_Handler(bagfile_path)
    
    