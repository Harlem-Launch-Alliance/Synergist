import sys
import glob
import serial
import time


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def choosePort():
    print("Please enter the number corresponding to your serial port.")
    serial_port_array = serial_ports()
    
    #while no serial ports present, keep checking for new devices
    while(len(serial_port_array) == 0):
        print("No serial port found. Check your connection.")
        serial_port_array = serial_ports()
        time.sleep(5)

    for i in range(len(serial_port_array)):
        print(f"{i}: {serial_port_array[i]}")
        
    while(True):
        portNumber = input()
        if not portNumber.isnumeric():
            print("Enter an integer.")
            continue
        portNumber = int(portNumber)
        if(len(serial_port_array) <= portNumber or portNumber<0):
            print("Please enter a number between 0 and " + str(len(serial_port_array)-1))
            continue
        break

    print("Your serial port is " + str(serial_port_array[portNumber]))
    return serial_port_array[portNumber]




