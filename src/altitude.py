import matplotlib.pyplot as plt
import numpy
from datetime import datetime

altitudePlot = plt.plot([], [])
altitudePlot.show()

def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw()

def handleAltitude(dataArray):
    
    altitude = dataArray[3]
    print(f"Altitude (m): {altitude}")
    currentTime = datetime.now()
    print(f"Current time: {currentTime}")

    update_line(altitudePlot, [currentTime, altitude])