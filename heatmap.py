import json
import folium
from folium.plugins import HeatMap

types = ["allTypes", "bus", "dBus", "exBus", "lBus", "nBus", "outBus", "tram", "stops", "setsOfStops"]
for typeName in types:
    with open('HeatMapData/'+typeName+"HeatMapData"+".json", "r") as jsonFile:
        data = json.load(jsonFile)
    map_object = folium.Map(location=[52.24,21.02], zoom_start=10)
    HeatMap(data,name=typeName,min_opacity=0.2,max_zoom=10, radius=50, blur=30).add_to(map_object)
    map_object.save("docs/"+typeName+"HeatMap.html")

