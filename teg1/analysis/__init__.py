############################
# - compatibility with Python 3. This stuff from M. Brett's notebooks
from __future__ import print_function  # print('me') instead of print 'me'
from __future__ import division  # 1/2 == 0.5, not 0

# - import common modules
import os
import os.path
import shutil
import scipy
import scipy.io
import numpy as np  # the Python array package
import string
import glob
import time
import sys
import datetime
import random
import pickle
import re
import subprocess
from pprint import pprint

# - some definitions
import socket
host_name = socket.gethostname()
home_path = os.path.expanduser("~")
imread = scipy.misc.imread
imsave = scipy.misc.imsave
#opj = os.path.join
gg = glob.glob
shape = np.shape
randint = np.random.randint
#random = np.random.random # - this makes a conflict, so don't use it.
randn = np.random.randn
zeros = np.zeros
ones = np.ones
imresize = scipy.misc.imresize
reshape = np.reshape
mod = np.mod


def opj(*args):
	if len(args) == 0:
		args = ['']
	str_args = []
	for a in args:
		str_args.append(str(a))
	return os.path.join(*str_args)

def opjh(*args):
	return opj(home_path,opj(*args))

def opjD(*args):
    return opjh('Desktop',opj(*args))

