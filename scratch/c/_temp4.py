from kzpy3.utils2 import *

"""
https://docs.python.org/3/howto/curses.html
https://github.com/pmbarrett314/curses-menu/tree/master/cursesmenu
"""

if True:
	import curses
	def pbar(window):
		for j in range(100):
		    for i in range(10):
		        window.addstr(i, 0, d2s('xyz:',dp(np.random.rand(1),2)))
		        window.refresh()
		    time.sleep(0.1)
	curses.wrapper(pbar)


if False:
	from curses import wrapper
	def main(stdscr):
	    # Clear screen
	    stdscr.clear()

	    # This raises ZeroDivisionError when i == 10.
	    for i in range(0, 11):
	        v = i-10
	        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10))

	    stdscr.refresh()
	    stdscr.getkey()

	wrapper(main)





if False:
	import sys,os
	import curses

	def draw_menu(stdscr):
	    k = 0
	    cursor_x = 0
	    cursor_y = 0

	    # Clear and refresh the screen for a blank canvas
	    stdscr.clear()
	    stdscr.refresh()

	    # Start colors in curses
	    curses.start_color()
	    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	    # Loop where k is the last character pressed
	    while (k != ord('q')):

	        # Initialization
	        stdscr.clear()
	        height, width = stdscr.getmaxyx()

	        if k == curses.KEY_DOWN:
	            cursor_y = cursor_y + 1
	        elif k == curses.KEY_UP:
	            cursor_y = cursor_y - 1
	        elif k == curses.KEY_RIGHT:
	            cursor_x = cursor_x + 1
	        elif k == curses.KEY_LEFT:
	            cursor_x = cursor_x - 1

	        cursor_x = max(0, cursor_x)
	        cursor_x = min(width-1, cursor_x)

	        cursor_y = max(0, cursor_y)
	        cursor_y = min(height-1, cursor_y)

	        # Declaration of strings
	        title = "Curses example"[:width-1]
	        subtitle = "Written by Clay McLeod"[:width-1]
	        keystr = "Last key pressed: {}".format(k)[:width-1]
	        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
	        if k == 0:
	            keystr = "No key press detected..."[:width-1]

	        # Centering calculations
	        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
	        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
	        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
	        start_y = int((height // 2) - 2)

	        # Rendering some text
	        whstr = "Width: {}, Height: {}".format(width, height)
	        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

	        # Render status bar
	        stdscr.attron(curses.color_pair(3))
	        stdscr.addstr(height-1, 0, statusbarstr)
	        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
	        stdscr.attroff(curses.color_pair(3))

	        # Turning on attributes for title
	        stdscr.attron(curses.color_pair(2))
	        stdscr.attron(curses.A_BOLD)

	        # Rendering title
	        stdscr.addstr(start_y, start_x_title, title)

	        # Turning off attributes for title
	        stdscr.attroff(curses.color_pair(2))
	        stdscr.attroff(curses.A_BOLD)

	        # Print rest of text
	        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
	        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
	        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
	        stdscr.move(cursor_y, cursor_x)

	        # Refresh the screen
	        stdscr.refresh()

	        # Wait for next input
	        k = stdscr.getch()

	def main():
	    curses.wrapper(draw_menu)

	if __name__ == "__main__":
	    main()


if False:
	import curses 

	screen = curses.initscr() 
	#curses.noecho() 
	curses.curs_set(0) 
	screen.keypad(1) 
	curses.mousemask(1)

	screen.addstr("This is a Sample Curses Script\n\n") 

	while True:
	    event = screen.getch() 
	    if event == ord("q"): break 
	    if event == curses.KEY_MOUSE:
	    	#print 'here'
	        _, mx, my, _, _ = curses.getmouse()
	        y, x = screen.getyx()
	        print x,y
	        screen.addstr(y, x, screen.instr(my, mx, 5))

	curses.endwin()

if False:
	#!/usr/bin/env python2                                                       

	import curses                                                                
	from curses import panel                                                     

	class Menu(object):                                                          

	    def __init__(self, items, stdscreen):                                    
	        self.window = stdscreen.subwin(0,0)                                  
	        self.window.keypad(1)                                                
	        self.panel = panel.new_panel(self.window)                            
	        self.panel.hide()                                                    
	        panel.update_panels()                                                

	        self.position = 0                                                    
	        self.items = items                                                   
	        self.items.append(('exit','exit'))                                   

	    def navigate(self, n):                                                   
	        self.position += n                                                   
	        if self.position < 0:                                                
	            self.position = 0                                                
	        elif self.position >= len(self.items):                               
	            self.position = len(self.items)-1                                

	    def display(self):                                                       
	        self.panel.top()                                                     
	        self.panel.show()                                                    
	        self.window.clear()                                                  

	        while True:                                                          
	            self.window.refresh()                                            
	            curses.doupdate()                                                
	            for index, item in enumerate(self.items):                        
	                if index == self.position:                                   
	                    mode = curses.A_REVERSE                                  
	                else:                                                        
	                    mode = curses.A_NORMAL                                   

	                msg = '%d. %s' % (index, item[0])                            
	                self.window.addstr(1+index, 1, msg, mode)                    

	            key = self.window.getch()                                        

	            if key in [curses.KEY_ENTER, ord('\n')]:                         
	                if self.position == len(self.items)-1:                       
	                    break                                                    
	                else:                                                        
	                    self.items[self.position][1]()                           

	            elif key == curses.KEY_UP:                                       
	                self.navigate(-1)                                            

	            elif key == curses.KEY_DOWN:                                     
	                self.navigate(1)                                             

	        self.window.clear()                                                  
	        self.panel.hide()                                                    
	        panel.update_panels()                                                
	        curses.doupdate()

	class MyApp(object):                                                         

	    def __init__(self, stdscreen):                                           
	        self.screen = stdscreen                                              
	        curses.curs_set(0)                                                   

	        submenu_items = [                                                    
	                ('beep', curses.beep),                                       
	                ('flash', curses.flash)                                      
	                ]                                                            
	        submenu = Menu(submenu_items, self.screen)                           

	        main_menu_items = [                                                  
	                ('beep', curses.beep),                                       
	                ('flash', curses.flash),                                     
	                ('submenu', submenu.display)                                 
	                ]                                                            
	        main_menu = Menu(main_menu_items, self.screen)                       
	        main_menu.display()                                                  

	if __name__ == '__main__':                                                       
	    curses.wrapper(MyApp)   
