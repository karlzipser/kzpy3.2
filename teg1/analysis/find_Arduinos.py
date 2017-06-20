# http://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino

import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print p


# http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/

