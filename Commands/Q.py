Q = {'a':1,'b':2,'c':3,'d':{'e':4,'f':5,'d':{'e':4,'f':5}}}

#EOF
def myprint(d):
  for k, v in d.iteritems():
    if isinstance(v, dict):
      myprint(v)
    else:
      print "{0} : {1}".format(k, v)