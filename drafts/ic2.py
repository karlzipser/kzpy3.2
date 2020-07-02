
"""
plutil -convert xml1 a.xml

import xmltodict

with open('path/to/file.xml') as fd:
    c = xmltodict.parse(fd.read())




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

import xmltodict
from json import loads, dumps
from datetime import datetime

for fname in ['a','b','c','d','e','f','g','h','i','j']:
	with open(opjD(fname+'.xml')) as fd:
	    c = xmltodict.parse(fd.read())

	clear_screen()

	

	d = c['plist']['dict']['array']['dict']


	dt = 1593336840.0 - 615054922 + 7*3600

	p = -1
	t = 0
	q = -1
	time_format_str = "%A, %B %d, %Y %I:%M"


	if False:
		for i in rlen(d):
			e = loads(dumps(d[i]))
			print i
			if 'array' in e:
				if 'dict' in e['array']:
					if type(e['array']['dict']) == list:
						for j in rlen(e['array']['dict']):
							if u'integer' in e['array']['dict'][j]:
								e['array']['dict'][j] = int(e['array']['dict'][j]['integer'])
			try:
				kprint(e)
			except:
				print(e)
			print
			raw_enter()

	assert c['plist']['dict']['array']['string'][4][:2] == 'E:'
	if c['plist']['dict']['array']['string'][5][0] == '+':
		I_start = False
	else:
		I_start = True

	for i in rlen(d):
		e = loads(dumps(d[i]))
		if 'dict' in e:
			if 'key' in e and 'real' in e:
				if 'integer' in e['dict']:
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



			if 'key' in e:
				if 'Subject' in e['key']:
					p_prev = p
					p = int(e['dict'][-3]['integer'])
					q = int(e['integer'][1])
					

					#print(str(i)+' '+e['dict'][-3]['integer'])
				else:
					pass


			if 'integer' in e['dict'] and 'string' in e:

				if e['dict']['integer'] == '18':


					if p_prev != p:
						print
					

					if p == 6:
						if I_start:
							tb = '\t\t'
							cl = 'cyan'
						else:
							tb = ''
							cl = 'yellow'
					else:
						if not I_start:
							tb = '\t\t'
							cl = 'cyan'
						else:
							tb = ''
							cl = 'yellow'
					#else:
					#	raw_enter()
					#cprint(str(p)+' '+str(q)+' '+tb+e['string']+'\t'+ts,cl)
					cprint(' '+tb+e['string']+'\t',cl)
				else:
					pass

	print

	raw_enter()



#,b