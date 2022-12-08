from multiprocessing import Process
import input
import time
import altitude
import connectSerial


if __name__ == '__main__': 
    portName = connectSerial.choosePort()
    p = Process(target=altitude.startDash)
    p.start()
    time.sleep(3)
    print("doing next thing")
    time.sleep(3)
    input.getInput(portName)