#####################################################################################
# Author: Jonathan Safer
# 
# Goal: Acquire data via serial port and hand it off to appropriate location (Cache)
#
#####################################################################################
import serial
import time
import random

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
                print("ERROR: Invalid non-ASCII input: check radio connection or baudrate")
                continue
    
            milliseconds = str(int(time.time() * 1000))
            dataString = milliseconds + " " + dataValue
            cache.put(dataString)

            #serialPort.write(b"Hi \r\n") # This can be used to send a message to the flight computer

def getTestInput(cache, portName): #generate sample telemtry for testing the dashboard
    counter = 0
    time.sleep(10)
    while(1):
        counter += 1
        time.sleep(.1)
        altitude = round(max(random.uniform(-1, 1), 500 - ((counter/10 - 50) * (counter/10 - 50)) + random.uniform(-1, 1)),2)
        if(counter < 280 and counter % 10 == 0):
            dataValue = f"0 0"
        elif(counter < 519 and counter % 10 == 0):
            dataValue = f"0 1"
        elif(counter < 800 and counter % 10 == 0):
            dataValue = f"0 2"
        elif(counter % 10 == 0):
            dataValue = f"0 3"
        else:
            dataValue = f"1 {altitude}"
        milliseconds = str(int(time.time() * 1000))
        dataString = milliseconds + " " + dataValue
        cache.put(dataString)

        #location data test

        lat = round(max(40, 40.75 + (counter/100 - 3.5)),5)
        lon = round(max(-74, -73.93 - (counter/100 - 3.5)),5)
        dataValue = f"3 {lat} {lon}"
        dataString = milliseconds + " " + dataValue
        cache.put(dataString)
