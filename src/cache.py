#####################################################################################
# Author: Jonathan Safer
# 
# Goal: Stage telemetry for deployment on server
#
#####################################################################################
from datetime import datetime

datatypes = {
    "0": "Altitude",
    "1": "GPS",
    "2": "Orientation"
}

altitudeCache = {
    "altitude": [],
    "time": []
}

def cacheValue(dataString):
    dataArray = dataString.split()
    if(len(dataArray) < 2 or not dataArray[1].isnumeric()):
        print(dataString)
        return
    currentTime = datetime.fromtimestamp(int(dataArray[0])/1000.0)
    altitudeCache["time"].append(currentTime)
    altitudeCache["altitude"].append(float(dataArray[4]))