#,a
from kzpy3.utils3 import *

#import parse_xml

Defaults = {
    'ichat_src':opjh('Library/Messages/Archive'),
    'xml_dst':opjD('kMessages/Archive'),
    'update_xml':True,
    'update_pkl':True,
    'update_dic':True,
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
A = Arguments







import xmltodict
from json import loads, dumps
from datetime import datetime
from kzpy3.utils3 import *


def parse_xml(fname):

    with open(opjD(fname)) as fd:
        c = xmltodict.parse(fd.read())

    d = c['plist']['dict']['array']['dict']

    p = -1
    t = 0

    assert c['plist']['dict']['array']['string'][4][:2] == 'E:'
    if c['plist']['dict']['array']['string'][5][0] == '+':
        I_start = False
    else:
        I_start = True

    timestamps = []
    mes = []
    texts = []

    for i in rlen(d):

        e = loads(dumps(d[i]))
        if 'dict' in e:
            if 'key' in e and 'real' in e:
                if 'integer' in e['dict']:
                    if e['dict']['integer'] == '15' and 'NS.time' in e['key']:

                        timestamps.append(float(e['real']))

                    else:
                        pass


            if 'key' in e:
                if 'Subject' in e['key']:

                    p = int(e['dict'][-3]['integer'])

                else:
                    pass

            if 'integer' in e['dict'] and 'string' in e:

                if e['dict']['integer'] == '18':

                    if p == 6:
                        if I_start:
                            me = True
                        else:
                            me = False
                    elif p == 11:
                        if not I_start:
                            me = True
                        else:
                            me = False
                    else:
                        clp(p,me,e['string'],'`yrb',r=0)
                        return {
                            'Error':True,
                            'timestamps':timestamps,
                            'mes':mes,
                            'texts':texts,
                            'p':p,
                            'string':e['string'],
                            }
                        assert False

                    mes.append(me)
                    texts.append(e['string'])
                else:
                    pass
    try:
        print 'texts start'
        for t in texts:
            print(t)
        print 'texts end'
        phone = int(texts[-1])
    except:
        clp(texts,'`wr')
        clp(timestamps,'`wr')
        clp(mes,'`wr',r=1)
        return {
            'Error':True,
            'timestamps':timestamps,
            'mes':mes,
            'texts':texts,
            #'p':p,
            #'string':e['string'],
        }


    lst = []
    T = {}

    try:
        for i in rlen(timestamps):
            lst.append({timestamps[i]:{'me':mes[i],'text':texts[i]}})
            T[timestamps[i]] = {'me':mes[i],'text':texts[i]}
        R = {
            'phone':phone,
            'texts':T,
        }
    except KeyboardInterrupt:
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)     
        clp(texts,'`gr')
        clp(timestamps,'`gr')
        clp(mes,'`gr',r=0)
        return {
            'Error':True,
            'timestamps':timestamps,
            'mes':mes,
            'texts':texts,
            #'p':p,
            #'string':e['string'],
        }       

    return R











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
        ichat_files = sggo(p,'*.ichat')

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




def update_pkl():

    xml_folders = sggo(A['xml_dst'],'*')

    for p in xml_folders:
        assert os.path.isdir(p)
        f = opj(A['xml_dst'],fname(p))

        xml_files = sggo(p,'*.ichat')

        for x in xml_files:

            pkl = x.replace('.ichat','.pkl')
            if not os.path.lexists( pkl ) or os.path.getmtime(x) > os.path.getmtime(pkl):
                pass
            else:
                continue
            cm(pkl)

            R = parse_xml(x)
            pprint(R)
            print()

            so(pkl,R)





def update_dic():

    dname = opj(pname(A['xml_dst']),'R.pkl')

    if os.path.lexists(dname):
        R = lo(dname)
    else:
        R = {
            'phone':{}
        }

    xml_folders = sggo(A['xml_dst'],'*')

    for p in xml_folders:
        assert os.path.isdir(p)
        pkl_files = sggo(p,'*.pkl')
        for x in pkl_files:
            R0 = lo(x)
            if 'Error' in R0:
                continue
            phone = R0['phone']
            if phone not in R['phone']:
                R['phone'][phone] = {}
            for timestamp in R0['texts']:
                text = R0['texts'][timestamp]
                R['phone'][phone][timestamp] = text

    return R

                









def main():

    if A['update_xml']:
        update_xml()
    update_pkl()
    R = update_dic()
    """
    d_path = opj(pname(A['xml_dst']),'D.pkl')

    if os.path.lexists(d_path):
        d_mtime = os.path.getmtime(d_path)
        D = lo(d_path)
    else:
        D = {}
        d_mtime = time.time()
    """

#,b

if __name__ == '__main__':
    main()


#EOF