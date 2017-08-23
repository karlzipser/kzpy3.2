#!/usr/bin/env python 
from kzpy3.vis2 import *
import threading

Thread_dic = {}
Thread_dic[THREAD_COUNTER] = 0
def Continuing_State(name=None,interval=2):
	Thread_dic[THREAD_COUNTER] += 1
	thread_id = (name,Thread_dic[THREAD_COUNTER])
	Thread_dic[thread_id] = time.time()
	D = {}
	if name:
		D[NAME] = name
	timer = Timer(interval)
	D[STOP_NOW] = False
	def function_thread():
		while not D[STOP_NOW]:
			if timer.check():
				print timer.time()
				timer.reset()
				Thread_dic[thread_id] = time.time()
			time.sleep(0.1)

	threading.Thread(target=function_thread).start()
	def function_stop():
		D[STOP_NOW] = True
	D[STOP] = function_stop
	return D

