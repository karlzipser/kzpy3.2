
if 'O' not in locals():
    O=h5r('/Users/karlzipser/Desktop_19Feb19_08h49m53s/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_24Jul18_20h04m17s_local_lrc/original_timestamp_data.h5py')
    I = {}
    I['L'] = O['left_image']['vals']
    I['R'] = O['right_image']['vals']

if False:
    XYs = {}
    XYs['L'] = []
    XYs['R'] = []
    for j in range(100):
        i = np.random.randint(len(I['L']))
        for s in ['L','R']:

            CA()
            fig = figure(s)
            clf()
            mi(I[s][i],s)
            Cdat = Click_Data(FIG=fig)
            xy_list = Cdat['CLICK'](NUM_PTS=1)
            pts_plot(na(xy_list),'r')
            spause()
            XYs[s] += xy_list
            raw_enter()
        l=na(XYs['L'])
        r=na(XYs['R'])
        figure(3);clf()
        plot(l[:,1],l[:,0]-r[:,0],'r.')

    def line(x,m,b):
        return m * x + b

    popt, pcov = curve_fit(line, l[:,1], l[:,0]-r[:,0])

    h = range(94)
    d = []
    for q in h:
        d.append( popt[0]*q+popt[1])


m = 0.53979735
b = -26.22838066

if False:
    j = np.random.randint(len(I['L']))
    left_image = I['L'][j]
    right_image = I['R'][j]
    mi(left_image,'left')
    mi(right_image,'right')
    for q in range(20):
        x = 30+np.random.randint(45)
        y = m*x + b
        figure('left')
        yy = 30+np.random.randint(45)
        plot(x,yy,'r.')
        figure('right')
        plot(x+y,yy,'r.')


if True:
    XYs = {}
    XYs['L'] = []
    XYs['R'] = []
    for j in range(100):
        CA()
        i = np.random.randint(len(I['L']))
        mi(I['R'][i],'R')
        figure('R')
        xy = xy_list[0]
        xy2 = [xy[0],xy[1]-xy[1]*m+b]
        pts_plot(na([xy])-na(xy_list[0][1]*m+b,'r')
        fig = figure(s)
        
        mi(I['L'][i],'L')
        Cdat = Click_Data(FIG=fig)
        xy_list = Cdat['CLICK'](NUM_PTS=1)
        pts_plot(na(xy_list),'r')
        spause()
        XYs[s] += xy_list
        figure('R')
        
        pts_plot(na(xy_list),'r')
        spause()
        raw_enter()


#EOF
