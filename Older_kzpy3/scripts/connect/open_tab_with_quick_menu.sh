#!/usr/bin/env bash

for I in 1 2 3 4
do

osascript -e 'tell application "Terminal" to activate' \
	-e 'tell application "System Events" to tell process "Terminal" to keystroke "t" using command down' \
	-e 'tell application "Terminal" to do script "n" in selected tab of the front window'


done

#EOF