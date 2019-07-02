#!/usr/bin/env python
from kzpy3.vis3 import *
exec(identify_file_str)

baudrate = 115200
timeout = 0.1

km_per_one_degree_of_latitude_38_degrees = 110.99421 # 111.03 
km_per_one_degree_of_longitude_38_degrees = 87.97371 # 85.39
garden_table_latitude = 37.88139 
garden_table_longitude = -122.27233

def gps_to_km(
    lat,
    lon,
    lat_ref=garden_table_latitude,
    lon_ref=garden_table_longitude,
):
    x = -km_per_one_degree_of_longitude_38_degrees * (lon-lon_ref)
    y = km_per_one_degree_of_latitude_38_degrees * (lat-lat_ref)
    return x,y

def get_arduino_serial_connections(baudrate, timeout):
    if using_linux():
        arduino_serial_prefix = 'ttyACM'
    elif using_osx():
        arduino_serial_prefix = 'tty.usbmodem141'
    sers = []
    ACM_ports = [opj('/dev', p) for p in os.listdir('/dev') if arduino_serial_prefix in p]
    for ACM_port in ACM_ports:
        try:
            sers.append(serial.Serial(ACM_port, baudrate=baudrate, timeout=timeout))
            cy('Opened {0}'.format(ACM_port))
        except:
            pass
    return sers

def assign_serial_connections(P,sers):
    ctr = 0
    timer = Timer(30)
    timer2 = Timer(1)
    P['Arduinos'] = {}
    for ser in sers:
        for _ in xrange(100000):

            try:
                ser_str = ser.readline()
                if len(ser_str) > 0:
                    cy(ctr,ser_str)
                ctr += 1
                exec('ser_tuple = list({0})'.format(ser_str))
                if ser_tuple[0] in ['GPS3']:
                    spd2s('Port',ser.port,'is the GPS3:',ser_str)
                    CS("\tusing 'GPS3'",emphasis=True)
                    P['Arduinos']['GPS3'] = ser
                    break
                else:
                    continue               
            except:
                pass
        else:
            CS_('Unable to identify port {0}'.format(ser.port))
    cy('Finished scanning serial ports.')

w = 300
M = CV2Plot(
    height_in_pixels=w,
    width_in_pixels=w,
    pixels_per_unit=w/1000.,
)
N = CV2Plot(
    height_in_pixels=w,
    width_in_pixels=w,
    pixels_per_unit=w/100.,
)

def show_(xys_raw):
    
    #cm(0)
    xys = na(xys_raw)
    xys[:,0] -= xys[0,0]#garden_table_latitude
    xys[:,1] -= xys[0,1]#garden_table_longitude
    xys[:,0] *= km_per_one_degree_of_latitude_38_degrees * 1000
    xys[:,1] *= km_per_one_degree_of_longitude_38_degrees * 1000
    #cm(1)
    a=0*xys
    a[:,0]=xys[:,1]
    a[:,1]=xys[:,0]
    M['clear']()
    M['pts_plot'](a)
    M['show'](title='M')
    #cm(2)
    xys = na(xys_raw)
    xys[:,0] -= xys[-1,0]
    xys[:,1] -= xys[-1,1]
    xys[:,0] *= km_per_one_degree_of_latitude_38_degrees * 1000
    xys[:,1] *= km_per_one_degree_of_longitude_38_degrees * 1000
    a=0*xys
    #cm(3)
    a[:,0]=xys[:,1]
    a[:,1]=xys[:,0]
    N['clear']()
    N['pts_plot'](a)
    N['show'](title='N')

if __name__ == '__main__':
    # python kzpy3/drafts/osx_gps.py
    flush_seconds = 0.1
    flush_timer = Timer(flush_seconds)
    P = {}
    sers = get_arduino_serial_connections(baudrate,timeout)
    assign_serial_connections(P,sers)
    file_timer = Timer(120)
    data = []
    xys = []
    os.system('mkdir -p '+opjD('GPS3'))
    start_time = time.time()
    while True:
        if file_timer.check():
            file_timer.reset()
            so(opjD('GPS3',d2n(start_time,'_',int(time.time()-start_time),'.pkl')),{'data':data,'xys':xys})
            #data = []
            #xys = []
        try:
            read_str = P['Arduinos']['GPS3'].readline()
            #cg('read_str =',read_str,sf=0)
            if flush_timer.check():
                P['Arduinos']['GPS3'].flushInput()
                P['Arduinos']['GPS3'].flushOutput()
                flush_timer.reset()            
            exec('GPS3_input = list({0})'.format(read_str))       
            m = GPS3_input[0]
            assert(m in ['GPS3'])
            GPS3_input.append(time.time())
            data.append(GPS3_input)
            #x,y = gps_to_km(GPS3_input[1],GPS3_input[2])
            x,y = GPS3_input[1],GPS3_input[2]
            xys.append([x,y])
            cb('GPS3_input =',GPS3_input)
            show_(xys)

        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            """
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
            """
            pass

if False:
    O=lo('/Users/karlzipser/Desktop/_GPS3/1562023175.39.pkl')
    CA()

    #pts_plot(xys);plt_square()




#EOF
