from collections import Counter
from genericpath import isfile
from ntpath import join
import requests
import os
import json
import matplotlib.pyplot as plt

# Create the /jsons directory if it doesn't exist
os.makedirs('jsons', exist_ok=True)

def fetch_and_save_data(api_url, apid_id, api_key, filename):
    try:
        # Make a GET request to the API
        api_url = api_url + api_id + '&apikey=' + api_key
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Save the response data as a JSON file
        with open(f'jsons/{filename}.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)

        print(f"Data saved to jsons/{filename}.json")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_data_from_json(filename, api_url_core, bus_lines_id, api_key):
    with open(f'jsons/{filename}.json', 'r') as json_file:
        data = json.load(json_file)
    shouldParse = False
    mypath='jsons/'
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    #print(onlyfiles)
    for item in data['result']:
        busStopId = item['values'][0]['value']
        busStopNr = item['values'][1]['value']
        if shouldParse:
            filename = 'LINES_'+busStopId+'_'+busStopNr+'.json'
            if filename not in onlyfiles:
                #print(filename)
                fetch_and_save_bus_lines_data(api_url_core, bus_lines_id, busStopId, busStopNr, api_key)
        if busStopId == '2460' and busStopNr == '01':
            shouldParse = True
        
    return data

def fetch_and_save_bus_lines_data(api_url_core, apid_id, busStopId, busStopNr, api_key):
    try:
        # Make a GET request to the API
        api_url = api_url_core + apid_id + '&busstopId=' + busStopId + '&busstopNr=' + busStopNr + '&apikey=' + api_key
        filename = 'LINES_'+busStopId+'_'+busStopNr
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Save the response data as a JSON file
        with open(f'jsons/{filename}.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=4)
        print(f"Data parsed from {api_url}")
        print(f"Data saved to jsons/{filename}.json")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def sorttuple(e):
    return e[1]

def plotting(data):

    # Separate the tuples into x and y values
    x_values = [x for x, y in data]

    value_counts = Counter(x_values)
    print(value_counts)
    sumLines = 0;
    sumStops = 0;
    for x, y in value_counts.items():
        sumLines+=x*y
    print(sumLines/len(data))
    

    newXVal = list(value_counts.keys())
    newYVal = list(value_counts.values())

    # Plot the data
    plt.scatter(newXVal, newYVal)
    plt.yscale('log')
    
    # Add labels and title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Ilość przystanków')
    plt.legend()

    # Show the plot
    plt.show()
    return



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
                    elif(dataType=="dBus" and i['values'][0]['value'][0]!='N'):
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
def printData(dataType, complex=False):
    resultData = []
    mypath='jsons/'
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    previousJ = ""
    currentLines = []
    for j in onlyfiles:
        if(complex and previousJ[6:10]!=j[6:10]):
            resultData.append((previousJ, len(set(currentLines))))
            currentLines=[]
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
                elif(dataType=="dBus" and i['values'][0]['value'][0]!='N'):
                    pass
                else:
                    continue;
                currentLines.append(i['values'][0]['value'])
            if(not complex):
                resultData.append((j, len(currentLines)))
                currentLines=[]
        previousJ=j
    if(complex):
        resultData.append((previousJ, len(set(currentLines))))
        currentLines=[]
    resultData.sort(key=sorttuple)
    print("Top 10 for type: "+dataType+" -----------------------------")
    print(resultData[-10:])
    return

def countStops():
    resultData = []
    mypath='jsons/'
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    currentSum = 0
    previousJ = ""
    for j in onlyfiles:
        with open(mypath+j, 'r') as json_file:
            data = json.load(json_file)

        if previousJ[6:10]==j[6:10]:
            if type(data['result'])!=str:
                currentSum+=1
        else:
            if previousJ!="":
                resultData.append((previousJ, currentSum))
            currentSum = 1

        previousJ=j
    resultData.append((previousJ, currentSum))
    resultData.sort(key=sorttuple)
    print("Top 10 most stops: "+" -----------------------------")
    print(resultData[-10:])
    return 


# Example usage
api_url = ''
api_id = ''
api_url_core = 'https://api.um.warszawa.pl/api/action/dbtimetable_get?id='  # Replace with your API URL
# api_id = 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'
bus_lines_id = '88cd555f-6f31-43ca-9de4-66c479ad5942'
api_key = 'f4351042-0e62-4be2-98b1-aec20b878958'
#fetch_and_save_data(api_url, api_id, api_key, 'przystanki')
#fetch_data_from_json('przystanki', api_url_core, bus_lines_id, api_key)
#fetch_and_analyze()
types = ["allTypes", "bus", "dBus", "exBus", "lBus", "nBus", "outBus", "tram"]
#for typeName in types:  
#    printData(typeName, complex)
#countStops()
saveSetsOfStopsHeatMapData()
