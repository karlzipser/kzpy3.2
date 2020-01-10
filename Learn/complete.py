
from kzpy3.utils3 import *

from default_args import Default_Arguments as D

w = ['--NET_TYPE','--HELP']

for a in D.keys():
	w.append(''+a)
	for d in D[a].keys():
		w.append('--'+d)
w = list(set(w))
b = " ".join(w)
c = "complete -W \""+b+"\" Learn"

clp(c)
list_of_strings_to_txt_file(
	opjk('Learn','complete.sh'),
	['#!/usr/bin/env bash',c]
)
#os.system(c)