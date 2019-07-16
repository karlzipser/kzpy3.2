path = opjD('Mr_Purple_10Jul19_13h21m39s')
L = h5r(opj(path,'left_timestamp_metadata_right_ts.h5py'))

encoder = L['encoder'][:]
motor = L['motor'][:]
button_number = L['button_number'][:]

e4 =[]
m4 = []
for i in rlen(button_number):
	if button_number[i] == 4:
		e4.append(encoder[i])
		m4.append(motor[i])
clf();plot(m4,e4,'.');spause()

#,
o=loD('xy_points')
#,a
CA()
pts_plot(o)

forward = []
backward = []
for i in rlen(o):
	m = o[i][0]
	e = o[i][1]
	if m >= 55 and m <= 71:
		forward.append([m,e])
	if m >= 20 and m <= 39:
		backward.append([m,e])

forward = na(forward)
backward = na(backward)

x = forward[:,0]
y = forward[:,1]
mf,bf = curve_fit(f___,x,y)[0]

x = backward[:,0]
y = backward[:,1]
mb,bb = curve_fit(f___,x,y)[0]
#,
motors_all = range(0,99)
motors_f = []
encoders_f = []
motors_b = []
encoders_b = []
for motor in motors_all:
	ef = mf*motor+bf
	eb = mb*motor+bb
	if ef >= 0 and ef <= 12:
		encoders_f.append(ef)
		motors_f.append(motor)
	if eb >= -8 and eb <= 0:
		encoders_b.append(eb)
		motors_b.append(motor)
plot(motors_f,encoders_f,'k')
plot(motors_b,encoders_b,'k')
#,b
#EOF
