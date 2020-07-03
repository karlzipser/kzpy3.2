#,a



from kzpy3.utils3 import *
import xmltodict
from json import loads, dumps
from datetime import datetime
import rtfunicode


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




dt = 1593336840.0 - 615054922 + 7*3600
time_format_str = "%A, %B %d, %Y %H:%M"




def parse_xml(fnm):
    a = fname(fnm).split(" on ")
    correspondent = get_safe_name(a[0],safe_chars=['+','.','@','-'],replacement_char=' ',condense=True)
    b = a[1].split(' at ')
    text_date = get_safe_name(b[0],safe_chars=['+','.','@','-'],replacement_char=' ',condense=True)
    text_time = get_safe_name(b[1],safe_chars=['+','.','@','-'],replacement_char=' ',condense=True).replace('.ichat','')


    with open(opjD(fnm)) as fd:
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
    timestamps_str = []
    mes = []
    texts = []

    for i in rlen(d):

        e = loads(dumps(d[i]))
        if 'dict' in e:
            if 'key' in e and 'real' in e:
                if 'integer' in e['dict']:
                    if e['dict']['integer'] == '15' and 'NS.time' in e['key']:
                        t = float(e['real'])
                        timestamps.append(t)
                        timestamps_str.append(datetime.fromtimestamp(dt+t).strftime(time_format_str))
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
        #print 'texts start'
        #for t in texts:
        #    print(t)
        #print 'texts end'
        phone = texts[-1]
    except:
        clp(texts,'`wr')
        clp(timestamps,'`wr')
        clp(mes,'`wr',r=0)
        return {
            'Error':True,
            'timestamps':timestamps,
            'mes':mes,
            'texts':texts,
        }


    lst = []
    T = {}

    try:
        for i in rlen(timestamps):
            lst.append({timestamps[i]:{'me':mes[i],'text':texts[i]}})
            T[timestamps[i]] = {'me':mes[i],'text':texts[i],'ts':timestamps_str[i]}
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

    R['correspondent'] = correspondent
    R['text_date'] = text_date
    R['text_time'] = text_time

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




Metamers = {}
for m in metamers:
    v = m[0]
    for k in m[1:]:
        Metamers[k] = v


def update_dic():

    dname = opj(pname(A['xml_dst']),'R.pkl')

    if os.path.lexists(dname):
        R = lo(dname,noisy=False)
    else:
        R = {
            'correspondent':{}
        }

    xml_folders = sggo(A['xml_dst'],'*')

    for p in xml_folders:
        assert os.path.isdir(p)
        pkl_files = sggo(p,'*.pkl')
        for x in pkl_files:
            R0 = lo(x,noisy=False)
            if 'Error' in R0:
                continue
            correspondent = R0['correspondent']
            if correspondent in Metamers:
                c = Metamers[correspondent]
                cm(correspondent,'->',c)
                correspondent = c
            if correspondent not in R['correspondent']:
                R['correspondent'][correspondent] = {}
            for timestamp in R0['texts']:
                text = R0['texts'][timestamp]
                R['correspondent'][correspondent][timestamp] = text

    return R

                




def R_str(R,correspondent):
    C = R['correspondent'][correspondent]
    ts = sorted(C.keys())
    t_prev = 0
    str_lst = []
    for t in ts:
        if t - t_prev > 60*60:
            tstr = datetime.fromtimestamp(dt+t).strftime(time_format_str)
            str_lst.append(tstr)
            t_prev = t
        if C[t]['me']:
            idstr = ' &&&cf2 '
        else:
            idstr = ' &&&cf0 '
        try:
            str_lst.append(idstr + C[t]['text'])
        except:
            cr(correspondent,idstr,C[t]['text'],'failed')

    return str_lst


def rtf_encode_char(unichar):
    code = ord(unichar)
    if code < 128:
        return str(unichar)
    return '\\u' + str(code if code <= 32767 else code-65536)

def rtf_encode(unistr):
    return ''.join(rtf_encode_char(c) for c in unistr)





rtf_header = """

{\\rtf1\\ansi\\ansicpg1252\cocoartf1561\cocoasubrtf610
{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;\\f1\\fnil\\fcharset0 AppleColorEmoji;}
{\colortbl;\\red255\green255\\blue255;\\red243\green0\\blue146;\\red33\green255\\blue6;}
{\*\expandedcolortbl;;\\cssrgb\\c57337\\c57337\c57337;\\cssrgb\\c1611\\c27337\\c63799;}
\margl1440\margr1440\\vieww10800\\viewh8400\\viewkind0
\pard\\tx720\\tx1440\\tx2160\\tx2880\\tx3600\\tx4320\\tx5040\\tx5760\\tx6480\\tx7200\\tx7920\\tx8640\pardirnatural\partightenfactor0

"""







def main():

    if A['update_xml']:
        update_xml()
    update_pkl()

    R = update_dic()
    
    so(opj(pname(A['xml_dst']),'R.pkl'),R)

    for c in R['correspondent'].keys():

        if True:#try:
            save_lst = [rtf_header]

            save_lst.append("\\f0\\fs64 \\cf0 "+c+"\n\\f1\n\\fs30 \\")



            sl = R_str(R,c)
            #print "\\f1\\fs64 " + c +"\n\\fs24 \\" 

            for s in sl:
                s = s.replace('?','^^^')
                r = s.encode('rtfunicode').replace('?','').replace('&&&','\\')
                #print '\\f0 ' + r.replace('^^^','?') + ' \\'
                save_lst.append('\\f0 ' + r.replace('^^^','?') + ' \\\n\\')
            save_lst.append('}')

            dname = opj(pname(A['xml_dst']),'printouts',c+'.rtf')

            os.system(d2s('mkdir -p',pname(dname)))

            list_of_strings_to_txt_file(dname,save_lst)
        else:#except:
            cr(c,'failed')
#,b

if __name__ == '__main__':
    main()


#EOF