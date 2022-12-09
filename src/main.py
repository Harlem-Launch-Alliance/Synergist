from multiprocessingQueue import MyQueue
from multiprocessing import Process
import input
import time
import altitude
import sys
import connectSerial


if __name__ == '__main__':
    inputCache = MyQueue() #this queue will be accessible across processes
    test = len(sys.argv) == 2 and sys.argv[1] == "test" #check if script is being run in test mode
    inputFunc = input.getTestInput if test else input.getInput #use test function if given test command

    if(test):
        print("Using test telemetry...")
        portName = "test"
        time.sleep(3)
    else:
        portName = connectSerial.choosePort()
    
    display = Process(target=altitude.startDash, args=(inputCache,)) #create dashboard as independent process
    serialInput = Process(target=inputFunc, args=(inputCache, portName,)) #create serial input as independent process
    #TODO create data logging as independent process

    print("Acquiring telemetry...")
    serialInput.start()#start input process
    time.sleep(3)
    print("Starting Dashboard...")
    display.start()#start displaying dashboard
    #TODO start logging data

    #prevent main process from exiting while children are still running
    serialInput.join()
    display.join()