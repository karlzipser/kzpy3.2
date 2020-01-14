from kzpy3.utils3 import *

val_runs = [
    'tegra-ubuntu_16Nov18_15h59m28s',
    'tegra-ubuntu_01Nov18_13h46m55s',
    'Mr_Black_24Sep18_18h52m26s',
    'tegra-ubuntu_07Oct18_18h24m28s',
    'tegra-ubuntu_17Oct18_12h11m22s',
    'tegra-ubuntu_12Oct18_11h11m30s',
    'tegra-ubuntu_25Oct18_10h21m55s',
    'tegra-ubuntu_12Nov18_20h56m16s',
    'tegra-ubuntu_25Oct18_15h43m36s',
]


train_runs = [
    'Mr_Black_18Sep18_18h06m34s',
    'tegra-ubuntu_16Oct18_11h24m21s',
    'tegra-ubuntu_26Oct18_09h14m36s',
    'Mr_Black_26Jul18_20h03m31s',
    'tegra-ubuntu_08Oct18_19h15m18s',
    'tegra-ubuntu_15Nov18_20h51m52s',
    'tegra-ubuntu_24Oct18_16h38m19s',
    'tegra-ubuntu_31Oct18_16h06m32s',
    'tegra-ubuntu_22Oct18_15h11m34s',
    'tegra-ubuntu_29Oct18_13h28m05s',
    'tegra-ubuntu_01Nov18_16h25m40s',
    'tegra-ubuntu_21Oct18_17h22m36s',
    'tegra-ubuntu_21Oct18_16h49m30s',
    'Mr_Black_08Sep18_16h11m59s',
    'tegra-ubuntu_02Nov18_17h09m48s',
    'tegra-ubuntu_29Oct18_14h05m23s',
    'tegra-ubuntu_02Nov18_10h06m03s',
    'tegra-ubuntu_16Oct18_17h02m43s',
    'tegra-ubuntu_18Oct18_08h14m24s_b',
    'tegra-ubuntu_26Oct18_08h37m07s',
    'tegra-ubuntu_17Oct18_12h46m32s',
    'Mr_Black_25Sep18_16h32m32s',
    'Mr_Black_28Sep18_13h55m17s',
    'Mr_Black_26Sep18_19h14m00s',
    'tegra-ubuntu_16Nov18_15h29m20s',
    'tegra-ubuntu_07Oct18_11h38m15s',
    'Mr_Black_30Sep18_18h34m01s',
    'tegra-ubuntu_19Oct18_11h33m22s',
    'Mr_Black_27Sep18_14h51m07s',
    'tegra-ubuntu_07Oct18_18h59m59s',
    'Mr_Black_04Oct18_18h16m14s',
    'Mr_Black_24Sep18_13h19m51s',
    'tegra-ubuntu_16Nov18_13h02m06s',
    'tegra-ubuntu_02Nov18_15h29m59s',
    'Mr_Black_21Sep18_18h42m46s',
    'tegra-ubuntu_15Nov18_20h55m02s',
    'Mr_Black_24Jul18_20h04m17s_local_lrc',
    'tegra-ubuntu_19Oct18_08h55m02s',
    'Mr_Black_03Oct18_11h27m02s',
    'Mr_Black_29Sep18_19h05m09s',
    'tegra-ubuntu_11Oct18_17h11m39s',
    'tegra-ubuntu_16Oct18_10h02m45s',
    'tegra-ubuntu_30Oct18_15h58m09s',
    'Mr_Black_08Sep18_16h57m06s',
    'Mr_Black_25Jul18_14h44m55s_local_lrc',
    'tegra-ubuntu_01Nov18_17h00m24s',
    'tegra-ubuntu_08Oct18_10h46m44s',
    'tegra-ubuntu_16Oct18_17h42m25s',
    'Mr_Black_25Jul18_14h29m56s_local_lrc',
    'tegra-ubuntu_01Nov18_13h09m32s',
    'tegra-ubuntu_22Oct18_15h48m48s',
    'tegra-ubuntu_18Oct18_16h15m46s',
    'tegra-ubuntu_31Oct18_16h47m50s',
    'tegra-ubuntu_18Oct18_17h10m29s',
    'tegra-ubuntu_19Oct18_12h22m42s',
    'tegra-ubuntu_15Nov18_20h53m56s',
    'tegra-ubuntu_28Oct18_17h27m55s',
    'Mr_Black_25Sep18_11h41m45s',
    'tegra-ubuntu_08Oct18_18h09m29s',
    'tegra-ubuntu_02Nov18_12h24m59s',
    'tegra-ubuntu_23Oct18_17h19m34s',
    'tegra-ubuntu_18Oct18_08h43m23s',
    'tegra-ubuntu_24Oct18_17h15m14s',
    'Mr_Black_25Jul18_19h55m13s',
    'Mr_Black_27Jul18_18h46m35s',
    'Mr_Black_03Oct18_19h11m35s',
    'tegra-ubuntu_25Oct18_16h17m55s',
    'tegra-ubuntu_29Oct18_17h22m22s',
    'Mr_Black_04Oct18_18h53m06s',
    'tegra-ubuntu_15Nov18_20h52m26s',
    'Mr_Black_27Jul18_17h55m00s',
    'Mr_Black_02Oct18_18h16m32s',
    'tegra-ubuntu_08Oct18_19h16m15s',
    'Mr_Black_05Oct18_17h18m02s_lost_IMU_early',
    'Mr_Black_01Oct18_18h58m41s',
    'tegra-ubuntu_16Oct18_09h27m05s',
    'tegra-ubuntu_19Oct18_11h46m46s',
    'tegra-ubuntu_15Oct18_18h47m18s',
    'tegra-ubuntu_02Nov18_16h04m58s',
    'Mr_Black_03Oct18_11h11m38s',
    'tegra-ubuntu_08Oct18_18h36m24s',
    'tegra-ubuntu_29Oct18_16h45m16s',
    'tegra-ubuntu_21Oct18_15h22m18s',
    'tegra-ubuntu_15Nov18_20h52m45s',
    'tegra-ubuntu_08Oct18_19h15m15s',
    'tegra-ubuntu_08Oct18_19h15m21s',
    'Mr_Black_29Jul18_18h56m59s',
]

pcom = "python kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019__save_Fire_data/Main.py --RUN " #tegra-ubuntu_01Nov18_13h09m32s

#time.sleep(rndint(2*minutes))
for r in train_runs+val_runs:
    next = False
    in_progress = sggo(opjD('Activations','data','*'))
    for i in in_progress:
        #cm(r,i,ra=1)
        if r in i:
            next = True
            break
    if next:
        cy('skipping',r)
        continue
    #time.sleep(rndint(2*minutes))
    clp('processing',r,'`rwb')
    os.system('touch '+opjD('Activations','data',r+'.h5py'))
    #raw_enter()
    os.system(pcom+r)
    
    #print pcom+r

