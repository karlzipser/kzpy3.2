#!/usr/bin/python
ctr = 0
import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5000:
      time.sleep(delay)
      count += 1
      print str(count) + " " + threadName

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 0.3, ) )
except:
   print "Error: unable to start thread"

print 'main loop'
while 1:
   #print ctr
   ctr += 1
   time.sleep(0.1)

# see: http://effbot.org/zone/thread-synchronization.htm

