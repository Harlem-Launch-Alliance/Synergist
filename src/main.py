import serial
import connectSerial
import altitude

print(connectSerial.serial_ports())

portName = connectSerial.choosePort()

serialPort = serial.Serial(port = portName, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART

while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        #translate binary to text
        dataValue = serialString.decode('Ascii')
        #splits string into array based on spaces
        dataArray = dataValue.split()

        #first piece of data is the type (0: flight state, 1: altitude etc..)
        #next pieces of data will depend on datatype, so should be handled independently (perhaps with a switch?)
        altitude.handleAltitude(dataArray)

        #serialPort.write(b"Hi \r\n") # This can be used to send a message to the flight computer