#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

baudrate = 115200
timeout = 0.1

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


if __name__ == '__main__':
    # python kzpy3/drafts/osx_gps.py
    flush_seconds = 0.1
    flush_timer = Timer(flush_seconds)
    P = {}
    sers = get_arduino_serial_connections(baudrate,timeout)
    assign_serial_connections(P,sers)
    file_timer = Timer(60)
    data = []
    xys = []
    os.system('mkdir -p '+opjD('GPS3'))
    while True:
        if file_timer.check():
            file_timer.reset()
            so(opjD('GPS3',d2n(time.time(),'.pkl')),{'data':data,'xys':xys})
            data = []
            xys = []
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
            xys.append([GPS3_input[1],GPS3_input[2]])
            cb('GPS3_input =',GPS3_input)
        except:
            pass

#EOF
