#!/usr/bin/env python
from kzpy3.utils3 import *
import default_values
exec(identify_file_str)
_ = default_values._
C = _['commands']


def show_menu(C):
    sorted_keys = sorted(C.keys())
    for i in rlen(sorted_keys):
        k = sorted_keys[i]
        cg(i,k)


if __name__ == '__main__':


    show_menu(C)

#EOF

    