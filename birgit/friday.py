"""
The ides here is to paste the code in segments, not all at once.
Try to guess what the result is before evaluating it in the ipython interpreter.

"""

#######################

print '*** test1 ***'

#######################


a = 1
b = 2
D = {}
D['a'] = b
D['b'] = a
print(a,b,D['a'],D['b'])


#######################


print(D.keys())

#######################

print(a.keys) # will give an error


#######################


l = []
l.append(1)
l.append(2)
print(l)

#######################


print(l[0])
print(l[1])


#######################


D['l'] = l
print(D['l'][1])


#######################
