#!/usr/bin/env python 
from kzpy3.vis2 import *
import threading

def Continuing_State(name='<no name>',ctr=1):
	D = {}
	D[NAME] = name
	timer = Timer(1)
	D[STOP_NOW] = False
	D[PAUSE_NOW] = False
	D[OUTPUT] = None
	D[COUNTER] = ctr
	def function_enter():
		print('Entering thread...')
	def function_exit():
		print('...leaving thread.')
	def function_thread():

		function_enter()
		work_timer = Timer(0)
		work_message_timer = Timer(3)
		pause_timer = Timer(2)
		wait_timer = Timer(0.1)
		while not D[STOP_NOW]:
			if not D[PAUSE_NOW]:
				D[OUTPUT] = d2s(D[NAME],'working for',work_timer.time(),'seconds')
				work_message_timer.message(D[OUTPUT])
				wait_timer.wait()
				print('w')
			else:
				pause_timer.message('<paused>')
		function_exit()
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

