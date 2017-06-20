from kzpy3.utils import *
print("importing kzpy3.osx_utils")
#import objc
import applescript

	
import shutil

def asr(s):
	applescript.AppleScript(s).run()

def stowe_Desktop(dst=False,save_positions=True):
    if dst==False:
        dst = opjh('Desktop_'+time_str())
    print(dst)
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
    time.sleep(1) # Need to pause because finder seems to need time to do it's work.
    y = load_obj(opj(src,'.item_positions'))
    for i in range(len(y)):
        pass
        #osa(d2n('tell application "Finder" to set desktop position of item ',i+1,' in desktop to {10,10}'))
        osa(d2n('tell application "Finder" to set desktop position of item ',i+1,' in desktop to {',y[i][0][0],',',y[i][0][1],'}'))
