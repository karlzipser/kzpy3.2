from kzpy3.utils3 import *

Defaults = {
    'ichat_src':opjh('Library/Messages/Archive'),
    'xml_dst':opjD('kMessages/Archive'),
    'update_xml':True,

}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
A = Arguments

def test_if_msg_is_calendar_entry(msg):
    return False

def mac_safe_filename(f):
    f = f.replace(' ','\ ')
    return f

def update_xml():
    ichat_folders = sggo(A['ichat_src'],'*')

    for p in ichat_folders:
        assert os.path.isdir(p)
        f = opj(A['xml_dst'],fname(p))
        os.system(d2s('mkdir -p',f))
        ichat_files = sggo(p,'*')

        for c in ichat_files:
            s = fname(c)
            g = opj(f,s)

            if not os.path.lexists( g ) or os.path.getmtime(c) > os.path.getmtime(g):
                pass
            else:
                continue
            print g

            os.system(d2s('cp',"'"+c+"'","'"+g+"'"))
            os.system(d2s("plutil -convert xml1","'"+g+"'"))

def main():

    if A['update_xml']:
        update_xml()

    d_path = opj(pname(A['xml_dst']),'D.pkl')

    if os.path.lexists(d_path):
        d_mtime = os.path.getmtime(d_path)
        D = lo(d_path)
    else:
        D = {}
        d_mtime = time.time()

if __name__ == '__main__':
    main()

if True:
    Is_Me = {
        6:True,
        11:False,
    }
else:
    Is_Me = {
        11:True,
        6:False,
    }


R = {
    'phone':'1501401141',
    'timestamps':[
        {
            6345335.142342:
                {
                    'is_me':False,
                    'text':'This is the third time.',
                }
        },
        {
            6345335.142342:
                {
                    'is_me':False,
                    'text':'This is the third time.',
                }
        },
    ],
}

#EOF