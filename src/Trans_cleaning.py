import cleaning_functions as clfun
import requests
import pandas as pd
import geopandas as gpd
from cartoframes.viz import Map, Layer, popup_element
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import mapping_functions as mapp
import json


# BICING

# We get all the information from the Bicing webpage in Json Format and we convert it to a dataframe

url = "https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information"
df=pd.read_json(url)
df = df["data"][0]

new_list = []
for i in df:
    name = i["name"]
    station_id = i['station_id']
    lat = i["lat"]
    lon = i["lon"]
    capacity = i["capacity"]
    new_list.append({"name":name, "station_id": station_id, "latitude":lat, "longitude":lon, "capacity": capacity}) 
bicing = pd.DataFrame(new_list)

# We create the base map with Barcelona coordenates

lat = 41.388431
long = 2.159569
base_map = Map(location=[lat, long], zoom_start=15)

# We create the heat map and add it to the base map

feature_group = mapp.get_feature(bicing, "Bicing stations density")
mapp.heat_map(bicing, feature_group,  15, "red", "red", "red", 1, 0.6, 0.6)

bicing.to_csv("Data/Transportation data/bicing.csv", index = False)

# METRO

railway = pd.read_csv("../Data/Transportation data/Metro.csv")

clfun.drop_column(railway  , ["CODI_CAPA", "CAPA_GENERICA", "ED50_COORD_X", "ED50_COORD_Y", "ETRS89_COORD_Y", "ETRS89_COORD_X", "DISTRICTE", "BARRI", "ADRECA", "TELEFON"])
clfun.drop_nan(railway , 0)
railway  = clfun.drop_value_less(railway , "NOM_CAPA", 10)
railway.rename(columns={'LATITUD': 'latitude', 'LONGITUD': 'longitude'}, inplace=True, errors='raise')

Metro= railway.loc[railway ["NOM_CAPA"]== "Metro i línies urbanes FGC"]
FGC = railway.loc[railway ["NOM_CAPA"]== "Ferrocarrils Generalitat (FGC)"]
Tramvia = railway.loc[railway ["NOM_CAPA"]== "Tramvia"]
Renfe = railway.loc[railway ["NOM_CAPA"]== "RENFE"]


# We create the heat map and add it to the base map

feature_group = mapp.get_feature("Metro", base_map)
mapp.heat_map(Metro, feature_group, 15, "blue", "blue", "blue", 1, 0.6, 0.6)

feature_group = mapp.get_feature("FGC", base_map)
mapp.heat_map(FGC, feature_group, 15, "blue", "blue", "blue", 1, 0.6, 0.6)

feature_group = mapp.get_feature("Tramvia", base_map)
mapp.heat_map(Tramvia, feature_group, 15, "blue", "blue", "blue", 1, 0.6, 0.6)

feature_group = mapp.get_feature("Renfe", base_map)
mapp.heat_map(Renfe, feature_group, 15, "blue", "blue", "blue", 1, 0.6, 0.6)



railway.to_csv("Data/Transportation data/railways.csv", index = False)
Metro.to_csv("Data/Transportation data/Metro.csv", index = False)
FGC.to_csv("Data/Transportation data/FGC.csv", index = False)
Tramvia.to_csv("Data/Transportation data/Tramvia.csv", index = False)
Renfe.to_csv("Data/Transportation data/Renfe.csv", index = False)


# BUS 

bus_stops = "Data/Transportation data/Bus stops.json"

with open(bus_stops, encoding='utf-8') as geo_bus:
    geo_bus = json.load(geo_bus)

new_list = []
new_list = mapp.get_variables(geo_bus, new_list)

bus_stops = pd.DataFrame(new_list)
bus_stops.rename(columns={'lat': 'latitude', 'lon': 'longitude'}, inplace=True, errors='raise')
bus_stops = gpd.GeoDataFrame(bus_stops, geometry=gpd.points_from_xy(bus_stops["longitude"], bus_stops["latitude"]))

# We delete the rows from points outside Barcelona

barcelona = "Data/bcn-geodata/terme-municipal/terme-municipal.geojson"

bus_stops = clfun.get_bcn_stops(barcelona, bus_stops)

bus_stops.to_csv("Data/Transportation data/bus_stops.csv", index = False)

feature_group = mapp.get_feature(bus_stops, "Bus stops density")
mapp.heat_map(bus_stops, feature_group, 7, "yellow", "yellow", "yellow", 1, 1, 1)

# We add the layer control module to the map.

folium.LayerControl().add_to(base_map)

