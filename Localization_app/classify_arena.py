from kzpy3.utils2 import *

markers_clockwise_Smyth_Fern_arena = [56,62,55,61,
	134,133,139,138,
	199,200,202,203,
	204,205,208,206,
	174,175,176,177,
	57,58,67,59,
	173,172,171,170,
	5,53,54,60,
	153,152,151,150,
	169,168,167,165,
	207,209,210,211,
	154,155,156,157,
	215,212,213,214,
	227,226,228,225,
	216,217,218,219,
	223,222,221,220,
	66,70,64,65,
	132,137,136,135,
	198,196,197,194,
	140,141,143,142,
	68,69,74,6,
	162,163,164,166,
	229,131,144,145,
	190,188,193,195,
	48,46,49,47,
	161,160,159,158]

p1=[199,200,202,203]
p2=[204,205,208,206]
p3=[174,175,176,177]
p4=[57,58,67,59]
p5=[173,172,171,170]

p6=[227,226,228,225]
p7=[153,152,151,150]
p8=[134,133,139,138]
p9=[216,217,218,219] 

p10=[223,222,221,220]
p11=[169,168,167,165]
p12=[207,209,210,211]
p13=[132,137,136,135]
p14=[161]
p15=[55,61]
p16=[160,159,158]
p17=[182,183,184,201]
p18=[51,50,4,63]
p19=[146,147,148,149]
p20=[52,189,192,191]
markers_clockwise_whole_room = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20

p1=[199,200,202,203]
p2=[204,205,208,206]
p3=[174,175,176,177]
p4=[57,58,67,59]
p5=[173,172,171,170]
p6=[227,226,228,225]
p7=[153,152,151,150]
p8=[134,133,139,138]
p9=[216,217,218,219] 
p10=[223,222,221,220]
p11=[169,168,167,165]
p12=[207,209,210,211]
markers_clockwise_12circle = p4+p5+p6+p7+p8+p9+p10+p11+p12+p1+p2+p3

p1=[199,200,202,203]	#
p2=[204,205,208,206]	# K
p3=[174,175,176,177]	# J
p4=[57,58,67,59]		# I
p5=[173,172,171,170]	# H
p6=[227,226,228,225]	# G
p7=[153,152,151,150]	# F
p8=[134,133,139,138]	# E
p9=[216,217,218,219]	# D
p10=[223,222,221,220]	# C
p11=[169,168,167,165]	# B
p12=[207,209,210,211]	# A
markers_clockwise_11circle = p4+p5+p6+p7+p8+p9+p10+p11+p12   +    p2+p3

p2=[201,184,183,182]	# +
p3=[174,175,176,177]	# J
p4=[214,213,212,215]	# +
p5=[173,172,171,170]	# H
p6=[135 ,136,137,132]	# +
p7=[153,152,151,150]	# F
p8=[134,133,139,138]	# E
p9=[157,156,155,154]	# +
p10=[223,222,221,220]	# C
p11=[65,64,70,66]		# +
p12=[207,209,210,211]	# A
markers_clockwise_11circle_half_raised = p4+p5+p6+p7+p8+p9+p10+p11+p12   +    p2+p3


p2=[182,183,184,201]	# + door
p3=[178,179,180,181]	# J
p4=[66,70,64,65]	# +
p5=[51,50,4,63]	# H
p6=[154,155,156,157]	# +
p7=[52,189,192,191]	# F
p8=[146,147,148,149]	# E fireplace
p9=[132,137,136,135]	# +
p10=[199,200,202,203]	# C
p11=[215,212,213,214]		# +
p12=[198,196,197,194]	# A windows
markers_clockwise_11circle_full_raised = p4+p5+p6+p7+p8+p9+p10+p11+p12+p2+p3

all_markers = {}
for m in markers_clockwise_Smyth_Fern_arena+markers_clockwise_whole_room+markers_clockwise_12circle+markers_clockwise_11circle+markers_clockwise_11circle_half_raised+markers_clockwise_11circle_full_raised:
	all_markers[m] = True
del(all_markers[190])
del(all_markers[131])




def classify_arena(aruco_data):
	results = []
	for markers_clockwise in [markers_clockwise_Smyth_Fern_arena,markers_clockwise_whole_room,markers_clockwise_12circle,markers_clockwise_11circle,markers_clockwise_11circle_half_raised,markers_clockwise_11circle_full_raised]:

		markers = {}
		for side in ['left','right']:
			for q in aruco_data[side+'_image_aruco'][vals]:
				for m in q['angles_to_center'].keys():
					if m in all_markers:
						markers[m] = True


		false_positives = {}

		ctr1 = 0
		#print 'markers not in markers_clockwise:'
		for m in markers_clockwise:
			if m not in markers:
				#print m
				ctr1 += 1
		#pd2s('len(markers) =',len(markers),'len(markers_clockwise) =',len(markers_clockwise))

		ctr2 = 0
		#print 'markers_clockwise not in markers:'
		for m in markers:
			if m not in markers_clockwise:
				#print m
				ctr2 += 1

		for m in markers:
			if m not in markers_clockwise:
				false_positives[m] = True

		#pd2s('false positives:',false_positives.keys())

		results += [(dp(ctr1/(1.0*len(markers)),1),dp(ctr2/(1.0*len(markers)),1))]
	return results


# results = classify_arena(lo(opj(r,'aruco_data.pkl'),noisy=False))











