from collections import Counter
from genericpath import isfile
from ntpath import join
import requests
import os
import json

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