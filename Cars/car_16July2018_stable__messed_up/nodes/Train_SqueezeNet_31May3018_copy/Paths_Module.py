from kzpy3.utils2 import *

CODE_PATH__ = opjh('kzpy3/Train_app')
VERSION_PATH = 'Train_SqueezeNet_31May2018'

spd2s('Using',VERSION_PATH,'(make sure this is correct)')
time.sleep(3)

pythonpaths([opjh('kzpy3'),opj(CODE_PATH__,VERSION_PATH),opj(CODE_PATH__,'nets')])

exec(identify_file_str)

#EOF
