#!/usr/bin/env python
from kzpy3.utils3 import *

t = 1.

if 't' in Arguments:
    t = float(Arguments['t'])
print_Arguments()

nvidia_smi_continuous(t)

#EOF

    