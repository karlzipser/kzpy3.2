
def find_files_recursively(src,pattern,FILES_ONLY=False,DIRS_ONLY=False):
    """
    https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
    """
    files = {}
    folders = {}
    ctr = 0
    timer = Timer(5)
    if src[-1] != '/':
        src = src + '/'
    src2 = src[:-1]
    print(d2s('src =',src,'pattern =',pattern))
    for root, dirnames, filenames in os.walk(src):
        assert(not(FILES_ONLY and DIRS_ONLY))
        if FILES_ONLY:
            use_list = filenames
        elif DIRS_ONLY:
            use_list = dirnames
        else:
            use_list = filenames+dirnames
        for filename in fnmatch.filter(use_list, pattern):
            file = opj(root,filename)
            folder = pname(file).replace(src2,'')
            file = fname(file)
            if file not in files:
                files[file] = []
            files[file].append(folder)
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(filename)
            ctr += 1
            if timer.check():
                print(d2s(time_str('Pretty'),ctr,'matches'))
                timer.reset()
    return folders,files


def find_host_folders(src,pattern):
    folders,files = find_files_recursively(src,pattern)
    the_folders = {}
    for f in folders.keys():
        if fname(f) not in the_folders:
            the_folders[fname(f)] = []
        the_folders[fname(f)].append([len(folders[f]),pname(f)])
    return the_folders


