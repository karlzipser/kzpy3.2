from kzpy3.utils.common import *

def date_and_time_setting_strings():
    now = datetime.datetime.now()
    date_str = now.strftime('20%y%m%d')
    time_str = now.strftime('%H:%M:%S')
    date_str = "sudo date +%Y%m%d -s "+date_str
    time_str = "sudo date +%T -s "+time_str
    return date_str,time_str

def ssh_date_time(host_ip,user='nvidia',timeout=10):
    date_str,time_str = date_and_time_setting_strings()
    sys_str = d2n('ssh -o ConnectTimeout=',timeout,' ',user+'@'+host_ip," '",date_str,'; ',time_str,"'")
    print(sys_str)
    os.system(sys_str)

def rsync(ip,user='nvidia',timeout=10):
    os.system("rsync -ravL --exclude '*.pyc' --exclude '*.pkl' kzpy3/* nvidia@"+ip+":kzpy3/")
    cprint(d2s(ip,'finished.'),'white','on_blue')
    beep()

def update_TXs(ips=[]):
    for ip in ips:
        threading.Thread(target=rsync,args=[ip]).start()

def update_TXs_range(start,stop=None,base_ip='169.254.131'):
    if stop == None:
        stop = start+1
    ips = []
    for i in range(start,stop):
        ips.append(d2n(base_ip,'.',i))
    update_TXs(ips)

#exec(identify_file_str)

#EOF
