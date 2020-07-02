#, a
from kzpy3.vis3 import *

import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
#plt.style.use('fivethirtyeight')
# %matplotlib inline


# find your chat.db and establish a connection
conn = sqlite3.connect(opjh('Library/Messages/chat.db'))
cur = conn.cursor()

# query the database to get all the table names
cur.execute(" select name from sqlite_master where type = 'table' ")

for name in cur.fetchall():
    print(name)


# create pandas dataframe with all the tables you care about.

## Mac OSX versions below High Sierra
#messages = pd.read_sql_query('''select *, datetime(date + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message''', conn) 

## High Sierra and above
messages = pd.read_sql_query('''select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message''', conn) 
attachments = pd.read_sql_query('''select *  from attachment''', conn) 

handles = pd.read_sql_query("select * from handle", conn)
chat_message_joins = pd.read_sql_query("select * from chat_message_join", conn)
message_attachment_joins = pd.read_sql_query("select * from message_attachment_join", conn)

# these fields are only for ease of datetime analysis (e.g., number of messages per month or year)
messages['message_date'] = messages['date']
messages['timestamp'] = messages['date_utc'].apply(lambda x: pd.Timestamp(x))
messages['date'] = messages['timestamp'].apply(lambda x: x.date())
messages['month'] = messages['timestamp'].apply(lambda x: int(x.month))
messages['year'] = messages['timestamp'].apply(lambda x: int(x.year))


# rename the ROWID into message_id, because that's what it is
messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)

# rename appropriately the handle and apple_id/phone_number as well
handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)


# merge the messages with the handles
merge_level_1 = pd.merge(messages[['text', 'handle_id', 'date','message_date' ,'timestamp', 'month','year','is_sent', 'message_id']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')

# and then that table with the chats
df_messages = pd.merge(merge_level_1, chat_message_joins[['chat_id', 'message_id']], on = 'message_id', how='left')


print(len(df_messages))
#print(df_messages.head())


# save the combined table for ease of read for future analysis!
df_messages.to_csv('./imessages_high_sierra.csv', index = False, encoding='utf-8')


df_messages['date'].min(), df_messages['date'].max()


# number of messages per day
plt.plot(df_messages.groupby('date').size())
plt.xticks(rotation='45')


# how many messages you have sent versus received
df_messages.groupby('is_sent').size()


# number of messages per month and year
df_messages.groupby('month').size()
df_messages.groupby('year').size()


# close connections
cur.close()
conn.close()

if False:
	kys = sorted(messages['text'].keys())
	for k in kys:
		print messages['text'][k]
		print

if False:
	n = 12419
	for k in ['handle_id','is_from_me','text']:#messages.keys():
		print k,messages[k][n]


#,a
from kzpy3.vis3 import *
P = {}
handle_ids = handles['handle_id']
phone_numbers = handles['phone_number']
for i in rlen(handle_ids):
	P[handle_ids[i]] = phone_numbers[i] 

N = {
	'karlzipser@berkeley.edu':'Karl',
	'+15109099328':'Karl',
	'+19292708285':'Ping',
	'+15108471373':'Kelley',
}

#M = {}
O = {}
ns = sorted(messages['text'].keys())

for n in ns:

	handle_id = messages['handle_id'][n]
	#print handle_id
	if handle_id in P:
		phone = P[handle_id]
		if phone in N:
			phone = N[phone]
		message_id = messages['message_id'][n]

		if phone not in O:
			#M[phone] = {}
			O[phone] = {}

		#M[phone][message_id] = {}

		#for k in ['is_from_me','text','handle_id']:#,'timestamp']: #messages.keys():
		#	M[phone][message_id][k] = messages[k][n]

		t = messages['timestamp'][n]

		if False:
			M[phone][message_id]['year'] = t.year
			M[phone][message_id]['month'] = t.month
			M[phone][message_id]['day'] = t.day
			M[phone][message_id]['dayofweek'] = t.dayofweek
			M[phone][message_id]['daysinmonth'] = t.daysinmonth
			M[phone][message_id]['hour'] = t.hour
			M[phone][message_id]['minute'] = t.minute
			M[phone][message_id]['second'] = t.second

		if t.year not in O[phone]:
			O[phone][t.year] = {}

		if t.month not in O[phone][t.year]:
			O[phone][t.year][t.month] = {}

		if t.day not in O[phone][t.year][t.month]:
			O[phone][t.year][t.month][t.day] = {}

		if t.hour not in O[phone][t.year][t.month][t.day]:
			O[phone][t.year][t.month][t.day][t.hour] = {}

		if t.minute not in O[phone][t.year][t.month][t.day][t.hour]:
			O[phone][t.year][t.month][t.day][t.hour][t.minute] = {}

		if t.second not in O[phone][t.year][t.month][t.day][t.hour][t.minute]:
			O[phone][t.year][t.month][t.day][t.hour][t.minute][t.second] = {}

		for k in ['is_from_me','text','handle_id']:#,'timestamp']: #messages.keys():
			O[phone][t.year][t.month][t.day][t.hour][t.minute][t.second][k] = messages[k][n]

	else:
		clp(handle_id,'`wrb')

z = 'Kelley'
for y in sorted(O[z]):
	#print y
	for m in sorted(O[z][y]):
		#print m
		for d in sorted(O[z][y][m]):
			clp(m,'/',d,'/',y,s0='')
			for h in sorted(O[z][y][m][d]):
				#print h
				for mn in sorted(O[z][y][m][d][h]):
					#print mn
					for s in sorted(O[z][y][m][d][h][mn]):
						O[z][y][m][d][h][mn][s]
						#print y,m,d,h,mn,s
						txt = O[z][y][m][d][h][mn][s]['text']
						if O[z][y][m][d][h][mn][s]['is_from_me']:
							c = 'white'
						else:
							c = 'blue'
						cprint(txt,c)
						print



#,b
#EOF
