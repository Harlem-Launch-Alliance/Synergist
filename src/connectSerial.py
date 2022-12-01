import sys
import glob
import serial


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


print("Which port would you like to use: ")
serial_port_array = serial_ports()
# if len(serial_port_array = 0):
#     print("No serial port found. Check your connection")
port_count = 0
for i in serial_port_array:
    string = str(port_count)
    print(string + ": " + i) 
    port_count +=1

success = False
while(not success):
    x = input()
    if not x.isnumeric():
        print("Enter an Integer")
    else:
        x = int(x)
        if(len(serial_port_array) <= x or x<0):
            print("Your integer must be between 0 and " + str(len(serial_port_array)-1))
        else:
            success = True

print("Your serial port " + str(x))




