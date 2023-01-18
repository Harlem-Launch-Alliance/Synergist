#####################################################################################
# Author: Jonathan Safer
# 
# Goal: Stage telemetry for deployment on server
#
#####################################################################################
from datetime import datetime

altitudeCache = {
    "altitude": [],
    "time": []
}

flightState = {
    "ON_PAD": 0,
    "ASCENDING": 0,
    "DESCENDING": 0,
    "LANDED": 0,
    "last": "ON_PAD"
}

locationCache = {
    "latitude": [],
    "longitude": []
}

def cacheValue(dataString):
    dataArray = dataString.split()
    if(len(dataArray) < 2 or not dataArray[1].isnumeric()):
        print(dataString)
        return
    currentTime = datetime.fromtimestamp(int(dataArray[0])/1000.0)

    match dataArray[1]:
        case "0":#flight state
            updateFlightState(currentTime, dataArray[2])
        case "1": #altitude
            altitudeCache["time"].append(currentTime)
            altitudeCache["altitude"].append(float(dataArray[2]))
        case "3": #location
            locationCache["latitude"].append(float(dataArray[2]))
            locationCache["longitude"].append(float(dataArray[3]))
        case _: #default
            print("Invalid data format: ", dataString)

#record first occurance of each flight state to mark transitions. Also keep track of the latest state
def updateFlightState(time, state):
    match state:
        case "0":
            flightState["last"] = "ON_PAD"
            flightState["ON_PAD"] = flightState["ON_PAD"] or time
        case "1":
            flightState["last"] = "ASCENDING"
            flightState["ASCENDING"] = flightState["ASCENDING"] or time
        case "2":
            flightState["last"] = "DESCENDING"
            flightState["DESCENDING"] = flightState["DESCENDING"] or time
        case "3":
            flightState["last"] = "LANDED"
            flightState["LANDED"] = flightState["LANDED"] or time
        case _:
            print("ERROR: Invalid flight state detected")