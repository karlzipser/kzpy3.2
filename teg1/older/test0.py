from kzpy3.utils import *

p = subprocess.Popen(["python","test2.py"])

time.sleep(10)

p.terminate()
