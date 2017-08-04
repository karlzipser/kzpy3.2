"""
The ides here is to paste the code in segments, not all at once.
Try to guess what the result is before evaluating it in the ipython interpreter.

"""

#######################

print '*** test1 ***'

#######################

# Variables
a = 1
b = 2
print(a,b)

##################

# dictionary
D = {}
D['a'] = b
D['b'] = a
print(a,b,D['a'],D['b'])



#######################
# list

l = []
l.append(1)
l.append(2)
print(l)

#######################


print(l[0])
print(l[1])



#######################


print(D.keys())
print(type(D.keys()))
print(D.keys()[1])


#######################

# dictionary holding a list

D['l'] = l
print(D['l'][1])


#######################
