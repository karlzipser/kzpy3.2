from kzpy3.utils3 import *

CODE_PATH__ = pname(file)
VERSION_PATH = fname(file)

spd2s('Using',VERSION_PATH,'(make sure this is correct)')
time.sleep(3)

pythonpaths([opjh('kzpy3'),opj(CODE_PATH__,VERSION_PATH),opj(CODE_PATH__,'nets')])

exec(identify_file_str)

#EOF
