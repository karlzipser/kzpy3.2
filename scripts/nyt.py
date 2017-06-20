#! //anaconda/bin/python

#import objc
#import applescript
from kzpy3.utils import *
a = """if application "Google Chrome" is running then
        tell application "Google Chrome" to make new window with properties {mode:"incognito"}
    else
        do shell script "open -a /Applications/Google\\\ Chrome.app --args --incognito"
    end if

    tell application "Google Chrome" to activate
    open location "http://nytimes.com" """
#applescript.AppleScript(a).run()
osa(a)