print("this is kzpy3")

from utils.times import *
from utils.files import *
from utils.strings import *
from utils.array_stuff import *
from utils.clipcode import *
from utils.connect import *

from utils.more import *

log_name = get_safe_name(sys.argv[0].replace(opjk(),'')+'.txt')
log_strs = []
log_strs.append(' '.join(sys.argv).replace(opjk(),'')+' # '+time_str('Pretty'))
os.system('mkdir -p '+opjk('__local__','logs'))
list_of_strings_to_txt_file(opjk('__local__','logs',log_name),log_strs,write_mode="a")

#EOF