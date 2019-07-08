



c=d2n('\x1b[31m','nice!','\x1b[32m','color','\x1b[40m',' \x1b[31m','blah','\x1b[104m','done','\x1b[32m')
print c

xsx='\x1b[0m'
xs0=xsx+'\x1b[31m'
xs1=xsx+'\x1b[32m'
xs3=xsx+'\x1b[40m\x1b[32m'

print(d2n('\x1b[31m','nice!','\x1b[32m','color','\x1b[40m',' \x1b[31m','blah','\x1b[104m','done','\x1b[32m'))



def p2s(*args,**kwargs):
    #print type(args)
    args = list(args)
    ##print(d2s(*list(args)))
    print(d2n(*([xsx]+args+[xsx])))
p2s(0,xsx+xs0,1,xs1,2,xs3,3,4)
p2s('hi',1,a=3)
p2s(0,xsx+xs0,1,xs1,2,xs3,3,4,a=32)
p2s(0,xsx+xs0,1,xs1,2,xs3,3,4,a=32)
p2s(0,xs0,1,xs1,2,xs3,3,4,xs1,'adfasdfa')
p2s(0,xs0,1,xs1,2,xs3,3,4,xsx,xs1,'adfasdfa')

for i in range(108):
    x = d2n('\x1b[',i,'m')
    p2s(x,i)

def n(*args,**kwargs):

    print(args,type(args))
    print(kwargs,type(kwargs))
n(1,2,3,level=0,test=9,a='aa')







"""http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html"""
import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print u"\u001b[0m"

import sys
for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
        print u"{001b[48;5;" + code + "m " + code.ljust(4) + "}"
    print u"\u001b[0m"

print u"\u001b[48;5;27mKarl\u001b[0m"
"""
Bold: \u001b[1m
Underline: \u001b[4m
Reversed: \u001b[7m

Up: \u001b[{n}A
Down: \u001b[{n}B
Right: \u001b[{n}C
Left: \u001b[{n}D


Up: \u001b[{n}A moves cursor up by n
Down: \u001b[{n}B moves cursor down by n
Right: \u001b[{n}C moves cursor right by n
Left: \u001b[{n}D moves cursor left by n
Next Line: \u001b[{n}E moves cursor to beginning of line n lines down
Prev Line: \u001b[{n}F moves cursor to beginning of line n lines down
Set Column: \u001b[{n}G moves cursor to column n
Set Position: \u001b[{n};{m}H moves cursor to row n column m
Clear Screen: \u001b[{n}J clears the screen
n=0 clears from cursor until end of screen,
n=1 clears from cursor to beginning of screen
n=2 clears entire screen
Clear Line: \u001b[{n}K clears the current line
n=0 clears from cursor to end of line
n=1 clears from cursor to start of line
n=2 clears entire line
Save Position: \u001b[{s} saves the current cursor position
Save Position: \u001b[{u} restores the cursor to the last saved position

"""
print u"\u001b[1m BOLD \u001b[0m\u001b[4m Underline \u001b[0m\u001b[7m Reversed \u001b[0m"

import time, sys
def loading():
    print "Loading..."
    for i in range(0, 100):
        time.sleep(0.1)
        sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
        sys.stdout.flush()
    print
    
loading()





import time, sys, random
def loading(count=5):
    all_progress = [0] * count
    sys.stdout.write("\n" * count) # Make sure we have space to draw the bars
    while any(x < 100 for x in all_progress):
        time.sleep(0.01)
        # Randomly increment one of our progress values
        unfinished = [(i, v) for (i, v) in enumerate(all_progress) if v < 100]
        index, _ = random.choice(unfinished)
        all_progress[index] += 1
        
        # Draw the progress bars
        sys.stdout.write(u"\u001b[1000D") # Move left
        sys.stdout.write(u"\u001b[" + str(count) + "A") # Move up
        for progress in all_progress: 
            width = progress / 4
            print "[" + "#" * width + " " * (25 - width) + "]"
        
loading()










import sys, tty
def command_line():
    tty.setraw(sys.stdin)
    while True:
        char = sys.stdin.read(1)
        if ord(char) == 3: # CTRL-C
            break;
        print ord(char)
        sys.stdout.write(u"\u001b[1000D") # Move all the way left







import sys, tty
 
def command_line():
    tty.setraw(sys.stdin)
    while True: # loop for each line
    # Define data-model for an input-string with a cursor
        input = ""
        while True: # loop for each character
            char = ord(sys.stdin.read(1)) # read one char and get char code
            
            # Manage internal data-model
            if char == 3: # CTRL-C
                return
            elif 32 <= char <= 126:
                input = input + chr(char)
            elif char in {10, 13}:
                sys.stdout.write(u"\u001b[1000D")
                print "\nechoing... ", input
                input = ""

            # Print current input-string
            sys.stdout.write(u"\u001b[1000D")  # Move all the way left
            sys.stdout.write(input)
            sys.stdout.flush()




import sys, tty
 
def command_line():
    tty.setraw(sys.stdin)
    while True: # loop for each line
    # Define data-model for an input-string with a cursor
        input = ""
        index = 0
        while True: # loop for each character
            char = ord(sys.stdin.read(1)) # read one char and get char code
            
            # Manage internal data-model
            if char == 3: # CTRL-C
                return
            elif 32 <= char <= 126:
                input = input[:index] + chr(char) + input[index:]
                index += 1
            elif char in {10, 13}:
                sys.stdout.write(u"\u001b[1000D")
                print "\nechoing... ", input
                input = ""
                index = 0
            elif char == 27:
                next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                if next1 == 91:
                    if next2 == 68: # Left
                        index = max(0, index - 1)
                    elif next2 == 67: # Right
                        index = min(len(input), index + 1)
            elif char == 127:
                input = input[:index-1] + input[index:]
                index -= 1
            # Print current input-string
            sys.stdout.write(u"\u001b[1000D") # Move all the way left
            sys.stdout.write(u"\u001b[0K")    # Clear the line
            sys.stdout.write(input)
            sys.stdout.write(u"\u001b[1000D") # Move all the way left again
            if index > 0:
                sys.stdout.write(u"\u001b[" + str(index) + "C") # Move cursor too index
            sys.stdout.flush()


import sys, tty
def syntax_highlight(input):
    stripped = input.rstrip()
    return stripped + u"\u001b[41m" + " " *  (len(input) - len(stripped)) + u"\u001b[0m"

def command_line():
    tty.setraw(sys.stdin)
    while True: # loop for each line
        # Define data-model for an input-string with a cursor
        input = ""
        index = 0
        while True: # loop for each character
            char = ord(sys.stdin.read(1)) # read one char and get char code
            
            # Manage internal data-model
            if char == 3: # CTRL-C
                return
            elif 32 <= char <= 126:
                input = input[:index] + chr(char) + input[index:]
                index += 1
            elif char in {10, 13}:
                sys.stdout.write(u"\u001b[1000D")
                print "\nechoing... ", input
                input = ""
                index = 0
            elif char == 27:
                next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                if next1 == 91:
                    if next2 == 68: # Left
                        index = max(0, index - 1)
                    elif next2 == 67: # Right
                        index = min(len(input), index + 1)
            elif char == 127:
                input = input[:index-1] + input[index:]
                index -= 1
            # Print current input-string
            sys.stdout.write(u"\u001b[1000D")
            sys.stdout.write(u"\u001b[0K")
            sys.stdout.write(syntax_highlight(input))
            sys.stdout.write(u"\u001b[1000D")
            if index > 0:
                sys.stdout.write(u"\u001b[" + str(index) + "C")
            sys.stdout.flush()

#EOF