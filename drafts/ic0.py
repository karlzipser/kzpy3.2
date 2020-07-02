
"""
plutil -convert xml1 c.xml

import xmltodict

with open('path/to/file.xml') as fd:
    doc = xmltodict.parse(fd.read())




		<dict>
			<key>$class</key>
			<dict>
				<key>CF$UID</key>
				<integer>18</integer>
			</dict>
			<key>NS.string</key>
			<string>Yes. You can do the TED talk.</string>
		</dict>
		<string>Yes. You can do the TED talk.</string>
		<string>59CED17C-C3A6-40A8-B323-720DCAEDDEBE</string>
		<dict>
			<key>$class</key>
			<dict>
				<key>CF$UID</key>
				<integer>31</integer>
			</dict>
			<key>BaseWritingDirection</key>
			<integer>-1</integer>
			<key>Error</key>
			<dict>
				<key>CF$UID</key>
				<integer>0</integer>
			</dict>
			<key>Flags</key>
			<integer>1081349</integer>



19
----. (n=4)
    dict. (n=9)
        ----. (n=2)
            integer 31
            key CF$UID
        ----. (n=2)
            integer 0
            key CF$UID
        ----. (n=2)
            integer 38
            key CF$UID
        ----. (n=2)
            integer 33
            key CF$UID
        ----. (n=2)
            integer 35
            key CF$UID
        ----. (n=2)
            integer 37
            key CF$UID
        ----. (n=2)
            integer 11
            key CF$UID
        ----. (n=2)
            integer 6
            key CF$UID
        ----. (n=2)
            integer 34
            key CF$UID
    false None
    integer (n=2)
        -1
        1081349
    key-. (n=12)
        $class
        BaseWritingDirection
        Error
        Flags
        GUID
        IsInvitation
        IsRead
        MessageText
        OriginalMessage
        Sender
        Subject
        Time
"""


#,a

from datetime import datetime

d = c['plist']['dict']['array']['dict']


dt = 1593336840.0 - 615054922 + 7*3600

p = -1
t = 0
time_format_str = "%A, %B %d, %Y %I:%M"

for i in rlen(d):
	e = loads(dumps(d[i]))

	try:
		if e['dict']['integer'] == '15' and 'NS.time' in e['key']:
			#print(str(i)+' '+e['real'])
			t_prev = t
			t = float(e['real'])
			if t - t_prev > 300:
				ts = datetime.fromtimestamp(dt+t).strftime(time_format_str)
			else:
				ts = ''
			time_format_str = "%I:%M"
		else:
			pass
	except:
		pass


	try:
		if 'Subject' in e['key']:
			p_prev = p
			p = int(e['dict'][-3]['integer'])
			#print(str(i)+' '+e['dict'][-3]['integer'])
		else:
			pass
	except:
		pass

	try:
		if e['dict']['integer'] == '18':
			if p_prev != p:
				print
			if p == 6:
				tb = ''
				cl = 'white'
			elif p == 11:
				tb = '\t\t'
				cl = 'cyan'
			else:
				raw_enter()
			cprint(tb+e['string']+'\t'+ts,cl)
		else:
			pass
	except:
		pass



#,b