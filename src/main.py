from multiprocessing import Process
import input
import time
import altitude
import connectSerial
import sys


if __name__ == '__main__':
    test = len(sys.argv) == 2 and sys.argv[1] == "test" #check if script is being run in test mode
    portName = connectSerial.choosePort()
    p = Process(target=altitude.startDash) #start dashboard as independent process
    p.start()
    time.sleep(3)
    print("Acquiring telemetry...")
    time.sleep(3)
    if(test):
        print("Using test telemetry...")
        time.sleep(3)
        input.getTestInput()
    input.getInput(portName)