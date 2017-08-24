#!/usr/bin/env python 
from kzpy3.vis2 import *
import threading

# RECOVER OTHER VERSION
def Continuing_State(name='<no name>',ctr=1):
	D = {}
	D[NAME] = name
	timer = Timer(1)
	D[STOP_NOW] = False
	D[OUTPUT] = None
	D[COUNTER] = ctr
	def function_thread():
		while not D[STOP_NOW]:
				if timer.check():
					print timer.time()
					timer.reset()
				time.sleep(0.1)
	def function_start():
		D[STOP_NOW] = False
		spd2s('...starting thread #',D[COUNTER],D[NAME])
		threading.Thread(target=function_thread).start()
	def function_stop():
		D[STOP_NOW] = True
	def function_pause():
		D[PAUSE_NOW] = True
	def function_continue():
		D[PAUSE_NOW] = False
	D[START] = function_start
	D[STOP] = function_stop
	D[PAUSE] = function_pause
	D[CONTINUE] = function_continue
	return D

