from genericpath import isfile
from ntpath import join
import os
import json

def saveHeatMapData(dataType):
    with open(f'przystanki.json', 'r') as json_file:
        stops = json.load(json_file)
    stopsCoords = {}
    for stop in stops['result']:
        busStopId = stop['values'][0]['value']
        busStopNr = stop['values'][1]['value']
        latitude = stop['values'][4]['value']
        longitude = stop['values'][5]['value']
        stopsCoords[busStopId+'_'+busStopNr]=[latitude,longitude]
    heatMapData = []
    mypath='jsons/'
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    with open('HeatMapData/'+dataType+"HeatMapData.json","w") as file:
        for j in onlyfiles:
            with open(mypath+j, 'r') as json_file:
                data = json.load(json_file)
            if type(data['result'])!=str:
                for i in data['result']:
                    if(dataType=="allTypes"):
                        pass
                    elif(dataType=="tram" and len(i['values'][0]['value'])<3):
                        pass
                    elif(dataType=="bus" and len(i['values'][0]['value'])>2):
                        pass
                    elif(dataType=="lBus" and i['values'][0]['value'][0]=='L'):
                        pass
                    elif(dataType=="exBus" and len(i['values'][0]['value'])>2 and (i['values'][0]['value'][0]=='5' or i['values'][0]['value'][0]=='4')):
                        pass
                    elif(dataType=="outBus" and len(i['values'][0]['value'])>2 and (i['values'][0]['value'][0]=='7' or i['values'][0]['value'][0]=='8')):
                        pass
                    elif(dataType=="nBus" and i['values'][0]['value'][0]=='N'):
                        pass
                    elif(dataType=="dBus" and i['values'][0]['value'][0]!='N' and len(i['values'][0]['value'])>2):
                        pass
                    else:
                        continue;
                    heatMapData.append(stopsCoords.get(j[6:13]))
        json.dump(heatMapData, file)
    return

def saveStopsHeatMapData():
    with open(f'przystanki.json', 'r') as json_file:
        stops = json.load(json_file)
    heatMapData = []
    for stop in stops['result']:
        latitude = stop['values'][4]['value']
        longitude = stop['values'][5]['value']
        heatMapData.append([latitude,longitude])
    with open('HeatMapData/'+"stops"+"HeatMapData.json","w") as file:
        json.dump(heatMapData, file)
    return

def saveSetsOfStopsHeatMapData():
    with open(f'przystanki.json', 'r') as json_file:
        stops = json.load(json_file)
    heatMapData = []
    setsData = {}
    busStopId = 0
    for stop in stops['result']:
        busStopId = stop['values'][0]['value']
        latitude = stop['values'][4]['value']
        longitude = stop['values'][5]['value']
        if(busStopId in setsData):
            setsData[busStopId].append([latitude,longitude])
        else:
            setsData[busStopId] = [[latitude, longitude]]
    for stopSet in setsData:
        sumLat = 0
        sumLong = 0
        for coords in setsData[stopSet]:
            sumLat+=float(coords[0])
            sumLong+=float(coords[1]) 
        heatMapData.append([sumLat/len(setsData[stopSet]),sumLong/len(setsData[stopSet])])
    with open('HeatMapData/'+"setsOfStops"+"HeatMapData.json","w") as file:
        json.dump(heatMapData, file)
    return
