from kzpy3.utils3 import *
project_path = pname(__file__)

Q = {
    'nothing':True,
}


def less_than(Arg_dic):
    if Arg_dic['left_hand_side'] < Arg_dic['right_hand_side']:
        return True
    else:
        return False

def greater_than(Arg_dic):
    return less_than({'left_hand_side':-Arg_dic['left_hand_side'],'right_hand_side':-Arg_dic['right_hand_side']})

def equals(Arg_dic):
    if Arg_dic['left_hand_side'] == Arg_dic['right_hand_side']:
        return True
    else:
        return False

def function_pass(Environment,D):
    pass

def function_true(Environment):
    print 'here'
    return True






#EOF
