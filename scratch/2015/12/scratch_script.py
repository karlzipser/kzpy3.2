import theano.tensor as T
from theano import pp
from theano import function

x_ = T.dmatrix('x')
y_ = T.dmatrix('y')
z_ = x_ + y_
Add__ = function([x_,y_],z_)

A = np.array([[2.,1.,1.],[4.,-6.,0.],[-2.,7.,2.]])

x = np.array([[1.],[1.],[2.]])



print Add__(A,A)
print A+A

w_ = T.dot(x_,y_)
Mult__ = function([x_,y_],w_)

print A.dot(x)
print Mult__(A,x)

############

def dp(f,n):
    f *= 10.0**n
    f = int(f)
    return f/(10.0**n)

############
l = txt_file_to_list_of_strings(opjh('scratch/2015/11/RPi_images/25Jan16_09h02m20s/session_list-25Jan16_09h02m20s.txt'))
command_dic = {}
for s in l:
    f = s.split(' ')[0]
    command_dic[f] = s

from kzpy3.vis import *

#img_dic = {}
img_folder = opjh('scratch/2015/11/RPi_images/25Jan16_09h02m20s/jpg')
#img_filenames = sorted(gg(opj(img_folder,'*.*')),key=natural_keys)
_,img_filenames = dir_as_dic_and_list((opj(img_folder)))
for i in range(2000,len(img_filenames)):
    f = img_filenames[i]
    print f
    if f not in img_dic:
        img_dic[f] = imread((opj(img_folder,f)))
    plt.clf()
    mi(img_dic[f],img_title=command_dic[f])
    plt.show()
    plt.ion()
    plt.pause(0.001)



############
motor_freq = 50
motor_ds = 0
servo_freq = 50
servo_ds = 0

servo_pwm_right_max = 11
servo_pwm_left_min = 7.2
servo_pwm_center = 9.5

def steering_freq(mouse_x):
    if mouse_x < 0.5:
        return servo_pwm_center - 2 * (0.5 - mouse_x) * (servo_pwm_center - servo_pwm_left_min)
    else:
        return servo_pwm_center + 2 * (mouse_x - 0.5) * (servo_pwm_right_max - servo_pwm_center) 

############
"server side"
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8080))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(64)
    if len(buf) > 0:
        print buf
        #break
############
"Client Side:"

import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8080))
clientsocket.send(raw_input())
clientsocket.close()

############



############
from kzpy3.vis import *
a=np.random.randn(10000)
hist(a,100)
plt.show()
############
import applescript
import shutil

dst = opjh('Desktop_'+time_str())

def stowe_Desktop(dst,save_positions=True):
    a="""
    tell application "Finder"
        tell every item of desktop
            get name
        end tell
    end tell
    """
    b="""
    tell application "Finder"
        
        get {desktop position, name} of item ITEM_NUM of desktop
        
    end tell"""

    w = applescript.AppleScript(a).run()
    y = []
    for x in range(len(w)):
        c = b.replace('ITEM_NUM',str(x+1))
        y.append(applescript.AppleScript(c).run())
    pprint(y)
    unix('mkdir -p ' + dst)
    _,l = dir_as_dic_and_list(opjD(''))
    for i in l:
        shutil.move(opjD(i),dst)
    if save_positions:
        save_obj(y,opj(dst,'.item_positions'))

def restore_Desktop(src):
    _,l = dir_as_dic_and_list(opjD(''))
    print(l)
    print(len(l))
    if len(l) > 0:
        print('**** Cannot restore Desktop because Desktop is not empty.')
        return False
    _,l = dir_as_dic_and_list(src)
    for i in l:
        shutil.move(opjh(src,i),opjD(''))
    time.sleep(1)
    y = load_obj(opj(src,'.item_positions'))
    for i in range(len(y)):
        pass
        #osa(d2n('tell application "Finder" to set desktop position of item ',i+1,' in desktop to {10,10}'))
        osa(d2n('tell application "Finder" to set desktop position of item ',i+1,' in desktop to {',y[i][0][0]-1,',',y[i][0][1],'}'))

############
tell application "Finder"
        set position of item 1 of desktop to {2300,100}
end tell
############
############
from kzpy3.vis import *
a=np.random.randn(10000)
hist(a,100)
plt.show()
############
import objc
import applescript
a = """if application "Google Chrome" is running then
        tell application "Google Chrome" to make new window with properties {mode:"incognito"}
    else
        do shell script "open -a /Applications/Google\\\ Chrome.app --args --incognito"
    end if

    tell application "Google Chrome" to activate
    open location "http://nytimes.com" """
applescript.AppleScript(a).run()

############
def say(t):
    unix('say '+t)
#############
def getClipboardData():
 p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
 retcode = p.wait()
 data = p.stdout.read()
 return data

def setClipboardData(data):
 p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
 p.stdin.write(data)
 p.stdin.close()
 retcode = p.wait()
############
c = load_obj('/tmp/zpy_vars/c')
#c = zload('c')
for d in c:
	if len(d)>0:
		unix('say --interactive=/green -r 200 '+d)
		raw_input('...')
############

print opjh()
############

from kzpy3.vis import *
mi(imread(opjh('Pictures/bay2.png')),2)
plt.show()
############

a = 1+1
b = 3
c = a**b
print(c)

############
a = re.split("#+","########### 213 ########")
n = np.int(''.join(a).replace(' ',''))
print(n)
############
import shelve

T='Hiya'
val=[1,2,3]

filename=opjD('shelve.out')
my_shelf = shelve.open(filename,'n') # 'n' for new

for key in dir():
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()

############
tell application "Finder"
    
    get {desktop position, name} of "untitled folder" desktop
    
end tell
############
tell application "Finder"
    set filelist to name of every file in desktop
end tell
############
tell application "Finder"
    
    get {desktop position, name} of item 2 of desktop
    
end tell
############
tell application "Finder"
    tell every item of desktop
        get name
    end tell
end tell
############
############
############
############
############
############
