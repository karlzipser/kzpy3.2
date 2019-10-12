#,a
for k in R.keys():
	for l in R[k].keys():
		if 'tegra' not in l:
			continue
		if l not in run_names:
			pd2s(k,l,'not in runs')

#,b