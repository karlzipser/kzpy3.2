from kzpy3.vis3 import *

def get_validation_data(
    network_to_validate=None,
    num=None,
):
    weights_path = opjD('Networks',network_to_validate,'weights')

    ctime_sorted_weightfiles = sort_dir_by_ctime(weights_path)

    selected_weightfiles = []

    for i in range(0,len(ctime_sorted_weightfiles),len(ctime_sorted_weightfiles)/num):
        selected_weightfiles.append(ctime_sorted_weightfiles[i])
    if ctime_sorted_weightfiles[-1] not in selected_weightfiles:
        selected_weightfiles.append(ctime_sorted_weightfiles[-1])
    so(opjD('Networks',network_to_validate,'Val_lists'),
        {'ctime_sorted_weightfiles':ctime_sorted_weightfiles,
        'selected_weightfiles':selected_weightfiles})

    np.random.shuffle(selected_weightfiles)
    for w in selected_weightfiles:
        wait = True
        while wait:
            python_ps_ctr = 0
            processes = unix('ps -e')
            for p in processes:
                if ' python' in p:
                    python_ps_ctr += 1
            if python_ps_ctr < 10:
                wait = False
            else:
                clp(python_ps_ctr,'python_ps_ctr')
                time.sleep(10)

        sys_str =  d2s(
            "python kzpy3/Train_app/Sq120_ldr_output_4April2019/Main.py",
            "--VALIDATION_WEIGHTS_FILE_PATH",
            w,
            '&'
        )
        print sys_str
        os.system(sys_str)
        time.sleep(15)




def get_validation_curve(
    network_to_validate=None,
):
    Val_lists = lo(opjD('Networks',network_to_validate,'Val_lists'))
    ctime_sorted_weightfiles = Val_lists['ctime_sorted_weightfiles']
    selected_weightfiles = Val_lists['selected_weightfiles']
    validation_loss_files = sggo(opjD('Networks',network_to_validate,'validation_loss','*'))

    V = {}
    ctr = 0
    validation_loss_files = sggo(opjD('Networks',network_to_validate,'validation_loss','*'))

    for s in selected_weightfiles:
        V[fname(s)] = {'ctr':ctr,'lst':[]}
        ctr += 1

    for s in selected_weightfiles:
        for v in validation_loss_files:
            if fname(s) in v:
                o = lo(v)
                V[fname(s)]['lst'] += o

    validation_losses = range(len(selected_weightfiles))
    for a in V.keys():
        validation_losses[V[a]['ctr']] = np.mean(na(V[a]['lst']))

    clf()
    plot(validation_losses,'k.-')
    plt.title(d2s('validation of',network_to_validate))
    plt.ylabel('loss')
    plt.xlabel('weightfiles')
    plt.xlim(0,300)
    spause()
    return V,validation_losses


if __name__ == '__main__':
    Defaults = {
        'data':0,
        'curve':0,
        'network_to_validate':'Sq120_ldr_output_4April2019',
        'num':50,
    }
    setup_Default_Arguments(Defaults)
    print_Arguments()
    if Arguments['data']:
        get_validation_data(
            Arguments['network_to_validate'],
            Arguments['num'],
        )

    if Arguments['curve']:
        get_validation_curve(
            Arguments['network_to_validate'],
        )
        raw_enter()


