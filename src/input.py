#####################################################################################
# Author: Jonathan Safer
# 
# Goal: Acquire data via serial port and hand it off to appropriate location (Cache)
#
#####################################################################################
import serial
import time
import random

def getTestInput(cache, portName):
    while(1):
        time.sleep(.1)
        dataValue = f"0 0 0 {random.randint(3, 9)}"
        milliseconds = str(int(time.time() * 1000))
        dataString = milliseconds + " " + dataValue
        cache.put(dataString)

def getInput(cache, portName):

    serialPort = serial.Serial(port = portName, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    serialString = ""                           # Used to hold data coming over UART

    while(1):

        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()
            #translate binary to text
            try:
                dataValue = serialString.decode('Ascii')
            except:
                print("ERROR: Invalid input")
    
            milliseconds = str(int(time.time() * 1000))
            dataString = milliseconds + " " + dataValue
            cache.put(dataString)

            #first piece of data is the type (0: flight state, 1: altitude etc..)
            #next pieces of data will depend on datatype, so should be handled independently (perhaps with a switch?)

            #serialPort.write(b"Hi \r\n") # This can be used to send a message to the flight computer