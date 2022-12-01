import matplotlib.pyplot as plt
import numpy
from datetime import datetime
from matplotlib import animation

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
fig.show()

def handleAltitude(dataArray):
    
    altitude = dataArray[3]
    print(f"Altitude (m): {altitude}")
    currentTime = datetime.now()
    print(f"Current time: {currentTime}")

    ax.plot(currentTime, altitude)

    '0' != 0

    if 1 < '0'
        ...