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

altitudeCache = []

def cacheValue(dataString):
    dataArray = dataString.split()
    currentTime = datetime.now()
    altitudeCache.append([currentTime, dataArray[3]])